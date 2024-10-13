import os

from django.core.exceptions import ValidationError
from PIL import Image


def validate_staff_pic_size(image):
    if image:
        with Image.open(image) as img:
            if img.width > 70 or img.height > 70:
                raise ValidationError(f"That size might too big")
            
def validate_cccd_pic_size(image):
    if image:
        with Image.open(image) as img:
            if img.width > 120 or img.height > 180:
                raise ValidationError(f"CCCD image size is too big")
            
def validate_image_file_extension(value):
    ext = os.path.splitext(value.name) [1]
    valid_extensions = [".jpg", ".jpeg", ".png", ".img"]
    if not ext.lower() in valid_extensions:
        raise ValidationError("Unsupported, only accept JPG, JPEG, PNG, IMG files. Please choose another pic")