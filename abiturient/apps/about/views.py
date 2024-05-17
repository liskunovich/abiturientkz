from abiturient import __version__


async def about__get_current_version():
    """
    Returns Application version
    """

    return {"version": __version__}
