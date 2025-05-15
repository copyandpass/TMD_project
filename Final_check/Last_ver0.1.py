from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyperclip
import time
import os
import requests
from rich.console import Console
from rich.markdown import Markdown

# 1️⃣ Selenium 브라우저 설정
options = Options()
# options.add_argument("--headless")  # 필요시 헤드리스 모드 사용
driver = webdriver.Chrome(options=options)

try:
    # 2️⃣ 릴리스AI 접속
    url = "https://lilys.ai/digest/3800693/2505424?s=1&nid=2505424"
    driver.get(url)
    time.sleep(2)  # 페이지 로딩 대기

    # 3️⃣ 강의 제목 추출
    try:
        lecture_title_elem = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div[4]/div/div[2]/div/div/span"))
        )
        full_text = lecture_title_elem.get_attribute("textContent").strip()
        lines = [line.strip() for line in full_text.split("\n") if "지금 가입하면" not in line and line.strip()]
        lecture_title = lines[0] if lines else "강의 제목 없음"
        print(f"📘 정제된 강의 제목: {lecture_title}")
    except Exception:
        print("❌ 강의 제목을 찾지 못했습니다. 기본 제목으로 진행합니다.")
        lecture_title = "강의 제목 없음"

    # 4️⃣ '스크립트' 탭 클릭
    try:
        script_btn = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/div[4]/div/div[3]/div[2]/div[2]/div[4]/div/div[1]/div[3]'))
        )
        script_btn.click()
        print("✅ '스크립트' 탭 클릭 완료")
    except Exception as e:
        print("❌ '스크립트' 탭 클릭 실패:", e)
        driver.quit()
        exit()

    time.sleep(3)  # 스크립트 로딩 대기

    # 5️⃣ 복사 버튼 클릭
    try:
        copy_btn = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, '//button[.//img[contains(@src, "copy")]]'))
        )
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", copy_btn)
        time.sleep(0.5)
        copy_btn.click()
        print("📋 복사 버튼 클릭 완료")
        time.sleep(1)
    except Exception as e:
        print("❌ 복사 버튼 클릭 실패:", e)
        driver.quit()
        exit()

    # 6️⃣ 클립보드에서 스크립트 추출
    try:
        script_text = pyperclip.paste()
        if not script_text.strip():
            raise ValueError("클립보드에 스크립트가 없습니다.")
        print("📎 스크립트 복사 완료")
    except Exception as e:
        print("❌ 클립보드 복사 실패:", e)
        script_text = "[스크립트 복사 실패]"

finally:
    driver.quit()

# 7️⃣ Gemini 프롬프트 구성
prompt = f"""
다음은 강의 영상의 전체 스크립트입니다.  
이 스크립트를 기반으로 **강의 영상의 상세 페이지를 작성하세요. 반드시 아래 출력 형식을 100% 그대로 따르세요.**  
다른 형식, 다른 섹션, 다른 문장은 절대 추가하거나 빼지 마세요.  
**당신의 답변은 오직 아래 출력 형식에 포함된 부분만 생성해야 합니다.**  

[학습자 수준: 초등학생 또는 중학생]  
- 눈에 잘 들어오도록 이모티콘이나 이모지를 넣어주세요.  
- 설명은 학습자의 수준에 맞게 쉽게 풀어 주세요.  
- 초등학생의 경우 어려운 용어는 최대한 피하고, 짧고 간단한 문장을 사용해 주세요.  
- 중학생의 경우 약간 어려운 용어도 쓸 수 있지만 반드시 쉬운 설명을 덧붙여 주세요.  
- 예시는 학습자의 생활과 밀접한 사례(예: 학교생활, 친구 관계, 스마트폰, 유튜브 등)를 활용해 주세요.  
- 내용은 지루하지 않도록 재미있고 친근한 톤으로 작성해 주세요.  
- 초등학생에게는 간단한 핵심만, 중학생에게는 조금 더 자세한 이유나 원리도 포함해 주세요.  

📜 스크립트:
====================
{script_text}
====================

📢 반드시 아래 출력 형식만을 따르세요.

[출력 형식 시작]

📘 강의 제목: {lecture_title}  
1. 강의 개요  
   - 배경 설명: 강의 주제가 중요한 이유  
   - 핵심 주제: 이번 강의의 핵심 개념 1–2문장  
   - 실생활 연결: 왜 배워야 하는지  

2. 학습 목표 / 기대 효과  
   - **초등학생용**  
     1) 인지 목표: 이해해야 할 핵심 개념  
     2) 행동 목표: 수업 후 할 수 있는 활동  
   - **중학생용**  
     1) 인지 목표: 개념 심화 설명  
     2) 분석 목표: 원리나 이유 설명  
   - 기대 효과: 수강 후 얻는 이점 1문장  

3. 강의 커리큘럼 / 목차  
   - 1) [00:00–05:00] 소주제 A 설명  
   - 2) [05:00–10:00] 소주제 B 토의  
   - 3) [10:00–15:00] 소주제 C 예시 실습  
   *(시간 배분은 예시이며, 실제 영상 길이에 맞춰 조정)*  

4. 강의 내용 설명 (상세 설명)  
   - **초등학생용**: 쉽고 짧은 문장으로 핵심 개념 전달  
   - **중학생용**: 전문 용어 + 쉬운 보충 설명  
   - 시각 자료: 도표·그림·실생활 사진 예시  
   - 생활 사례: 학교·친구·스마트폰 등 친숙한 예시  

5. Q&A / 피드백 섹션  
   - 예상 질문 1: “~이 부분이 잘 이해가 안 돼요” → 답변 + 추가 팁  
   - 예상 질문 2: “왜 이렇게 사용하는 건가요?” → 답변 + 학습 팁  
   - 추가 피드백: 실습 시 주의할 점  

[출력 형식 끝]
"""

# 8️⃣ Gemini API 요청
API_KEY = "AIzaSyBIj15XrDcbebWbbMoz-ROIx1mkmwwmmSw"  # 실제 배포 시 보안 주의, 환경 변수 사용 권장
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

headers = {
    "Content-Type": "application/json"
}
data = {
    "contents": [
        {
            "parts": [
                {"text": prompt}
            ]
        }
    ]
}

# 9️⃣ 응답 출력 및 저장
console = Console()
response = requests.post(API_URL, headers=headers, json=data)

if response.status_code == 200:
    result = response.json()
    text = result["candidates"][0]["content"]["parts"][0]["text"]

    console.rule(f"[bold green]📘 강의 제목: {lecture_title}")
    console.print(Markdown(text))

    os.makedirs("outputs", exist_ok=True)
    with open("outputs/gemini_output.md", "w", encoding="utf-8") as f:
        f.write(f"# 📘 강의 제목: {lecture_title}\n\n")
        f.write(text)
    print("✅ Gemini 응답이 outputs/gemini_output.md 에 저장되었습니다!")

else:
    console.print(f"[red]❌ Error {response.status_code}[/red]")
    console.print(response.text)
