# Test the mkdocs_handler.py module


import rimscode_website.mkdocs_handler as mkd


def test_write_mkdocs_conf(tmp_path, mocker):
    """Test the _write_mkdocs_conf function to create the same file as before."""
    # copy mkdocs.yml file from repo to temporary tmp_conf file
    tmp_yml_orig = tmp_path.joinpath("mkdocs_orig.yml")
    tmp_yml_orig.write_text(
        """nav:
- Home: index.md
- Schemes:
  - Periodic Table: schemes.md
  - Elements:
    - Zr:
      - Overview: zr/index.md
      - Zr-1: zr/zr-1.md
    - Ba:
      - Overview: ba/index.md
      - Ba-1: ba/ba-1.md
      - Ba-2: ba/ba-2.md
- Contribute: contribute.md
"""
    )

    tmp_yml = tmp_path.joinpath("mkdocs.yml")
    tmp_yml.write_text(tmp_yml_orig.read_text())

    # mock the REPO_PATH to the temporary path
    mocker.patch("rimscode_website.mkdocs_handler.REPO_PATH", tmp_path)

    # get the settings out of the mkdocs.yml file
    tmp_conf = mkd._load_mkdocs_conf()

    # get the settings configuration
    idx = None
    for ind, entry in enumerate(tmp_conf["nav"]):
        if "Schemes" in entry.keys():
            idx = ind
            break

    settings_dict = tmp_conf["nav"][idx]

    # write the settings file to the temporary file
    mkd._write_mkdocs_conf(settings_dict)

    # compare the two files
    assert tmp_yml.read_text() == tmp_yml_orig.read_text()
