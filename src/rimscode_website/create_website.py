# Workflow for creating the RIMS scheme part of the website

from rimscode_website.elements_md import ElementMD
from rimscode_website.mkdocs_handler import navigation
from rimscode_website.schemes_md import write_scheme_md


def website():
    """Create the RIMS scheme part of the website."""
    element_writer = ElementMD()
    element_writer.write_elements_md()

    write_scheme_md(element_writer.ele_index_urls)

    navigation(element_writer.all_schemes)

    print("RIMS scheme part of the website created. Enjoy!")


if __name__ == "__main__":
    website()
