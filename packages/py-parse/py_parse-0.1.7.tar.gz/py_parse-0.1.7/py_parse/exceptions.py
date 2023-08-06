class WrongHTMLFormatError(Exception):
    """
    Raises when something wrong with html markup. For example, when there are no tags, or closed tag (</tag>) goes
    without open this tag etc.
    """
    pass


class NoSuchElementError(Exception):
    """
    Raises when element was not found with current filter
    """
    pass


class NoRelativeError(Exception):
    """
    Raises when no such relative found
    """
    pass
