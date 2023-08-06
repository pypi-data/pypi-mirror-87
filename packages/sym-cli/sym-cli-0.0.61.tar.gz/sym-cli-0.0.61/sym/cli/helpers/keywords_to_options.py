from typing import List, Mapping, Sequence, Union

Options = Mapping[str, Union[str, bool]]
Argument = Union[str, Options]


def keywords_to_options(args: Sequence[Argument]) -> List[str]:
    """
    Converts any dicts in the given arguments into a sequence of
    options. The keys correspond to option names (with underscores
    replaced with hyphens). String values correspond to option
    arguments; boolean values correspond to the presence or
    absence of the option, with no argument.
    """

    result = []
    for arg in args:
        if isinstance(arg, str):
            result.append(arg)
            continue
        if arg is None:
            continue
        if isinstance(arg, list):
            result.extend(keywords_to_options(arg))
            continue
        for (key, value) in arg.items():
            if value in (False, None):
                continue
            prefix = "-" if len(key) == 1 else "--"
            option = prefix + key.replace("_", "-")
            if not isinstance(value, (tuple, list)):
                value = [value]
            for val in value:
                result.append(option)
                if isinstance(val, str):
                    result.append(val)
    return result
