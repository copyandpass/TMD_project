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
