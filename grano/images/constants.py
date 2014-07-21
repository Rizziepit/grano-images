import mimetypes


ACCEPTED_EXTENSIONS = set(('.png', '.jpg', '.jpeg', '.bmp'))
ACCEPTED_MIMETYPES = set()
for ext in ACCEPTED_EXTENSIONS:
    ACCEPTED_MIMETYPES.add(mimetypes.types_map[ext])
    if ext in mimetypes.common_types:
        ACCEPTED_MIMETYPES.add(mimetypes.common_types[ext])
