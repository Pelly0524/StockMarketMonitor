from huggingface_hub import hf_hub_download

# 下載模型
file_path = hf_hub_download(
    repo_id="foduucom/stockmarket-pattern-detection-yolov8", filename="best.pt"
)
print("Model downloaded to:", file_path)
