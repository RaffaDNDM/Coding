def uniform_dir_path(directory):
    """
    Return directory path with '/' at the end

    Args:
        directory (str): directory path that you want to uniform

    Returns:
        directory (str): modified directory path that ends with '/'
    """

    if directory.endswith('/') or directory.endswith('\\'):
        return directory
    else:
        return directory+'/'