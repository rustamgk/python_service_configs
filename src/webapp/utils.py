import typing

__all__ = (
    'is_entry_match',
)


def is_entry_match(entry, conditions):
    # type: (typing.Dict, typing.Dict) -> bool
    for needle, value in conditions.items():
        node = entry
        for part in needle.split('.'):
            node = node.get(part)
            if node is None:
                return False

        if node != value:
            return False

    return True
