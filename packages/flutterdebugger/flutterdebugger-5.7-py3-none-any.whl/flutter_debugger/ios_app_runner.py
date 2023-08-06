import tempfile
import os

APPS_FILE_REPO = "git@gitlab.ximalaya.com:flutter/flutterdebugapps.git"


def get_app_repo_local_path():
    clone_path = os.path.join(tempfile.gettempdir(), "appfiles_for_flutter")
    if not os.path.exists(clone_path):
        os.system("git clone {0} {1} > /dev/null".format(APPS_FILE_REPO, clone_path))
    else:
        os.system("cd {0} && git pull > /dev/null".format(clone_path))
    return clone_path


def fetch_app_file(app_name):
    clone_path = get_app_repo_local_path()
    app_file_path = os.path.join(clone_path, "{0}.app".format(app_name))
    if not os.path.exists(app_file_path):
        return None
    return app_file_path


def run_app(app_name):
    app_path = fetch_app_file(app_name)
    os.system(" ios-deploy --noinstall -L --bundle {0}".format(app_path))


def list_support_app():
    app_names = []
    clone_path = get_app_repo_local_path()
    if os.path.exists(clone_path):
        app_paths = os.listdir(clone_path)
        for app_path in app_paths:
            if app_path.endswith(".app"):
                app_names.append(app_path.split("/")[-1].split(".")[0])
    return app_names

