"""Script to generate a synthetic reference aerial test image for AEGIS detection validation."""

from pathlib import Path
from PIL import Image, ImageDraw


def create_reference_aerial_image(output_path: str | Path = "detection/samples/reference_aerial.jpg") -> Path:
    """Creates a synthetic aerial test scene representing terrain with isolated human targets."""
    target_path = Path(output_path)
    target_path.parent.mkdir(parents=True, exist_ok=True)

    # 1280x720 aerial aspect ratio
    width, height = 1280, 720
    # Background: brownish-green rugged search terrain
    img = Image.new("RGB", (width, height), color=(95, 110, 80))
    draw = ImageDraw.Draw(img)

    # Draw simulated water creek / hazard barrier
    draw.polygon([(200, 0), (280, 0), (380, 720), (300, 720)], fill=(45, 75, 105))

    # Draw simulated rock clusters / elevation contour patches
    draw.ellipse([500, 150, 750, 320], fill=(130, 125, 110), outline=(100, 95, 80))
    draw.ellipse([800, 400, 1100, 620], fill=(120, 115, 100), outline=(90, 85, 70))

    # Draw simulated isolated human targets (high contrast rescue jacket color: safety orange)
    # Target 1: stranded near water barrier (x=330, y=280)
    draw.rectangle([325, 275, 345, 315], fill=(240, 90, 30), outline=(30, 30, 30))
    draw.ellipse([328, 265, 342, 278], fill=(220, 180, 150))

    # Target 2: stranded near rock cluster (x=620, y=230)
    draw.rectangle([615, 225, 635, 265], fill=(230, 50, 40), outline=(30, 30, 30))
    draw.ellipse([618, 215, 632, 228], fill=(210, 170, 140))

    img.save(target_path, "JPEG", quality=90)
    print(f"Created reference aerial test image: {target_path} ({width}x{height})")
    return target_path


if __name__ == "__main__":
    create_reference_aerial_image()
