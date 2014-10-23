__author__ = 'foxma'

from app import partnumber


def test_rev_in_filename_regex_picks_rev():
    assert partnumber.rev_in_filename_regex("11371-93991111-Rev.C.pdf") == "C"
    assert partnumber.rev_in_filename_regex("16420_SP93-1271_REVA1.pdf") == "A1"
    assert partnumber.rev_in_filename_regex("11371-93991111-Rev. C.pdf") == "C"
    assert partnumber.rev_in_filename_regex("11371-93991111-Rev C.pdf") == "C"
    assert partnumber.rev_in_filename_regex("11371-93991111-Rev-C.pdf") == "C"
    assert partnumber.rev_in_filename_regex("11371-93991111-rev-C1.pdf") == "C1"
    assert partnumber.rev_in_filename_regex("11371-93991111-rev-OBS.pdf") == "OBS"
    assert partnumber.rev_in_filename_regex("11371-93991111-rev-00C.pdf") == "00C"


def test_rev_in_filename_regex_excludes_no_rev():
    assert partnumber.rev_in_filename_regex("11371-93991111-Rev.pdf") is None
    assert partnumber.rev_in_filename_regex("11371-93991111-Rev.xls") is None
    assert partnumber.rev_in_filename_regex("11371-93991111-Rev.png") is None
    assert partnumber.rev_in_filename_regex("11371-93991111-rev. .pdf") is None
    assert partnumber.rev_in_filename_regex("11371-93991111-rev..pdf") is None
