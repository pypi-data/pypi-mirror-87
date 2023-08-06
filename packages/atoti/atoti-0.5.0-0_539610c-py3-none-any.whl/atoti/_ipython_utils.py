from typing import Any, Mapping, Sequence


def ipython_key_completions_for_mapping(mapping: Mapping[str, Any]) -> Sequence[str]:
    """Return IPython key completions for mapping."""
    return list(mapping.keys())


def run_from_ipython():
    """Test if the current session is being run from IPython."""
    try:

        # pylint: disable = pointless-statement
        __IPYTHON__  # type: ignore
        return True
    except NameError:
        return False
