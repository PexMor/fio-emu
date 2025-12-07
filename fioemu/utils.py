"""Utility functions for FIO emulator."""
import pathlib
from typing import Optional


def load_example_response(
    api_id: str,
    number: int,
    format: str,
    examples_dir: pathlib.Path,
) -> Optional[str]:
    """
    Load an example response from the examples directory.

    Args:
        api_id: The API endpoint identifier (e.g., 'periods', 'by_id')
        number: The example number
        format: The response format (e.g., 'xml', 'json')
        examples_dir: The examples directory path

    Returns:
        The file contents as a string, or None if not found
    """
    example_file = examples_dir / api_id / f"{api_id}_{number}.{format}"

    if not example_file.exists():
        return None

    try:
        with open(example_file, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return None

