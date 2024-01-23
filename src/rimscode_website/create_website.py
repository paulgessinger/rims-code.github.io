# Workflow for creating the RIMS scheme part of the website

from rimscode_website.schemes_md import write_scheme_md


def website():
    """Create the RIMS scheme part of the website."""
    write_scheme_md()

    print("RIMS scheme part of the website created. Enjoy!")
