def format_bytes_list(bl):
    """Format any iterable of byte strings as a list for output.
    """
    return b'[%s]' % b', '.join(bl)
