_message_indent = 0


def _push_indent():
    global _message_indent
    _message_indent += 2


def _pop_indent():
    global _message_indent
    _message_indent -= 2


def debug(message: str):
    """
    Print a debug message to the moulinette's logs

    :param message:         the message to print
    """
    print(" " * _message_indent + message)
