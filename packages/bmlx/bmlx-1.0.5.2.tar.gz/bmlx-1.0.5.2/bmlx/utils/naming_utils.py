import re

# ^(?![0-9]+$)(?!-)[a-zA-Z0-9-]{,63}(?<!-)$ is for normal checking
# notice that we changed 63->30, because some component like volcano
# would add some suffix to name, so ,we limit pipeline with shorter length
_NAMING_RE = re.compile(r"^(?![0-9]+$)(?!-)[a-zA-Z0-9-]{,30}(?<!-)$")


def is_name_valid(name):
    global _NAMING_RE
    return _NAMING_RE.match(name)
