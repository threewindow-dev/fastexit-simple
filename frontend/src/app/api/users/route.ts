import { NextRequest, NextResponse } from 'next/server';

// 백엔드 FastAPI URL (컨테이너 내부 통신)
const BACKEND_URL = process.env.BACKEND_URL || 'http://backend:8000';

export async function GET() {
  try {
    const response = await fetch(`${BACKEND_URL}/api/users`);
    
    if (!response.ok) {
      return NextResponse.json(
        { error: 'Failed to fetch users from backend' },
        { status: response.status }
      );
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('BFF Error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    
    const response = await fetch(`${BACKEND_URL}/api/users`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      return NextResponse.json(
        { error: 'Failed to create user' },
        { status: response.status }
      );
    }

    const data = await response.json();
    return NextResponse.json(data, { status: 201 });
  } catch (error) {
    console.error('BFF Error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
