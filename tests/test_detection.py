"""Unit and contract tests for AEGIS aerial person detection pipeline."""

import json
from pathlib import Path
from unittest.mock import MagicMock
import pytest
from shared.schemas.detection import BoundingBox, DetectionItem, DetectionResult
from detection.infer import resolve_model_path, run_detection, save_annotated_image


class TestDetectionSchemas:
    """Tests data validation and serialization for detection contracts."""

    def test_bounding_box_valid(self):
        bbox = BoundingBox(x1=50.0, y1=100.0, x2=150.0, y2=200.0)
        assert bbox.width == 100.0
        assert bbox.height == 100.0
        assert bbox.center == (100.0, 150.0)
        assert bbox.to_xyxy_list() == [50.0, 100.0, 150.0, 200.0]

    def test_bounding_box_invalid_inversion(self):
        with pytest.raises(ValueError, match="must be >="):
            BoundingBox(x1=200.0, y1=100.0, x2=50.0, y2=200.0)

    def test_detection_result_save_and_load_json(self, tmp_path):
        bbox = BoundingBox(x1=10.0, y1=20.0, x2=80.0, y2=120.0)
        item = DetectionItem(target_id=1, bbox=bbox, confidence=0.9123, class_name="person")
        result = DetectionResult(
            image_path=str(tmp_path / "test.jpg"),
            image_width=1280,
            image_height=720,
            target_count=1,
            detections=[item],
            model_name="yolov8n.pt",
        )

        out_json = tmp_path / "result.json"
        saved_path = result.save_json(out_json)
        assert saved_path.exists()

        loaded = DetectionResult.load_json(saved_path)
        assert loaded.target_count == 1
        assert len(loaded.detections) == 1
        assert loaded.detections[0].confidence == 0.9123
        assert loaded.detections[0].bbox.x2 == 80.0


class TestModelPathResolution:
    """Tests model weights resolution and fallback logic."""

    def test_fallback_to_pretrained(self):
        weights, is_custom = resolve_model_path(None)
        assert "yolo" in weights.lower()
        assert is_custom is False

    def test_explicit_custom_path(self, tmp_path):
        custom_weights = tmp_path / "custom_sard.pt"
        custom_weights.write_text("weights_stub")
        weights, is_custom = resolve_model_path(str(custom_weights))
        assert weights == str(custom_weights.resolve())
        assert is_custom is True


class TestInferencePipeline:
    """Tests inference execution and error handling."""

    def test_missing_image_file_raises_not_found(self):
        with pytest.raises(FileNotFoundError):
            run_detection("non_existent_aerial_image.jpg")

    def test_run_detection_contract_with_mocked_yolo(self, tmp_path, monkeypatch):
        # Create a lightweight dummy test image
        from PIL import Image
        dummy_img_path = tmp_path / "sample.jpg"
        Image.new("RGB", (640, 480), color=(100, 150, 80)).save(dummy_img_path)

        # Mock YOLO model to test end-to-end contract logic without download dependency
        class MockBox:
            xyxy = [[100.0, 120.0, 180.0, 240.0]]
            conf = [0.875]
            cls = [0]

        class MockResult:
            boxes = [MockBox()]
            names = {0: "person"}

        mock_yolo_instance = MagicMock()
        mock_yolo_instance.predict.return_value = [MockResult()]

        import ultralytics
        monkeypatch.setattr(ultralytics, "YOLO", lambda weights: mock_yolo_instance)

        result = run_detection(dummy_img_path, conf=0.25)
        assert isinstance(result, DetectionResult)
        assert result.target_count == 1
        assert result.image_width == 640
        assert result.image_height == 480
        assert result.detections[0].class_name == "person"
        assert result.detections[0].confidence == 0.875
        assert result.detections[0].bbox.x1 == 100.0

    def test_save_annotated_image(self, tmp_path):
        from PIL import Image
        sample_img = tmp_path / "drone_raw.jpg"
        Image.new("RGB", (640, 480), color=(80, 120, 60)).save(sample_img)

        bbox = BoundingBox(x1=50.0, y1=60.0, x2=150.0, y2=180.0)
        item = DetectionItem(target_id=1, bbox=bbox, confidence=0.88, class_name="person")
        result = DetectionResult(
            image_path=str(sample_img),
            image_width=640,
            image_height=480,
            target_count=1,
            detections=[item],
            model_name="yolov8n.pt",
        )

        out_img = tmp_path / "annotated.jpg"
        saved = save_annotated_image(sample_img, result, out_img)
        assert Path(saved).exists()
