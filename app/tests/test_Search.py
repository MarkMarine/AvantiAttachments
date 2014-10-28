import app.search as search


def test_find_rev_regex_picks_rev():
    assert search.return_rev_from_file_name("11371-93991111-Rev.C.pdf") == "C"
    assert search.return_rev_from_file_name("16420_SP93-1271_REVA1.pdf") == "A1"
    assert search.return_rev_from_file_name("11371-93991111-Rev. C.pdf") == "C"
    assert search.return_rev_from_file_name("11371-93991111-Rev C.pdf") == "C"
    assert search.return_rev_from_file_name("11371-93991111-Rev-C.pdf") == "C"
    assert search.return_rev_from_file_name("11371-93991111-rev-C1.pdf") == "C1"
    assert search.return_rev_from_file_name("11371-93991111-rev-OBS.pdf") == "OBS"
    assert search.return_rev_from_file_name("11371-93991111-rev-00C.pdf") == "00C"
    assert search.return_rev_from_file_name("0051-72664_001_REV_2 (99T0244 CUSTOMER PRINT).pdf") == "2"
    assert search.return_rev_from_file_name("ECO 19711_DNC-107_REVA_Page_4N.jpg") == "A"


def test_find_rev_regex_excludes_no_rev():
    assert search.return_rev_from_file_name("11371-93991111-Rev.pdf") is None
    assert search.return_rev_from_file_name("11371-93991111-rev. .pdf") is None
    assert search.return_rev_from_file_name("11371-93991111-rev..pdf") is None


def test_find_rev_excludes_words_with_rev():
    assert search.return_rev_from_file_name("To Do - ECO 21643 - Please review two new...pdf") is None
    assert search.return_rev_from_file_name("99R1336-Vessel revised.PDF") is None
    assert search.return_rev_from_file_name("EMAIL- ECP 21098, Revision - Form F82419-Rev.pdf") is None


def test_find_rev_fails_if_two_revs():
    assert search.return_rev_from_file_name("0051-72664_001_REV_2 (99T0244 REV B CUSTOMER PRINT).pdf") is None


def test_split_rev_table_returns_lst():
    assert search.split_rev_table_data("100016209	00A	00C	12547") == ["100016209", "00A", "00C", "12547"]


def test_create_new_part_name():
    assert search.create_new_part_name("100016209	00D	12748") == "100016209-REV-00D"


def test_filter_zeros_from_rev():
    assert search.filter_zeros_from_rev("00A") == "A"
    assert search.filter_zeros_from_rev("0A1") == "A1"


def test_is_a_bom_redline():
    file_true1 = 'ECO 10884-BOM-100016209-RevA-Chges.pdf'
    file_true2 = 'ECO 10884_BOM_100016209-RevA-Chges.pdf'
    file_true3 = 'ECO 10884 BOM 100016209-RevA-Chges.pdf'
    file_false1 = 'ECO 10884BOM100016209-RevA-Chges.pdf'
    file_false2 = 'ECO 10884 BOMBPROOF 100016209-RevA-Chges.pdf'
    file_false3 = 'ECO 10884-BOMBPROOF-100016209-RevA-Chges.pdf'
    assert search.is_a_bom_redline(file_true1) == True
    assert search.is_a_bom_redline(file_true2) == True
    assert search.is_a_bom_redline(file_true3) == True
    assert search.is_a_bom_redline(file_false1) == False
    assert search.is_a_bom_redline(file_false2) == False
    assert search.is_a_bom_redline(file_false3) == False


def test_is_material_spec():
    assert search.is_material_spec("C:\\AVANTI\\ECP-ECO 2013\\19679\\NEW REVISIONS\\MS_100005039.pdf") == True
    assert search.is_material_spec("MS_100005039.pdf") == True
    assert search.is_material_spec("MS 100005039.pdf") == True
    assert search.is_material_spec("msa_100005039.pdf") == False
    assert search.is_material_spec(" msa_100005039.pdf") == False
    assert search.is_material_spec("ms1_100005039.pdf") == False
    assert search.is_material_spec("asdfms_100005039.pdf") == False
