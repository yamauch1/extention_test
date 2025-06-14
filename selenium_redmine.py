from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pickle
import os
import time

# クッキー保存用ファイルパス
COOKIES_FILE = "cookies.pkl"

# ログイン関数
def login(driver):
    driver.get("http://localhost:8080/login")
    driver.find_element(By.ID, "username").send_keys("admin")
    driver.find_element(By.ID, "password").send_keys("12345678")
    driver.find_element(By.ID, "password").submit()  # フォーム送信
    time.sleep(2)  # ログイン完了待機

# クッキーを保存
def save_cookies(driver):
    pickle.dump(driver.get_cookies(), open(COOKIES_FILE, "wb"))

# クッキーを読み込み
def load_cookies(driver):
    cookies = pickle.load(open(COOKIES_FILE, "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)

# メイン処理
def main():
    driver = webdriver.Edge()
    driver.get("http://localhost:8080/")  # クッキー追加前にドメインにアクセス

    # クッキーが存在すれば読み込み、なければログイン
    if os.path.exists(COOKIES_FILE):
        try:
            load_cookies(driver)
            driver.refresh()  # クッキーを適用
            print("クッキーを使ってセッションを復元しました")
        except:
            login(driver)
            save_cookies(driver)
            print("クッキーの読み込みに失敗したため、新規ログインしました")
    else:
        login(driver)
        save_cookies(driver)
        print("新規ログインしてクッキーを保存しました")

    # チケット作成ページに移動
    driver.get("http://localhost:8080/projects/prj-test/issues/new")

    # テキスト入力
    textarea = driver.find_element(By.ID, "issue_description")
    textarea.send_keys("""----------------------------
書き込みテスト
改行も対応可確認中
----------------------------""")

    # ステータス選択
    select = Select(driver.find_element(By.ID, "issue_status_id"))
    select.select_by_visible_text("中")

    time.sleep(3)  # 確認用


if __name__ == "__main__":
    main()