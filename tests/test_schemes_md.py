# Tests for schemes_md.py file

from rimscode_website import schemes_md

import pytest


def test_all_colors():
    """Ensure that a set is returned with values and that all entries are strings."""
    ret_val = schemes_md._all_colors()
    assert isinstance(ret_val, set)
    for v in ret_val:
        assert isinstance(v, str)
    assert len(ret_val) > 0


@pytest.mark.parmetrize(
    "color, tag_name", [["#ffffc7", "tg_ffffc7"], ["ffe4bb", "tg_ffe4bb"]]
)
def test_table_style_tag_name():
    assert schemes_md._table_style_tag_name("#ffffc7") == "tg_ffffc7"
