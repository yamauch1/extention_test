import sys
import json
import struct
import pickle
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

# 設定
COOKIES_FILE = "cookies.pkl"
driver = None  # グローバルでブラウザを保持

# メッセージ処理用関数
def send_message(message):
    encoded = json.dumps(message).encode('utf-8')
    sys.stdout.write(struct.pack('I', len(encoded)))
    sys.stdout.write(encoded)
    sys.stdout.flush()

def read_message():
    raw_length = sys.stdin.read(4)
    if not raw_length:
        return None
    length = struct.unpack('@I', raw_length)[0]
    return sys.stdin.read(length)

# ログイン処理
def login():
    driver.get("http://localhost:8080/login")
    driver.find_element(By.ID, "username").send_keys("admin")
    driver.find_element(By.ID, "password").send_keys("12345678")
    driver.find_element(By.ID, "password").submit()
    time.sleep(2)
    return {"status": "logged_in"}

# クッキー操作
def save_cookies():
    pickle.dump(driver.get_cookies(), open(COOKIES_FILE, "wb"))

def load_cookies():
    if os.path.exists(COOKIES_FILE):
        cookies = pickle.load(open(COOKIES_FILE, "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)
        return True
    return False

# チケット作成
def create_ticket():
    driver.get("http://localhost:8080/projects/prj-test/issues/new")
    
    textarea = driver.find_element(By.ID, "issue_description")
    textarea.send_keys("""----------------------------
書き込みテスト
改行も対応可確認中
----------------------------""")

    select = Select(driver.find_element(By.ID, "issue_status_id"))
    select.select_by_visible_text("中")
    
    return {"status": "ticket_created"}

# メイン処理
def handle_command(data):
    global driver
    
    try:
        if data.get("command") == "init":
            driver = webdriver.Edge()
            driver.get("http://localhost:8080/")
            
            if not load_cookies():
                login()
                save_cookies()
            return {"status": "ready"}
            
        elif data.get("command") == "create_ticket":
            return create_ticket()
            
        elif data.get("command") == "screenshot":
            driver.save_screenshot("screenshot.png")
            return {"status": "screenshot_saved"}
            
        else:
            return {"error": "unknown_command"}
            
    except Exception as e:
        return {"error": str(e)}

# Native Messagingループ
def main():
    while True:
        message = read_message()
        if not message:
            break
            
        try:
            data = json.loads(message)
            response = handle_command(data)
            send_message(response)
            
        except json.JSONDecodeError:
            send_message({"error": "invalid_json"})
        except Exception as e:
            send_message({"error": f"unexpected_error: {str(e)}"})

if __name__ == "__main__":
    main()