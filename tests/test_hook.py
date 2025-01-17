import subprocess

import pytest

from ao_conventional_pre_commit.hook import RESULT_FAIL, RESULT_SUCCESS, main


@pytest.fixture
def cmd():
    return "ao-conventional-pre-commit"


def test_main_fail__missing_args():
    result = main()

    assert result == RESULT_FAIL


def test_main_fail__bad(bad_commit_path):
    result = main([bad_commit_path])

    assert result == RESULT_FAIL


def test_main_fail__custom(bad_commit_path):
    result = main(["custom", bad_commit_path])

    assert result == RESULT_FAIL


def test_main_success__conventional(conventional_commit_path):
    result = main([conventional_commit_path])

    assert result == RESULT_SUCCESS


def test_main_success__custom(custom_commit_path):
    result = main(["custom", custom_commit_path])

    assert result == RESULT_SUCCESS


def test_main_success__custom_conventional(conventional_commit_path):
    result = main(["custom", conventional_commit_path])

    assert result == RESULT_SUCCESS


def test_main_success__conventional_utf8(conventional_utf8_commit_path):
    result = main([conventional_utf8_commit_path])

    assert result == RESULT_SUCCESS


def test_main_fail__conventional_gbk(conventional_gbk_commit_path):
    result = main([conventional_gbk_commit_path])

    assert result == RESULT_FAIL


def test_main_fail__conventional_with_scope(conventional_commit_path):
    result = main(["--force-scope", conventional_commit_path])

    assert result == RESULT_FAIL


def test_main_success__conventional_with_scope(cmd, conventional_commit_with_scope_path):
    result = main(["--force-scope", conventional_commit_with_scope_path])

    assert result == RESULT_SUCCESS


def test_main_success__fixup_commit(fixup_commit_path):
    result = main([fixup_commit_path])

    assert result == RESULT_SUCCESS


def test_main_fail__fixup_commit(fixup_commit_path):
    result = main(["--strict", fixup_commit_path])

    assert result == RESULT_FAIL


def test_main_success__conventional_commit_multi_line(conventional_commit_multi_line_path):
    result = main([conventional_commit_multi_line_path])

    assert result == RESULT_SUCCESS


def test_main_fail__conventional_commit_bad_multi_line(conventional_commit_bad_multi_line_path):
    result = main([conventional_commit_bad_multi_line_path])

    assert result == RESULT_FAIL


def test_main_fail__conventional_commit_no_ticket(conventional_commit_bad_missing_ticket_path):
    result = main([conventional_commit_bad_missing_ticket_path])

    assert result == RESULT_FAIL


def test_main_success__conventional_commit_no_ticket(conventional_commit_bad_missing_ticket_path):
    result = main(["--optional-ticket", conventional_commit_bad_missing_ticket_path])

    assert result == RESULT_SUCCESS


def test_main_success__conventional_commit_optional_colon(conventional_commit_optional_colon_path):
    result = main([conventional_commit_optional_colon_path])

    assert result == RESULT_SUCCESS


def test_main_fail__conventional_commit_optional_colon_force_colon(conventional_commit_optional_colon_path):
    result = main(["--force-colon-after-ticket", conventional_commit_optional_colon_path])

    assert result == RESULT_FAIL


def test_subprocess_fail__missing_args(cmd):
    result = subprocess.call(cmd)

    assert result == RESULT_FAIL


def test_subprocess_fail__bad(cmd, bad_commit_path):
    result = subprocess.call((cmd, bad_commit_path))

    assert result == RESULT_FAIL


def test_subprocess_fail__custom(cmd, bad_commit_path):
    result = subprocess.call((cmd, "custom", bad_commit_path))

    assert result == RESULT_FAIL


def test_subprocess_success__conventional(cmd, conventional_commit_path):
    result = subprocess.call((cmd, conventional_commit_path))

    assert result == RESULT_SUCCESS


def test_subprocess_success__custom(cmd, custom_commit_path):
    result = subprocess.call((cmd, "custom", custom_commit_path))

    assert result == RESULT_SUCCESS


def test_subprocess_success__custom_conventional(cmd, conventional_commit_path):
    result = subprocess.call((cmd, "custom", conventional_commit_path))

    assert result == RESULT_SUCCESS


def test_subprocess_fail__conventional_with_scope(cmd, conventional_commit_path):
    result = subprocess.call((cmd, "--force-scope", conventional_commit_path))

    assert result == RESULT_FAIL


def test_subprocess_success__conventional_with_scope(cmd, conventional_commit_with_scope_path):
    result = subprocess.call((cmd, "--force-scope", conventional_commit_with_scope_path))

    assert result == RESULT_SUCCESS


def test_subprocess_success__fixup_commit(cmd, fixup_commit_path):
    result = subprocess.call((cmd, fixup_commit_path))

    assert result == RESULT_SUCCESS


def test_subprocess_fail__fixup_commit(cmd, fixup_commit_path):
    result = subprocess.call((cmd, "--strict", fixup_commit_path))

    assert result == RESULT_FAIL


def test_subprocess_success__conventional_commit_multi_line(cmd, conventional_commit_multi_line_path):
    result = subprocess.call((cmd, conventional_commit_multi_line_path))

    assert result == RESULT_SUCCESS


def test_subprocess_fail__conventional_commit_bad_multi_line(cmd, conventional_commit_bad_multi_line_path):
    result = subprocess.call((cmd, conventional_commit_bad_multi_line_path))

    assert result == RESULT_FAIL


def test_subprocess_fail__conventional_commit_no_ticket(cmd, conventional_commit_bad_missing_ticket_path):
    result = subprocess.call((cmd, conventional_commit_bad_missing_ticket_path))

    assert result == RESULT_FAIL


def test_subprocess_success__conventional_commit_no_ticket(cmd, conventional_commit_bad_missing_ticket_path):
    result = subprocess.call((cmd, "--optional-ticket", conventional_commit_bad_missing_ticket_path))

    assert result == RESULT_SUCCESS


def test_subprocess_success__conventional_commit_optional_colon(cmd, conventional_commit_optional_colon_path):
    result = subprocess.call((cmd, conventional_commit_optional_colon_path))

    assert result == RESULT_SUCCESS


def test_subprocess_fail__conventional_commit_optional_colon_force_colon(cmd, conventional_commit_optional_colon_path):
    result = subprocess.call((cmd, "--force-colon-after-ticket", conventional_commit_optional_colon_path))

    assert result == RESULT_FAIL
