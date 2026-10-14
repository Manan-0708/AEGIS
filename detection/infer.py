"""Aerial target detection inference module for AEGIS.

Supports loading fine-tuned SARD_YOLO weights with automatic fallback to
pretrained Ultralytics YOLO models filtering for person targets.
Outputs structured JSON conforming to shared/schemas/detection.py.
"""

from datetime import datetime, timezone
import os
from pathlib import Path
import sys
from typing import List, Optional, Tuple, Union

import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Add repo root to sys.path so shared imports work consistently
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from shared.schemas.detection import BoundingBox, DetectionItem, DetectionResult


def resolve_model_path(custom_path: Optional[str] = None) -> Tuple[str, bool]:
    """Resolves the model weight path, checking custom checkpoints before falling back to pretrained YOLO.

    Args:
        custom_path: Explicitly provided model weights path or name.

    Returns:
        Tuple of (resolved_path_or_name, is_custom_sard_weights).
    """
    if custom_path:
        path = Path(custom_path)
        if path.exists():
            return str(path.resolve()), True
        return custom_path, False

    # Check environment variable
    env_weights = os.environ.get("MODEL_WEIGHTS_PATH")
    if env_weights and Path(env_weights).exists():
        return str(Path(env_weights).resolve()), True

    # Check local weights directory
    weights_dir = REPO_ROOT / "detection" / "weights"
    for candidate in ["best.pt", "sard.pt", "sard_yolo.pt"]:
        candidate_path = weights_dir / candidate
        if candidate_path.exists():
            return str(candidate_path.resolve()), True

    # Fallback to standard pretrained lightweight model
    return "yolov8n.pt", False


def run_detection(
    source: Union[str, Path, np.ndarray, Image.Image],
    model_path: Optional[str] = None,
    conf: float = 0.25,
    iou: float = 0.45,
) -> DetectionResult:
    """Runs person detection inference on an aerial image or array.

    Args:
        source: Path to image file, NumPy image array, or PIL Image.
        model_path: Optional explicit model weight file path or model name.
        conf: Confidence threshold filter (default: 0.25 for aerial targets).
        iou: NMS IoU threshold (default: 0.45).

    Returns:
        DetectionResult object conforming to the shared AEGIS contract.

    Raises:
        FileNotFoundError: If the source image path does not exist.
        ValueError: If input format is invalid.
    """
    # Validate source image file if path passed
    image_path_str = ""
    if isinstance(source, (str, Path)):
        src_path = Path(source)
        if not src_path.exists():
            raise FileNotFoundError(f"Source image not found: {src_path.resolve()}")
        image_path_str = str(src_path.resolve())
        pil_image = Image.open(src_path).convert("RGB")
    elif isinstance(source, Image.Image):
        pil_image = source.convert("RGB")
        image_path_str = "<memory_pil_image>"
    elif isinstance(source, np.ndarray):
        pil_image = Image.fromarray(source)
        image_path_str = "<memory_numpy_array>"
    else:
        raise ValueError(f"Unsupported source type: {type(source)}")

    img_width, img_height = pil_image.size
    weights, is_custom = resolve_model_path(model_path)

    # Lazy import ultralytics YOLO to keep module lightweight
    try:
        from ultralytics import YOLO
    except ImportError as e:
        raise ImportError(
            "ultralytics package is required for detection inference. "
            "Install with: pip install ultralytics"
        ) from e

    model = YOLO(weights)

    # For standard pretrained models, filter for COCO class 0 ('person')
    predict_kwargs = {"conf": conf, "iou": iou, "verbose": False}
    if not is_custom:
        predict_kwargs["classes"] = [0]

    results = model.predict(pil_image, **predict_kwargs)
    detections: List[DetectionItem] = []

    if results and len(results) > 0:
        first_res = results[0]
        boxes = first_res.boxes
        if boxes is not None:
            for idx, box in enumerate(boxes):
                coords = box.xyxy[0]
                if hasattr(coords, "tolist"):
                    coords = coords.tolist()
                coords = list(coords)

                conf_val = box.conf[0]
                if hasattr(conf_val, "item"):
                    conf_val = conf_val.item()
                confidence = float(conf_val)

                cls_val = box.cls[0]
                if hasattr(cls_val, "item"):
                    cls_val = cls_val.item()
                cls_id = int(cls_val)

                class_label = (
                    first_res.names.get(cls_id, "person")
                    if hasattr(first_res, "names") and isinstance(first_res.names, dict)
                    else "person"
                )

                # Clamp bounding boxes to image dimensions
                x1 = max(0.0, min(float(coords[0]), float(img_width)))
                y1 = max(0.0, min(float(coords[1]), float(img_height)))
                x2 = max(x1, min(float(coords[2]), float(img_width)))
                y2 = max(y1, min(float(coords[3]), float(img_height)))

                detections.append(
                    DetectionItem(
                        target_id=idx + 1,
                        bbox=BoundingBox(
                            x1=round(x1, 2),
                            y1=round(y1, 2),
                            x2=round(x2, 2),
                            y2=round(y2, 2),
                        ),
                        confidence=round(confidence, 4),
                        class_name=class_label,
                    )
                )

    return DetectionResult(
        image_path=image_path_str,
        image_width=img_width,
        image_height=img_height,
        target_count=len(detections),
        detections=detections,
        timestamp=datetime.now(timezone.utc).isoformat(),
        model_name=Path(weights).name if Path(weights).is_file() else str(weights),
    )


def save_annotated_image(
    image_source: Union[str, Path, Image.Image],
    result: DetectionResult,
    output_path: Union[str, Path],
) -> str:
    """Renders detection bounding boxes and confidence labels on an image and saves to disk."""
    if isinstance(image_source, (str, Path)):
        img = Image.open(image_source).convert("RGB")
    else:
        img = image_source.copy().convert("RGB")

    draw = ImageDraw.Draw(img)

    for item in result.detections:
        b = item.bbox
        # High-visibility neon green bounding box
        draw.rectangle([b.x1, b.y1, b.x2, b.y2], outline=(0, 255, 120), width=3)

        label = f"#{item.target_id} {item.class_name} {item.confidence:.2f}"
        text_bbox = draw.textbbox((b.x1, max(0.0, b.y1 - 18)), label)
        # Background badge for text legibility
        draw.rectangle(
            [text_bbox[0] - 2, text_bbox[1] - 2, text_bbox[2] + 2, text_bbox[3] + 2],
            fill=(0, 200, 90),
        )
        draw.text((b.x1, max(0.0, b.y1 - 18)), label, fill=(0, 0, 0))

    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_file, "JPEG", quality=95)
    return str(out_file.resolve())


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="AEGIS Aerial Person Detection Inference Pipeline"
    )
    parser.add_argument(
        "--source",
        type=str,
        required=True,
        help="Path to aerial test image or folder of images",
    )
    parser.add_argument(
        "--weights",
        type=str,
        default=None,
        help="Optional path to custom model weights (*.pt)",
    )
    parser.add_argument(
        "--conf",
        type=float,
        default=0.25,
        help="Confidence threshold (default: 0.25 for aerial views)",
    )
    parser.add_argument(
        "--iou",
        type=float,
        default=0.45,
        help="NMS IoU threshold (default: 0.45)",
    )
    parser.add_argument(
        "--save-json",
        type=str,
        default=None,
        help="Optional path to write output DetectionResult JSON",
    )
    parser.add_argument(
        "--save-img",
        type=str,
        default=None,
        help="Optional path to save annotated preview image with bounding boxes",
    )

    args = parser.parse_args()

    source_path = Path(args.source)
    if not source_path.exists():
        print(f"Error: Specified source path does not exist: {source_path}")
        sys.exit(1)

    targets_to_evaluate: List[Path] = []
    if source_path.is_file():
        targets_to_evaluate.append(source_path)
    elif source_path.is_dir():
        for ext in ["*.jpg", "*.jpeg", "*.png", "*.bmp"]:
            targets_to_evaluate.extend(source_path.glob(ext))

    if not targets_to_evaluate:
        print(f"No valid image files found in {source_path}")
        sys.exit(1)

    print(
        f"\n[AEGIS Detection] Evaluating {len(targets_to_evaluate)} image(s) (conf={args.conf}, iou={args.iou})"
    )
    resolved_w, is_custom = resolve_model_path(args.weights)
    print(
        f"[AEGIS Detection] Model weights: {resolved_w} ({'Custom SARD' if is_custom else 'Pretrained YOLO baseline'})"
    )

    for img_file in targets_to_evaluate:
        res = run_detection(img_file, model_path=args.weights, conf=args.conf, iou=args.iou)
        print(f"\n--- Results for {img_file.name} ---")
        print(f"Targets Detected: {res.target_count}")
        for det in res.detections:
            print(
                f"  - Target #{det.target_id}: [{det.bbox.x1}, {det.bbox.y1}, {det.bbox.x2}, {det.bbox.y2}] "
                f"({det.class_name}) conf={det.confidence:.4f}"
            )

        if args.save_json:
            json_target = Path(args.save_json)
            if len(targets_to_evaluate) > 1:
                json_target = (
                    json_target.parent / f"{img_file.stem}_detection.json"
                )
            res.save_json(json_target)
            print(f"Saved detection JSON: {json_target}")

        if args.save_img:
            img_target = Path(args.save_img)
            if len(targets_to_evaluate) > 1:
                img_target = (
                    img_target.parent / f"{img_file.stem}_annotated.jpg"
                )
            save_annotated_image(img_file, res, img_target)
            print(f"Saved annotated preview: {img_target}")


if __name__ == "__main__":
    main()
