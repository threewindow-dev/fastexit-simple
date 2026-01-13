#!/usr/bin/env python3
"""
Selenium을 사용한 FastExit 웹 애플리케이션 테스트
"""

import time
import sys
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.service import Service

# 테스트 URL
FRONTEND_URL = "http://localhost:3001"
BACKEND_URL = "http://localhost:8001"
BACKEND_DOCS_URL = f"{BACKEND_URL}/docs"

def setup_driver():
    """Chrome 드라이버 설정"""
    print("Setting up Chrome driver...")
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # 헤드리스 모드
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-web-resources')
    options.add_argument('--window-size=1920,1080')
    options.binary_location = "/usr/bin/chromium-browser"  # 시스템 Chromium 사용
    
    try:
        # ChromeDriver 경로 지정
        service = Service("/usr/bin/chromedriver")
        driver = webdriver.Chrome(service=service, options=options)
        print("✓ Chrome driver initialized")
        return driver
    except WebDriverException as e:
        print(f"✗ Failed to initialize Chrome driver: {e}")
        print(f"  ChromeDriver location: {os.path.exists('/usr/bin/chromedriver')}")
        print(f"  Chromium location: {os.path.exists('/usr/bin/chromium-browser')}")
        sys.exit(1)

def test_backend_api(driver):
    """Backend API 문서 페이지 테스트"""
    print(f"\n--- Testing Backend API: {BACKEND_DOCS_URL} ---")
    
    try:
        driver.get(BACKEND_DOCS_URL)
        print(f"✓ Navigated to {BACKEND_DOCS_URL}")
        
        # 페이지 로드 대기
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        
        # 페이지 타이틀 확인
        title = driver.title
        print(f"  Page Title: {title}")
        
        # FastAPI Swagger UI 확인
        if "FastAPI" in driver.page_source or "swagger" in driver.page_source.lower():
            print("✓ Backend API docs page loaded successfully")
            return True
        else:
            print("✗ Backend API docs page not properly loaded")
            print(f"  Page source preview: {driver.page_source[:500]}")
            return False
            
    except TimeoutException:
        print(f"✗ Timeout loading {BACKEND_DOCS_URL}")
        return False
    except Exception as e:
        print(f"✗ Error testing backend: {e}")
        return False

def test_frontend(driver):
    """Frontend 페이지 테스트"""
    print(f"\n--- Testing Frontend: {FRONTEND_URL} ---")
    
    try:
        driver.get(FRONTEND_URL)
        print(f"✓ Navigated to {FRONTEND_URL}")
        
        # 페이지 로드 대기 (최대 15초)
        WebDriverWait(driver, 15).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        
        # 페이지 타이틀 확인
        title = driver.title
        print(f"  Page Title: {title}")
        
        # 페이지 소스 확인
        page_source = driver.page_source
        
        # Next.js 애플리케이션 확인
        if "Next.js" in page_source or "__NEXT_DATA__" in page_source:
            print("✓ Next.js application detected")
        
        # 에러 메시지 확인
        if "error" in page_source.lower() and "500" in page_source:
            print("✗ Page shows error message")
            print(f"  Page source preview: {page_source[:1000]}")
            return False
        
        # body 태그 확인
        try:
            body = driver.find_element(By.TAG_NAME, "body")
            body_text = body.text[:500] if body.text else "Empty body"
            print(f"  Body content preview: {body_text}")
        except Exception as e:
            print(f"  Could not get body content: {e}")
        
        print("✓ Frontend page loaded")
        
        # 스크린샷 저장
        screenshot_path = "/tmp/fastexit-frontend-screenshot.png"
        driver.save_screenshot(screenshot_path)
        print(f"  Screenshot saved: {screenshot_path}")
        
        return True
        
    except TimeoutException:
        print(f"✗ Timeout loading {FRONTEND_URL}")
        return False
    except Exception as e:
        print(f"✗ Error testing frontend: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """메인 테스트 실행"""
    print("=" * 60)
    print("FastExit Web Application Test with Selenium")
    print("=" * 60)
    
    driver = None
    try:
        driver = setup_driver()
        
        # Backend 테스트
        backend_ok = test_backend_api(driver)
        
        # Frontend 테스트
        frontend_ok = test_frontend(driver)
        
        # 결과 출력
        print("\n" + "=" * 60)
        print("Test Results:")
        print(f"  Backend API: {'✓ PASS' if backend_ok else '✗ FAIL'}")
        print(f"  Frontend:    {'✓ PASS' if frontend_ok else '✗ FAIL'}")
        print("=" * 60)
        
        if not backend_ok or not frontend_ok:
            sys.exit(1)
        
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        if driver:
            driver.quit()
            print("\n✓ Driver closed")

if __name__ == "__main__":
    main()
