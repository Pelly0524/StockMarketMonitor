import time
import mss
import cv2
import numpy as np
from ultralytics import YOLO

# 載入模型
model = YOLO(r"best.pt")

# 設定模型參數
model.overrides["conf"] = 0.15  # NMS 置信度閾值
model.overrides["iou"] = 0.6  # NMS IoU 閾值
model.overrides["agnostic_nms"] = False  # NMS 是否類別無關
model.overrides["max_det"] = 1000  # 每張圖片的最大檢測數量

# 初始化螢幕截圖工具
sct = mss.mss()

# 調整 Monitor 1 的範圍
monitor = {"top": max(0, -135), "left": 2560, "width": 2560, "height": 1600}

while True:
    # 擷取螢幕畫面
    screenshot = sct.grab(monitor)
    frame = np.array(screenshot)

    # 將 BGRA 轉換為 BGR
    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

    # 執行 YOLOv8 推論
    results = model(frame)

    # 在畫面上繪製檢測結果
    annotated_frame = results[0].plot()

    # 顯示畫面
    cv2.imshow("YOLOv8 Monitor 1", annotated_frame)

    # 加入延遲
    time.sleep(0.1)

    # 按下 'q' 鍵退出
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# 釋放資源
cv2.destroyAllWindows()
