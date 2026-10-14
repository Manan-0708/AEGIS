# Model Weights Directory

This directory stores fine-tuned YOLO model checkpoint files for aerial person detection.

### Supported Checkpoint Files:
- `best.pt` — Standard checkpoint from YOLO fine-tuning
- `sard.pt` — Fine-tuned SARD_YOLO dataset weights
- `sard_yolo.pt` — Alternative SARD_YOLO model checkpoint

### Google Drive Download:
Trained model weights are hosted on the AEGIS team Google Drive:
`https://drive.google.com/drive/folders/10CpW4MUXdUUGAECRarOE9qn1lQKXlFLo`

### Automatic Fallback:
If no custom checkpoint is placed in this directory, the inference pipeline in `detection/infer.py` automatically falls back to standard pretrained Ultralytics `yolov8n.pt` filtering for the `person` class.
