"""
Utility functions for the application.
"""
import asyncio
import os
import re
import uuid

from fastapi import UploadFile
from pathvalidate import sanitize_filename


def sanitize_file(filename: str) -> str:
    """
    Make a filename safe for storage using pathvalidate; add uuid suffix.
    """
    uuid_suffix = uuid.uuid4().hex[:8]
    filename_without_extension = os.path.splitext(filename)[0]
    extension = os.path.splitext(filename)[1]
    filename_without_extension = filename_without_extension.strip()
    extension = extension.strip()
    filename_without_extension = re.sub(r"_+", "_", sanitize_filename(filename_without_extension))
    filename_without_extension = filename_without_extension.strip("._ ")
    if not filename_without_extension:
        filename_without_extension = "unnamed"
    return f"{filename_without_extension}_{uuid_suffix}{extension}".encode("utf-8").decode("utf-8")


async def save_file(file: UploadFile, dest_dir: str) -> str:
    """
    Save a file to the filesystem (async I/O via thread pool). Uses sanitized filename.
    """
    safe_name = sanitize_file(file.filename or "unnamed")
    file_content = await file.read()
    dest_path = os.path.join(dest_dir, safe_name)

    def _write() -> None:
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        with open(dest_path, "wb") as f:
            f.write(file_content)

    await asyncio.to_thread(_write)