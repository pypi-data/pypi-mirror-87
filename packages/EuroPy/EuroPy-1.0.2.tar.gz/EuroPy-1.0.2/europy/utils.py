def isnotebook():
    try:
        shell = get_ipython()
        return True
    except NameError:
        return False