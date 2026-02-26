# main.py
import network
import time
from machine import Pin
import urequests  # MicroPythonでHTTP通信を行うためのライブラリ

# --- 設定項目（ご自身の環境に合わせて書き換えてください） ---
WIFI_SSID = "YOUR_WIFI_SSID"
WIFI_PASSWORD = "YOUR_WIFI_PASSWORD"
GAS_URL = "https://script.google.com/macros/s/YOUR_GAS_ID/exec"

# --- 1. Wi-Fi接続処理 ---
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print("Wi-Fiに接続中...")
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    while not wlan.isconnected():
        print(".")
        time.sleep(1)
print("Wi-Fi接続成功！ IP:", wlan.ifconfig()[0])

# --- 2. センサーの初期設定 ---
sensor = Pin(4, Pin.IN, Pin.PULL_UP)

# 「前回のドアの状態」を記憶する変数（0: 閉、 1: 開）
# 起動時の状態を最初の「前回の状態」として記憶します
previous_state = sensor.value()

print("ドア監視システム起動。監視を開始します...")

# --- 3. メインループ（監視処理） ---
while True:
    current_state = sensor.value()  # 今のドアの状態を取得

    # 【エッジ検知】前回が「0(閉)」で、今回が「1(開)」に変化した瞬間だけ実行！
    if previous_state == 0 and current_state == 1:
        print("【検知】ドアが開きました！メールを送信します...")

        try:
            # GASのURLにアクセス（ブラウザでURLを開くのと同じ動作）
            response = urequests.get(GAS_URL)
            print("サーバーからの返答:", response.text)
            response.close()  # 通信を終了してメモリを解放
            print("メール送信完了。次の動作を待機します。")
        except Exception as e:
            print("通信エラー発生:", e)

    # 今の状態を「前回の状態」として上書き保存し、次のループへ
    previous_state = current_state

    time.sleep(0.5)  # 0.5秒おきに監視