# initialization file for rimscode_website package


from pathlib import Path

REPO_PATH = Path(__file__).parent.parent.parent
DB_PATH = REPO_PATH.joinpath("db")
DOCS_PATH = REPO_PATH.joinpath("docs")

from .create_website import website  # noqa: E402

__all__ = ["DB_PATH", "DOCS_PATH", "website"]
