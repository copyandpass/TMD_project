from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 1. 브라우저 실행 (Chrome 자동 설치 포함)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://gemini.google.com/app")  # 로그인은 수동으로 직접 진행

# 2. 프롬프트 입력창 로딩 대기 후 선택
input_box = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='textbox'][aria-label='여기에 프롬프트 입력']"))
)

# 3. 입력할 텍스트 정의
text = """
다음은 예시 프롬프트입니다.
이 텍스트는 Gemini에게 전달되어 응답을 받아올 것입니다.
중간에 줄바꿈도 자유롭게 가능합니다.
"""

# 4. JavaScript를 사용하여 텍스트 한 번에 입력
driver.execute_script("""
arguments[0].innerText = arguments[1];
arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
""", input_box, text)

# 5. 전송 버튼 클릭 (추천 XPath 기반)
send_button = WebDriverWait(driver, 25).until(
    EC.element_to_be_clickable((By.XPATH, "//button[.//mat-icon[text()='send']]"))
)
send_button.click()

# 6. Gemini 응답 결과 대기 및 추출
result_box = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, "/html/body/chat-app/main/side-navigation-v2/mat-sidenav-container/mat-sidenav-content/div/div[2]/chat-window/div/chat-window-content/div[1]/infinite-scroller/div/model-response/div/response-container/div/div[2]/div/div/message-content/div"))
)

# 7. 결과 출력
print("\n🧠 Gemini 응답:")
print(result_box.text)

# 8. 종료 대기 (수동 확인용)
input("\n🔚 엔터를 누르면 브라우저가 종료됩니다.")
driver.quit()
