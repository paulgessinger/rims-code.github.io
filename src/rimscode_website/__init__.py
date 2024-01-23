# initialization file for rimscode_website package


from pathlib import Path

REPO_PATH = Path(__file__).parent.parent.parent

from .create_website import website  # noqa: E402

__all__ = ["REPO_PATH", "website"]
