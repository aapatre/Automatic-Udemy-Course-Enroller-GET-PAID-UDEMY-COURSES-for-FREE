import os


def get_app_dir() -> str:
    """
    Gets the app directory where all data related to the script is stored

    :return:
    """
    app_dir = os.path.join(os.path.expanduser("~"), ".udemy_enroller")

    if not os.path.isdir(app_dir):
        # If the app data dir does not exist create it
        os.mkdir(app_dir)
    return app_dir
