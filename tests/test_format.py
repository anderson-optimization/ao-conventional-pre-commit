import re

import pytest

from ao_conventional_pre_commit import format

CUSTOM_TYPES = ["one", "two"]


def test_r_types():
    result = format.r_types(CUSTOM_TYPES)
    regex = re.compile(result)

    assert regex.match("one")
    assert regex.match("two")


def test_r_scope__optional():
    result = format.r_scope()
    regex = re.compile(result)

    assert regex.match("")


def test_r_scope__not_optional():
    result = format.r_scope(optional=False)
    regex = re.compile(result)

    # Assert not optional anymore
    assert not regex.match("")


def test_r_scope__parenthesis_required():
    result = format.r_scope()
    regex = re.compile(result)

    # without parens produces a match object with a 0 span
    # since the (scope) is optional
    without_parens = regex.match("something")
    assert without_parens.span() == (0, 0)

    # with parens produces a match object with a span
    # that covers the input string
    with_parens = regex.match("(something)")
    assert with_parens.span() == (0, 11)


def test_r_scope__alphanumeric():
    result = format.r_scope()
    regex = re.compile(result)

    assert regex.match("(50m3t41N6)")


def test_r_scope__special_chars():
    result = format.r_scope()
    regex = re.compile(result)

    assert regex.match("(some-thing)")
    assert regex.match("(some_thing)")
    assert regex.match("(some/thing)")
    assert regex.match("(some thing)")
    assert regex.match("(some:thing)")


def test_r_delim():
    result = format.r_delim()
    regex = re.compile(result)

    assert regex.match(":")


def test_r_delim__optional_breaking_indicator():
    result = format.r_delim()
    regex = re.compile(result)

    assert regex.match("!:")


def test_r_ticket():
    result = format.r_ticket()
    regex = re.compile(result)

    assert not regex.match("DTCT-99:")
    assert not regex.match("DTCT-99")
    assert regex.match(" DTCT-99")
    assert regex.match(" DTCT-99:")


def test_r_subject__starts_with_space():
    result = format.r_subject()
    regex = re.compile(result)

    assert not regex.match("something")
    assert regex.match(" something")


def test_r_subject__alphanumeric():
    result = format.r_subject()
    regex = re.compile(result)

    assert regex.match(" 50m3t41N6")


def test_r_subject__special_chars():
    result = format.r_subject()
    regex = re.compile(result)

    assert regex.match(" some-thing")
    assert regex.match(" some_thing")
    assert regex.match(" some/thing")
    assert regex.match(" some thing")


def test_r_autosquash_prefixes():
    result = format.r_autosquash_prefixes()
    regex = re.compile(result)

    for prefix in format.AUTOSQUASH_PREFIXES:
        assert regex.match(prefix)


def test_conventional_types__default():
    result = format.conventional_types()

    assert result == format.CONVENTIONAL_TYPES


def test_conventional_types__custom():
    result = format.conventional_types(["custom"])

    assert set(["custom", *format.CONVENTIONAL_TYPES]) == set(result)


@pytest.mark.parametrize("type", format.DEFAULT_TYPES)
def test_is_conventional__default_type(type):
    input = f"{type}: DTCT-99: message"

    assert format.is_conventional(input)


@pytest.mark.parametrize("type", format.CONVENTIONAL_TYPES)
def test_is_conventional__conventional_type(type):
    input = f"{type}: DTCT-99: message"

    assert format.is_conventional(input)


@pytest.mark.parametrize("type", CUSTOM_TYPES)
def test_is_conventional__custom_type(type):
    input = f"{type}: DTCT-99: message"

    assert format.is_conventional(input, CUSTOM_TYPES)


@pytest.mark.parametrize("type", format.CONVENTIONAL_TYPES)
def test_is_conventional__conventional_custom_type(type):
    input = f"{type}: DTCT-99: message"

    assert format.is_conventional(input, CUSTOM_TYPES)


def test_is_conventional__breaking_change():
    input = "fix!: DTCT-99: message"

    assert format.is_conventional(input)


def test_is_conventional__with_scope():
    input = "feat(scope): DTCT-99: message"

    assert format.is_conventional(input)


def test_is_conventional__body_multiline_body_bad_type():
    input = """wrong: DTCT-99: message

    more_message
    """

    assert not format.is_conventional(input)


def test_is_conventional__bad_body_multiline():
    input = """feat(scope): DTCT-99: message
    more message
    """

    assert not format.is_conventional(input)


def test_is_conventional__body_multiline():
    input = """feat(scope): DTCT-99: message

    more message
    """

    assert format.is_conventional(input)


def test_is_conventional__bad_body_multiline_paragraphs():
    input = """feat(scope): DTCT-99: message
    more message

    more body message
    """

    assert not format.is_conventional(input)


@pytest.mark.parametrize("char", ['"', "'", "`", "#", "&"])
def test_is_conventional__body_special_char(char):
    input = f"feat: DTCT-99: message with {char}"

    assert format.is_conventional(input)


def test_is_conventional__wrong_type():
    input = "wrong: DTCT-99: message"

    assert not format.is_conventional(input)


def test_is_conventional__scope_special_chars():
    input = "feat(%&*@()): DTCT-99: message"

    assert not format.is_conventional(input)


def test_is_conventional__space_scope():
    input = "feat (scope): DTCT-99: message"

    assert not format.is_conventional(input)


def test_is_conventional__scope_space():
    input = "feat(scope) : DTCT-99: message"

    assert not format.is_conventional(input)


def test_is_conventional__no_ticket_space():
    input = "feat(scope):DTCT-99: message"

    assert not format.is_conventional(input)


def test_is_conventional__scope_not_optional():
    input = "feat: DTCT-99: message"

    assert not format.is_conventional(input, optional_scope=False)


def test_is_conventional__scope_not_optional_empty_parenthesis():
    input = "feat(): DTCT-99: message"

    assert not format.is_conventional(input, optional_scope=False)


def test_is_conventional__missing_delimiter():
    input = "feat DTCT-99: message"

    assert not format.is_conventional(input)


def test_is_conventional__missing_ticket():
    input = "feat: message"

    assert not format.is_conventional(input)


def test_is_conventional__optional_ticket():
    input = "feat: message"

    assert format.is_conventional(input, optional_ticket=True)


def test_is_conventional__missing_colon():
    input = "feat: DTCT-99 message"

    assert format.is_conventional(input)


def test_is_conventional__missing_colon_not_optional_colon():
    input = "feat: DTCT-99 message"

    assert not format.is_conventional(input, optional_colon_after_ticket=False)


@pytest.mark.parametrize(
    "input,has_prefix",
    [
        ("amend! ", True),
        ("fixup! ", True),
        ("squash! ", True),
        ("squash! whatever .. $12 #", True),
        ("squash!", False),
        (" squash! ", False),
        ("squash!:", False),
        ("feat(foo):", False),
    ],
)
def test_has_autosquash_prefix(input, has_prefix):
    assert format.has_autosquash_prefix(input) == has_prefix
