<<<<<<< HEAD
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# 1. Chrome 설정
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

try:
    # 2. 브라우저 실행
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://gemini.google.com/app")  # 수동 로그인

    # 3. 입력창 로딩 대기
    input_box = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='textbox'][aria-label='여기에 프롬프트 입력']"))
    )

    # 4. 텍스트 입력
    text = """
다음은 강의 영상의 전체 스크립트입니다. 이 스크립트를 기반으로 강의 영상의 상세 페이지를 작성해주세요.
상세 페이지의 구성은 다음과 같습니다:
=======
import requests
from rich.console import Console
from rich.markdown import Markdown

# 🎯 1. API 키 및 URL 설정
API_KEY = "AIzaSyBIj15XrDcbebWbbMoz-ROIx1mkmwwmmSw"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

headers = {
    "Content-Type": "application/json"
}

# 📄 2. 사용할 프롬프트
prompt = """
다음은 강의 영상의 전체 스크립트입니다. 이 스크립트를 기반으로 강의 영상의 상세 페이지를 작성해주세요. 상세 페이지의 구성은 다음과 같습니다:
>>>>>>> 6a6f0bf2a3a3368101b946c4803ae5523a311839

1. 강의 개요
2. 학습 목표 / 기대 효과
3. 강의 커리큘럼 / 목차
4. 강의 내용 설명 (상세 설명)
5. Q&A / 피드백 섹션

[학습자 수준: 초등학생 또는 중학생]

- 설명은 학습자의 수준에 맞게 쉽게 풀어 주세요.
- 초등학생의 경우 어려운 용어는 최대한 피하고, 짧고 간단한 문장을 사용해 주세요.
- 중학생의 경우 약간 어려운 용어도 쓸 수 있지만 반드시 쉬운 설명을 덧붙여 주세요.
- 예시는 학습자의 생활과 밀접한 사례(예: 학교생활, 친구 관계, 스마트폰, 유튜브 등)를 활용해 주세요.
- 내용은 지루하지 않도록 재미있고 친근한 톤으로 작성해 주세요.
- 초등학생에게는 간단한 핵심만, 중학생에게는 조금 더 자세한 이유나 원리도 포함해 주세요.

아래는 스크립트입니다:
====================
(여기에 스크립트 내용 입력)
====================

"""

<<<<<<< HEAD

    driver.execute_script("""
    arguments[0].innerText = arguments[1];
    arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
    """, input_box, text)

    # 5. 전송 버튼 클릭
    send_button = WebDriverWait(driver, 25).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/chat-app/main/side-navigation-v2/mat-sidenav-container/mat-sidenav-content/div/div[2]/chat-window/div/input-container/div/input-area-v2/div/div/div[3]/div/div[2]/button"))
    )
    send_button.click()

    # 6. 가장 최근 응답 요소 로딩 및 텍스트 확인까지 대기
    WebDriverWait(driver, 30).until(
        lambda d: d.find_element(By.XPATH, "(//message-content)[last()]").text.strip() != ""
    )
    time.sleep(2)  # 약간 더 기다리기 (렌더링 지연 방지)

    # 7. 응답 박스를 다시 가져와야 stale 방지됨!
    result_box = driver.find_element(By.XPATH, "(//message-content)[last()]")

    # 8. 자식 텍스트 추출
    text_elements = result_box.find_elements(By.XPATH, ".//*")
    full_response = "\n".join(el.text.strip() for el in text_elements if el.text.strip())

    print("\n🧠 Gemini 응답:")
    print(full_response)

    input("\n🔚 엔터를 누르면 브라우저 종료됩니다.")
    driver.quit()

except Exception as e:
    print("❌ 오류 발생:", e)
    driver.save_screenshot("error.png")
    try:
        driver.quit()
    except:
        pass
=======
# 📨 3. 요청 데이터 구성
data = {
    "contents": [
        {
            "parts": [
                {"text": prompt}
            ]
        }
    ]
}

# 🚀 4. API 요청
response = requests.post(API_URL, headers=headers, json=data)

# 🖨️ 5. 응답 출력 (Markdown + Emoji 지원)
console = Console()

if response.status_code == 200:
    result = response.json()
    text = result["candidates"][0]["content"]["parts"][0]["text"]
    
    console.rule("[bold cyan]🧠 Gemini 응답")  # 구분선
    console.print(Markdown(text))             # Markdown으로 예쁘게 출력
else:
    console.print(f"[red]❌ Error {response.status_code}[/red]")
    console.print(response.text)
>>>>>>> 6a6f0bf2a3a3368101b946c4803ae5523a311839
