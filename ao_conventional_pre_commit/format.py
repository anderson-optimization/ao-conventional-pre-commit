import re

CONVENTIONAL_TYPES = ["feat", "fix"]
DEFAULT_TYPES = [
    "build",
    "chore",
    "ci",
    "docs",
    "feat",
    "fix",
    "perf",
    "refactor",
    "revert",
    "style",
    "test",
]
AUTOSQUASH_PREFIXES = [
    "amend",
    "fixup",
    "squash",
]


def r_types(types):
    """Join types with pipe "|" to form regex ORs."""
    return "|".join(types)


def r_scope(optional=True):
    """Regex str for an optional (scope)."""
    if optional:
        return r"(\([\w \/:-]+\))?"
    else:
        return r"(\([\w \/:-]+\))"


def r_delim():
    """Regex str for optional breaking change indicator and colon delimiter."""
    return r"!?:"


def r_subject():
    """Regex str for subject line."""
    return r"\s+.+$"


def r_ticket(optional_ticket=False, optional_colon_after_ticket=True):
    """Regex str for a Jira ticket number with optional colon"""
    if optional_ticket:
        if optional_colon_after_ticket:
            return r"(\s+([A-Z]+-[0-9]+:?))?"
        else:
            return r"(\s+([A-Z]+-[0-9]+:))?"
    else:
        if optional_colon_after_ticket:
            return r"\s+([A-Z]+-[0-9]+:?)"
        else:
            return r"\s+([A-Z]+-[0-9]+:)"


def r_body():
    """Regex str for the body"""
    return r"(?P<multi>\r?\n(?P<sep>^$\r?\n)?.+)?"


def r_autosquash_prefixes():
    """Regex str for autosquash prefixes."""
    return "|".join(AUTOSQUASH_PREFIXES)


def conventional_types(types=[]):
    """Return a list of Conventional Commits types merged with the given types."""
    if set(types) & set(CONVENTIONAL_TYPES) == set():
        return CONVENTIONAL_TYPES + types
    return types


def is_conventional(input, types=DEFAULT_TYPES, optional_scope=True, optional_ticket=False, optional_colon_after_ticket=True):
    """
    Returns True if input matches AO Conventional Commits formatting
    https://www.conventionalcommits.org

    Optionally provide a list of additional custom types.
    """
    types = conventional_types(types)
    pattern = f"^({r_types(types)}){r_scope(optional_scope)}{r_delim()}{r_ticket(optional_ticket, optional_colon_after_ticket)}{r_subject()}{r_body()}"  # noqa: E501
    regex = re.compile(pattern, re.MULTILINE)

    result = regex.match(input)
    is_valid = bool(result)
    if is_valid and result.group("multi") and not result.group("sep"):
        is_valid = False

    return is_valid


def has_autosquash_prefix(input):
    """
    Returns True if input starts with one of the autosquash prefixes used in git.
    See the documentation, please https://git-scm.com/docs/git-rebase.

    It doesn't check whether the rest of the input matches Conventional Commits
    formatting.
    """
    pattern = f"^(({r_autosquash_prefixes()})! ).*$"
    regex = re.compile(pattern, re.DOTALL)

    return bool(regex.match(input))
