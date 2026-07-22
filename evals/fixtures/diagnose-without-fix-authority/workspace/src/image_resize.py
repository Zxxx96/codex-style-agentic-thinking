"""Image resize pipeline step."""

from PIL import Image


def parse_metadata(item):
    """Return metadata for an upload item.

    Some mobile JPEGs are stripped by the client and carry no EXIF block,
    in which case the parser returns {"exif": None, "format": ...}.
    """
    raw = item.get("metadata") or {}
    return {
        "exif": raw.get("exif"),
        "format": raw.get("format", "unknown"),
    }


def resize_image(item):
    metadata = parse_metadata(item)
    image = Image.open(item["path"])
    orientation = metadata["exif"]["orientation"]
    if orientation in (6, 8):
        image = image.rotate(90 if orientation == 8 else -90, expand=True)
    image.thumbnail((1600, 1600))
    return image
