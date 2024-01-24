# Create all pages for elements available in the database

from pathlib import Path
from typing import Tuple, Union
import warnings

from rimscode_website import DB_PATH, DOCS_PATH
from rimscode_website.utils import ELEMENTS_BY_NAME


class ElementMD:
    """Class to handle the creation of the element markdown pages."""

    def __init__(self):
        """Initialize the class."""
        self.db_dict = None

        self._all_schemes = {}  # dictionary with all scheme: {ele: [ele-1, ele-2, ...]}
        self._ele_index_urls = {}  # dictionary with element name: url for adding to periodic table

        self._create_db_dict()

    @property
    def all_schemes(self) -> dict:
        """Return a dictionary with the all schemes per element.

        Example dictionary that could be returned:
        {"he": ["he-1", "he-2"], "as": ["as-1", "as-2", "as-3"]}

        :return: Dictionary with element name as key and list of schemes as value.
        """
        return self._all_schemes

    @property
    def ele_index_urls(self) -> dict:
        """Return a dictionary with the element index urls.

        While the URL is not complicated compared to the element, the important
        function of this dictionary is to keep track of which elements exist.
        URLs are simply pointing at the folder. Example return dictionary:
        {"he": "he/", "as": "as/"}

        :return: Dictionary with element name as key and url as value. See example.
        """
        return self._ele_index_urls

    def write_elements_md(self):
        """Create all pages for elements in the database."""
        self._create_ele_folders()
        self._create_ele_files()

    def _create_db_dict(self):
        """Create a dictionary with the database information.

        Keys for the dictionary are:
            "files" -> Path to the json file.
            "elements" -> Element name.
            "positions" -> Position of the element in the list of elements.
        """
        db_files_in = DB_PATH.glob("*.json")

        db_dict = {"files": [], "elements": [], "positions": []}
        for f in db_files_in:
            # parse the file name
            ele_pos = _parse_fname(f)
            if ele_pos is not None:
                db_dict["files"].append(f)
                db_dict["elements"].append(ele_pos[0])
                db_dict["positions"].append(ele_pos[1])

        self.db_dict = db_dict

    def _create_ele_folders(self):
        """Create empty folders for each element in the database.

        :param eles: List of elements in the database. Can contain duplicates.
        """
        eles = self.db_dict["elements"]
        for ele in set(eles):
            folder = Path(DOCS_PATH.joinpath(ele))
            folder.mkdir(exist_ok=True)

            # empty the folders of all files
            for f in folder.glob("*"):
                f.unlink()

    def _create_ele_files(self) -> None:
        """Create all the markdown pages for the elements in the database."""
        db_dict = self.db_dict

        for fl, ele, pos in zip(
            db_dict["files"], db_dict["elements"], db_dict["positions"]
        ):
            folder = Path(DOCS_PATH.joinpath(ele))

            # scheme files
            fname = folder.joinpath(f"{ele}-{pos}.md")
            with open(fname, "w") as f:
                f.write(self._create_ele_file_content(fl))

            # add element and scheme to the all_schemes dictionary
            dict_entry = f"{ele}/{fname.stem}"
            if ele not in self._all_schemes.keys():
                self._all_schemes[ele] = [dict_entry]
            else:
                self._all_schemes[ele].append(dict_entry)

        # index file
        for ele in set(db_dict["elements"]):
            folder = Path(DOCS_PATH.joinpath(ele))
            fname = folder.joinpath("index.md")
            with open(fname, "w") as f:
                f.write(self._create_ele_index_content(ele))

            # add url to self to the url dictionary
            self._ele_index_urls[ele] = f"{ele}/"

    @staticmethod
    def _create_ele_file_content(fl: Path) -> str:
        """Create the content of the element markdown file.

        :param fl: Path to the json file.

        :return: String with the content of the markdown file.
        """
        # todo: parse the json file and create the content
        ele, pos = _parse_fname(fl)
        ret = f"# {ele.capitalize()} scheme {pos}"
        return ret

    def _create_ele_index_content(self, ele) -> str:
        """Create the index file for all the elements in the database.

        :param ele: Element name (all lowercase).

        :return: String with the content of the index markdown file.
        """
        db_dict = self.db_dict

        ret = f"# Schemes for {ele.capitalize()}\n\n"

        # get sorted positions list for this element from dictionary
        positions = sorted(
            [
                pos
                for pos, e in zip(db_dict["positions"], db_dict["elements"])
                if e == ele
            ]
        )

        # create a relative URL for each file
        urls = [f"../{ele}/{ele}-{pos}.md" for pos in positions]

        # create a bullet point list of links to the schemes
        ret += "\n".join(
            [
                f"* [{ele.capitalize()} scheme {pos}]({url})"
                for pos, url in zip(positions, urls)
            ]
        )

        return ret


def _parse_fname(fname: Path) -> Union[Tuple[str, int], None]:
    """Parse the filename and return the element name and the position.

    :param fname: Path to the file to parse.

    :return: Tuple with element name (all lowercase) and position or
        None if the file name is invalid.
    """
    try:
        ele, pos = fname.stem.split("-")
        pos = int(pos)
    except ValueError:  # file name cannot be unpacked
        warnings.warn(
            f"Invalid database file name {fname.stem}.", UserWarning, stacklevel=2
        )
        return None

    # check if element name is valid
    valid_elements = set(k.casefold() for k in ELEMENTS_BY_NAME.keys())
    if ele.casefold() not in valid_elements:
        warnings.warn(
            f"Invalid element name in database file {fname.stem}.",
            UserWarning,
            stacklevel=2,
        )
        return None

    return ele.lower(), pos


if __name__ == "__main__":
    writer = ElementMD()
    writer.write_elements_md()
