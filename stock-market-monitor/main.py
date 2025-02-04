import cv2
import time
import numpy as np
import threading
from ultralytics import YOLO

# 從你先前寫好的檔案匯入產生圖表的函式
from ccxt_btc_chart import fetch_and_plot_btc_usdt_binance
from ccxt_eth_chart import fetch_and_plot_eth_usdt_binance
from ccxt_sol_chart import fetch_and_plot_sol_usdt_binance
from ccxt_paxg_chart import fetch_and_plot_paxg_usdt_binance

# --------------------- 設定 YOLO 模型 ---------------------
model = YOLO("best.pt")
model.overrides["conf"] = 0.15
model.overrides["iou"] = 0.6
model.overrides["agnostic_nms"] = False
model.overrides["max_det"] = 1000

# 圖片路徑列表 (要不斷讀取這四張圖片)
chart_paths = [
    "charts/btc_15m_chart_binance.png",
    "charts/eth_15m_chart_binance.png",
    "charts/sol_15m_chart_binance.png",
    "charts/paxg_15m_chart_binance.png",
]


# ------------------ Worker Thread: 更新圖表 ------------------
def update_charts_loop():
    """
    持續更新 4 張圖表的 Worker Thread
    可酌情在裡面加 sleep() 控制頻率，避免呼叫交易所 API 過於頻繁
    """
    while True:
        try:
            fetch_and_plot_btc_usdt_binance()
            fetch_and_plot_eth_usdt_binance()
            fetch_and_plot_sol_usdt_binance()
            fetch_and_plot_paxg_usdt_binance()
        except Exception as e:
            print(f"Error updating charts: {e}")
        # 休息 10 秒，避免過度頻繁的 API 呼叫
        time.sleep(10)


# ------------------ 主程式 (Main Thread) ------------------
def main():
    # 1) 先啟動多執行緒更新圖表
    chart_thread = threading.Thread(target=update_charts_loop, daemon=True)
    chart_thread.start()

    # 2) 建立全螢幕視窗
    window_name = "YOLOv8 Inference (BTC/ETH/SOL/PAXG) - Fullscreen"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    while True:
        # A) 讀取 4 張圖（未推論），先做拼接
        valid_images = []
        for path in chart_paths:
            img = cv2.imread(path)
            if img is None:
                print(f"Failed to read image: {path}")
                continue
            valid_images.append(img)

        # 確定 4 張都成功讀取後才進行拼接
        if len(valid_images) == 4:
            # 假設四張圖大小相同，直接 hstack + vstack
            top_row = np.hstack((valid_images[0], valid_images[1]))
            bottom_row = np.hstack((valid_images[2], valid_images[3]))
            combined = np.vstack((top_row, bottom_row))

            # B) 對拼接後的大圖做 YOLO 推論
            results = model(combined)
            # 把推論結果 (boxes, labels 等) 疊加到影像上
            annotated_combined = results[0].plot()

            # C) 顯示於全螢幕視窗
            cv2.imshow(window_name, annotated_combined)

        # D) 每回合給一點延遲，並處理鍵盤事件
        #    這樣才不會卡住視窗，也可讓使用者按下 'q' 離開
        key = cv2.waitKey(2000)  # 2秒
        if key & 0xFF == ord("q"):
            break

    # E) 結束視窗
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
