from os.path import normpath

from app import Search


errorlog = normpath("c:/users/foxma/pycharmprojects/avantiattachments/results/manual_fix_required.txt")

def test_rev_in_filename_regex_picks_rev():
    assert Search.find_rev("11371-93991111-Rev.C.pdf", errorlog) == "C"
    assert Search.find_rev("16420_SP93-1271_REVA1.pdf", errorlog) == "A1"
    assert Search.find_rev("11371-93991111-Rev. C.pdf", errorlog) == "C"
    assert Search.find_rev("11371-93991111-Rev C.pdf", errorlog) == "C"
    assert Search.find_rev("11371-93991111-Rev-C.pdf", errorlog) == "C"
    assert Search.find_rev("11371-93991111-rev-C1.pdf", errorlog) == "C1"
    assert Search.find_rev("11371-93991111-rev-OBS.pdf", errorlog) == "OBS"
    assert Search.find_rev("11371-93991111-rev-00C.pdf", errorlog) == "00C"
    assert Search.find_rev("0051-72664_001_REV_2 (99T0244 CUSTOMER PRINT).pdf", errorlog) == "2"
    assert Search.find_rev("ECO 19711_DNC-107_REVA_Page_4N.jpg", errorlog) == "A"


def test_rev_in_filename_regex_excludes_no_rev():
    assert Search.find_rev("11371-93991111-Rev.pdf", errorlog) is None
    assert Search.find_rev("11371-93991111-Rev.xls", errorlog) is None
    assert Search.find_rev("11371-93991111-Rev.png", errorlog) is None
    assert Search.find_rev("11371-93991111-rev. .pdf", errorlog) is None
    assert Search.find_rev("11371-93991111-rev..pdf", errorlog) is None


def test_find_rev_excludes_words_with_rev():
    assert Search.find_rev("To Do - ECO 21643 - Please review two new...pdf", errorlog) is None
    assert Search.find_rev("99R1336-Vessel revised.PDF", errorlog) is None
    assert Search.find_rev("EMAIL- ECP 21098, Revision - Form F82419-Rev.pdf", errorlog) is None


def test_find_rev_fails_if_two_revs():
    assert Search.find_rev("0051-72664_001_REV_2 (99T0244 REV B CUSTOMER PRINT).pdf", errorlog) is None
