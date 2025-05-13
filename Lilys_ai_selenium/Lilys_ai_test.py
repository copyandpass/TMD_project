from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyperclip
import time
import os

options = Options()
# options.add_argument("--headless")  # 디버깅 위해 비활성화 권장
driver = webdriver.Chrome(options=options)

try:
    url = "https://lilys.ai/digest/3784018/2480672?s=1&nid=2480672"
    driver.get(url)

    # 스크립트 버튼 클릭
    script_button_xpath = "/html/body/div[1]/div[1]/div[3]/div/div[3]/div[2]/div[2]/div[4]/div/div[1]/div[3]/div/div/div"
    script_btn = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, script_button_xpath))
    )
    script_btn.click()
    time.sleep(2)  # 콘텐츠 로딩 대기

    # 복사 버튼 (img → button 부모)
    copy_button_xpath = "/html/body/div[1]/div[1]/div[2]/div/div[3]/div[3]/div[1]/div[4]/div[2]/div[3]/div[2]/button"
    copy_btn = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, copy_button_xpath))
    )

    # 클릭 가능할 때까지 대기 후 강제 클릭
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, copy_button_xpath))
    )
    driver.execute_script("arguments[0].click();", copy_btn)

    time.sleep(1.5)  # 클립보드 복사 대기

    # 클립보드에서 텍스트 읽기
    copied_text = pyperclip.paste()

    # 콘솔 출력
    print("\n📄 복사된 스크립트 내용:")
    print("=" * 50)
    print(copied_text)
    print("=" * 50)

    # 파일 저장
    os.makedirs("scripts", exist_ok=True)
    with open("scripts/copied_script.txt", "w", encoding="utf-8") as f:
        f.write(copied_text)

    print("\n✅ 스크립트가 성공적으로 저장되었습니다!")

finally:
    driver.quit()
