from os.path import normpath

from app.Search import *


def test_find_rev_regex_picks_rev():
    errorlog = normpath("c:/users/foxma/documents/github/avantiattachments/results/manual_fix_required.txt")
    assert find_rev("11371-93991111-Rev.C.pdf", errorlog) == "C"
    assert find_rev("16420_SP93-1271_REVA1.pdf", errorlog) == "A1"
    assert find_rev("11371-93991111-Rev. C.pdf", errorlog) == "C"
    assert find_rev("11371-93991111-Rev C.pdf", errorlog) == "C"
    assert find_rev("11371-93991111-Rev-C.pdf", errorlog) == "C"
    assert find_rev("11371-93991111-rev-C1.pdf", errorlog) == "C1"
    assert find_rev("11371-93991111-rev-OBS.pdf", errorlog) == "OBS"
    assert find_rev("11371-93991111-rev-00C.pdf", errorlog) == "00C"
    assert find_rev("0051-72664_001_REV_2 (99T0244 CUSTOMER PRINT).pdf", errorlog) == "2"
    assert find_rev("ECO 19711_DNC-107_REVA_Page_4N.jpg", errorlog) == "A"


def test_find_rev_regex_excludes_no_rev():
    errorlog = normpath("c:/users/foxma/documents/github/avantiattachments/results/manual_fix_required.txt")
    assert find_rev("11371-93991111-Rev.pdf", errorlog) is None
    assert find_rev("11371-93991111-Rev.xls", errorlog) is None
    assert find_rev("11371-93991111-Rev.png", errorlog) is None
    assert find_rev("11371-93991111-rev. .pdf", errorlog) is None
    assert find_rev("11371-93991111-rev..pdf", errorlog) is None


def test_find_rev_excludes_words_with_rev():
    errorlog = normpath("c:/users/foxma/documents/github/avantiattachments/results/manual_fix_required.txt")
    assert find_rev("To Do - ECO 21643 - Please review two new...pdf", errorlog) is None
    assert find_rev("99R1336-Vessel revised.PDF", errorlog) is None
    assert find_rev("EMAIL- ECP 21098, Revision - Form F82419-Rev.pdf", errorlog) is None


def test_find_rev_fails_if_two_revs():
    errorlog = normpath("c:/users/foxma/documents/github/avantiattachments/results/manual_fix_required.txt")
    assert find_rev("0051-72664_001_REV_2 (99T0244 REV B CUSTOMER PRINT).pdf", errorlog) is None


def test_split_rev_table_returns_lst():
    assert split_rev_table_data("100016209	00A	00C	12547") == ["100016209", "00A", "00C", "12547"]


def test_create_new_part_name():
    data = "100016209	00D	12748"
    assert create_new_part_name(data) == "100016209-REV-00D"


def test_iterate_over_list_create_objects():
    data = normpath("c:/users/foxma/documents/github/avantiattachments/indexes/sample_REVT.txt")
    path = normpath("c:/users/foxma/documents/github/avantiattachments/samples")
    errorlog = normpath("c:/users/foxma/documents/github/avantiattachments/results/manual_fix_required.txt")
    assert iterate_over_list_create_objects(data, path, errorlog) == "ECO-18832-100015940-RevD.pdf"
