import os
from django.core.exceptions import ValidationError

def validate_file_extension(file):
    ext = os.path.splitext(file.name)[1]
    valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Unsupported file extension.')