"""Shared data schemas for AEGIS aerial target detection."""

from datetime import datetime, timezone
import json
from pathlib import Path
from typing import List, Tuple
from pydantic import BaseModel, Field, model_validator


class BoundingBox(BaseModel):
    """Represents a 2D bounding box in pixel coordinates."""
    x1: float = Field(..., description="Top-left X coordinate in pixels")
    y1: float = Field(..., description="Top-left Y coordinate in pixels")
    x2: float = Field(..., description="Bottom-right X coordinate in pixels")
    y2: float = Field(..., description="Bottom-right Y coordinate in pixels")

    @model_validator(mode="after")
    def validate_coordinates(self) -> "BoundingBox":
        if self.x2 < self.x1:
            raise ValueError(f"x2 ({self.x2}) must be >= x1 ({self.x1})")
        if self.y2 < self.y1:
            raise ValueError(f"y2 ({self.y2}) must be >= y1 ({self.y1})")
        return self

    @property
    def width(self) -> float:
        return self.x2 - self.x1

    @property
    def height(self) -> float:
        return self.y2 - self.y1

    @property
    def center(self) -> Tuple[float, float]:
        return ((self.x1 + self.x2) / 2.0, (self.y1 + self.y2) / 2.0)

    def to_xyxy_list(self) -> List[float]:
        return [self.x1, self.y1, self.x2, self.y2]


class DetectionItem(BaseModel):
    """Represents a single detected target."""
    target_id: int = Field(..., description="Unique integer index of detected target")
    bbox: BoundingBox = Field(..., description="Bounding box in pixel coordinates")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Detection confidence score between 0.0 and 1.0")
    class_name: str = Field(default="person", description="Target object classification label")


class DetectionResult(BaseModel):
    """Standardized detection telemetry output for an aerial frame or image."""
    image_path: str = Field(..., description="Path to the evaluated image file")
    image_width: int = Field(..., gt=0, description="Width of the image in pixels")
    image_height: int = Field(..., gt=0, description="Height of the image in pixels")
    target_count: int = Field(..., ge=0, description="Total count of detected targets")
    detections: List[DetectionItem] = Field(default_factory=list, description="List of detected targets")
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="ISO 8601 UTC timestamp of inference"
    )
    model_name: str = Field(..., description="Name or path of model weights used for inference")

    def save_json(self, output_path: str | Path) -> Path:
        """Serializes detection result to formatted JSON on disk."""
        target = Path(output_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        with open(target, "w", encoding="utf-8") as f:
            f.write(self.model_dump_json(indent=2))
        return target

    @classmethod
    def load_json(cls, json_path: str | Path) -> "DetectionResult":
        """Loads and validates detection result from JSON on disk."""
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls.model_validate(data)
