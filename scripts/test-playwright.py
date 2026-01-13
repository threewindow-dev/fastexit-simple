#!/usr/bin/env python3
"""
Playwright를 사용한 FastExit 웹 애플리케이션 테스트
(WSL에 최적화된 버전)
"""

import asyncio
import sys
from playwright.async_api import async_playwright

# 테스트 URL
FRONTEND_URL = "http://localhost:3001"
BACKEND_URL = "http://localhost:8001"
BACKEND_DOCS_URL = f"{BACKEND_URL}/docs"

async def test_backend_api(page):
    """Backend API 문서 페이지 테스트"""
    print(f"\n--- Testing Backend API: {BACKEND_DOCS_URL} ---")
    
    try:
        response = await page.goto(BACKEND_DOCS_URL, wait_until="load", timeout=15000)
        print(f"✓ Navigated to {BACKEND_DOCS_URL}")
        print(f"  Status: {response.status}")
        
        # 페이지 타이틀 확인
        title = await page.title()
        print(f"  Page Title: {title}")
        
        # 페이지 컨텐츠 확인
        page_content = await page.content()
        
        # FastAPI Swagger UI 확인
        if "FastAPI" in page_content or "swagger" in page_content.lower():
            print("✓ Backend API docs page loaded successfully")
            return True
        else:
            print("✗ Backend API docs page not properly loaded")
            return False
            
    except Exception as e:
        print(f"✗ Error testing backend: {e}")
        return False

async def test_frontend(page):
    """Frontend 페이지 테스트"""
    print(f"\n--- Testing Frontend: {FRONTEND_URL} ---")
    
    try:
        response = await page.goto(FRONTEND_URL, wait_until="load", timeout=15000)
        print(f"✓ Navigated to {FRONTEND_URL}")
        print(f"  Status: {response.status}")
        
        # 페이지 로드 대기
        await page.wait_for_load_state("networkidle", timeout=10000)
        
        # 페이지 타이틀 확인
        title = await page.title()
        print(f"  Page Title: {title}")
        
        # 페이지 컨텐츠 확인
        page_content = await page.content()
        
        # Next.js 애플리케이션 확인
        if "Next.js" in page_content or "__NEXT_DATA__" in page_content:
            print("✓ Next.js application detected")
        
        # 에러 메시지 확인
        if "error" in page_content.lower() and "500" in page_content:
            print("✗ Page shows error message")
            return False
        
        # 페이지 타이틀로 콘텐츠 확인
        if "FastExit" in title:
            print("✓ FastExit title found")
        
        # 사용자 목록 섹션이 있는지 확인
        try:
            # 사용자 목록을 찾기 위해 몇 초 대기
            await asyncio.sleep(2)
            body_text = await page.text_content("body")
            if body_text and len(body_text) > 100:
                print(f"✓ Page content loaded (length: {len(body_text)} chars)")
            else:
                print("⚠ Page content seems minimal")
        except Exception as e:
            print(f"⚠ Could not verify body content: {e}")
        
        # 스크린샷 저장
        screenshot_path = "/tmp/fastexit-frontend-screenshot.png"
        await page.screenshot(path=screenshot_path)
        print(f"✓ Screenshot saved: {screenshot_path}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error testing frontend: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """메인 테스트 실행"""
    print("=" * 60)
    print("FastExit Web Application Test with Playwright")
    print("=" * 60)
    
    async with async_playwright() as p:
        try:
            # Chromium 브라우저 시작
            print("\n📦 Launching Chromium browser...")
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            print("✓ Browser launched successfully")
            
            # Backend 테스트
            backend_ok = await test_backend_api(page)
            
            # Frontend 테스트
            frontend_ok = await test_frontend(page)
            
            # 결과 출력
            print("\n" + "=" * 60)
            print("Test Results:")
            print(f"  Backend API: {'✓ PASS' if backend_ok else '✗ FAIL'}")
            print(f"  Frontend:    {'✓ PASS' if frontend_ok else '✗ FAIL'}")
            print("=" * 60)
            
            # 정리
            await context.close()
            await browser.close()
            
            if not backend_ok or not frontend_ok:
                sys.exit(1)
            
        except Exception as e:
            print(f"\n✗ Test failed with error: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
