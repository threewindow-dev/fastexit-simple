from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg
from psycopg.rows import dict_row
import os
from typing import List, Optional

app = FastAPI(title="FastExit API")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인으로 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 데이터베이스 연결 설정
def get_db_connection():
    # 환경 변수가 없으면 명시적으로 에러 발생 (보안)
    db_password = os.getenv("DB_PASSWORD")
    if not db_password:
        raise ValueError("DB_PASSWORD environment variable is required")
    
    conn = psycopg.connect(
        host=os.getenv("DB_HOST", "postgres"),
        dbname=os.getenv("DB_NAME", "fastexit"),
        user=os.getenv("DB_USER", "postgres"),
        password=db_password,
        port=os.getenv("DB_PORT", "5432"),
        row_factory=dict_row
    )
    return conn

# Pydantic 모델
class User(BaseModel):
    id: Optional[int] = None
    username: str
    email: str
    full_name: Optional[str] = None

class UserCreate(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None

@app.on_event("startup")
async def startup_event():
    """애플리케이션 시작 시 데이터베이스 테이블 초기화"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                # users 테이블 생성
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        username VARCHAR(100) UNIQUE NOT NULL,
                        email VARCHAR(255) UNIQUE NOT NULL,
                        full_name VARCHAR(255),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # 샘플 데이터 삽입 (테이블이 비어있을 경우)
                cur.execute("SELECT COUNT(*) FROM users")
                count = cur.fetchone()["count"]
                
                if count == 0:
                    sample_users = [
                        ("john_doe", "john@example.com", "John Doe"),
                        ("jane_smith", "jane@example.com", "Jane Smith"),
                        ("bob_wilson", "bob@example.com", "Bob Wilson"),
                    ]
                    
                    for username, email, full_name in sample_users:
                        cur.execute(
                            "INSERT INTO users (username, email, full_name) VALUES (%s, %s, %s)",
                            (username, email, full_name)
                        )
                
                conn.commit()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {e}")

@app.get("/")
async def root():
    """헬스 체크"""
    return {"message": "FastExit API is running", "status": "healthy"}

@app.get("/api/users", response_model=List[User])
async def get_users():
    """모든 사용자 조회"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, username, email, full_name FROM users ORDER BY id")
                users = cur.fetchall()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/api/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    """특정 사용자 조회"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, username, email, full_name FROM users WHERE id = %s", (user_id,))
                user = cur.fetchone()
        
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.post("/api/users", response_model=User, status_code=201)
async def create_user(user: UserCreate):
    """새 사용자 생성"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO users (username, email, full_name) VALUES (%s, %s, %s) RETURNING id, username, email, full_name",
                    (user.username, user.email, user.full_name)
                )
                new_user = cur.fetchone()
            conn.commit()
        return new_user
    except psycopg.errors.UniqueViolation:
        raise HTTPException(status_code=400, detail="Username or email already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.delete("/api/users/{user_id}", status_code=204)
async def delete_user(user_id: int):
    """사용자 삭제"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM users WHERE id = %s RETURNING id", (user_id,))
                deleted = cur.fetchone()
            conn.commit()
        
        if deleted is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
