from typing import Dict, Iterable, List, Text

from bmlx.flow import Channel, Artifact


def as_channel(artifacts: Iterable[Artifact]) -> Channel:
    """Converts artifact collection of the same artifact type into a Channel.

    Args:
      artifacts: An iterable of Artifact.

    Returns:
      A static Channel containing the source artifact collection.

    Raises:
      ValueError when source is not a non-empty iterable of Artifact.
    """
    try:
        first_element = next(iter(artifacts))
        if isinstance(first_element, Artifact):
            return Channel(
                type_name=first_element.type_name, artifacts=artifacts
            )
        else:
            raise ValueError("Invalid artifact iterable: {}".format(artifacts))
    except StopIteration:
        raise ValueError("Cannot convert empty artifact iterable into Channel")


def unwrap_channel_dict(
    channel_dict: Dict[Text, Channel]
) -> Dict[Text, List[Artifact]]:
    """Unwrap dict of channels to dict of lists of Artifact.

    Args:
      channel_dict: a dict of Text -> Channel

    Returns:
      a dict of Text -> List[Artifact]
    """
    return dict((k, list(v.get())) for k, v in channel_dict.items())
