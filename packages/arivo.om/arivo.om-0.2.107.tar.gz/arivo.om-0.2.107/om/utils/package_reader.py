import glob
import json
import logging
import os
from io import StringIO

import yaml
from dotenv import dotenv_values


def _prepare_env_dict(env_dict, package, filename=""):
    # add file for convenience
    env_dict["filename"] = filename
    # always add package name (folder) because env.NAME != dirname
    env_dict["package"] = package
    return env_dict


def _prepare_hw_env_dict(env_dict):
    try:
        env_dict["HARDWARE_TYPE"] = json.loads(env_dict["HARDWARE_TYPE"])
    except:
        pass
    return env_dict


def load_env(path):
    package_folder = os.path.basename(os.path.dirname(path))
    env_dict = dotenv_values(path)
    return _prepare_env_dict(env_dict, package_folder, path)


def load_yml(filename, yml_loader=None):
    # yaml loader may be necessary for example if somebody else tries to load an yml with a rates matrix
    if yml_loader is None:
        yml_loader = yaml.FullLoader
    if os.path.exists(filename):
        try:
            with open(filename) as f:
                return yaml.load(f, Loader=yml_loader)
        except:
            logging.error("Failed to load yml file " + filename)
    return {}


def load_env_content(env, package="", filename=""):
    stream = StringIO(env)
    env_dict = dotenv_values(stream=stream)
    return _prepare_env_dict(env_dict, package, filename)


def load_yml_content(yml, yml_loader=None):
    if yml_loader is None:
        yml_loader = yaml.FullLoader
    try:
        stream = StringIO(yml)
        content = yaml.load(stream, Loader=yml_loader)
        return ({} if content is None else content)

    except:
        logging.error("Failed to load yml content", extra={"content": yml})
    return {}


def load_hw_env(path):
    env_dict = load_env(path)
    return _prepare_hw_env_dict(env_dict)


def load_hw_env_content(env, package, filename=""):
    env_dict = load_env_content(env, package=package, filename=filename)
    return _prepare_hw_env_dict(env_dict)


def get_package_folders(prefix="", package_dir="/opt/openmodule/dist2/"):
    """get package folders with prefix
    Args:
        prefix (str): prefix to match, e.g. "om-" for all openmodule packages
        package_dir (str): path to directory containing the packages aka dist2 path
    Returns:
        list of directories of the matching hardware packages
    """
    all_dirs = sorted(glob.glob(os.path.join(package_dir, "{}*".format(prefix))))
    return [d for d in all_dirs
            if os.path.isdir(d) and os.path.exists(os.path.join(d, "env")) and os.path.exists(os.path.join(d, "yml"))]


def get_hw_packages(type, package_dir="/opt/openmodule/dist2/"):
    """get hardware packages matching type (matches specified number of '-' separated blocks), so it's possible to match as specific as necessary

    Args:
        type (str): prefix to match, e.g. "io" for all io packages or "cam-ip-avigilon" for all avigilon cameras
        package_dir (str): path to directory containing the hardware packages
    Returns:
        list of directories of the matching hardware packages
    """
    all_dirs = get_package_folders("hw-", package_dir=package_dir)
    matching_dirs = []
    type_split = type.split('-')
    for d in all_dirs:
        env = os.path.join(d, "env")
        try:
            env_dict = load_hw_env(env)
            for hw_type in env_dict.get("HARDWARE_TYPE", []):
                if type_split == hw_type.split('-')[:len(type_split)]:
                    matching_dirs.append(d)
                    break
        except Exception as e:
            logging.error("Unexpected error while loading hardware env file " + env)
    return matching_dirs


def get_hw_settings(type, package_dir="/opt/openmodule/dist2/"):
    """get settings of the hardware packages prefix-matching type

    Args:
        type (str): prefix to match, e.g. "io" for all io packages or "cam-ip-avigilon" for all avigilon cameras
        package_dir (str): path to directory containing the hardware packages
    Returns:
        list of {"env": dict, "yml": [dict,list,None]}, where in "env" one can find the env variables as a dict and in
            "yml" one can find the yaml settings
    """
    hw_dirs = get_hw_packages(type, package_dir)
    hw_settings = []
    for d in hw_dirs:
        hw_settings.append(load_package_settings(d))
    return hw_settings


def load_package_settings_with_content(env, yml, package, filename="", env_loader=None, yml_loader=None):
    if env_loader is None:
        env_loader = load_hw_env_content
    if yml_loader is None:
        yml_loader = yaml.FullLoader
    settings = {"env": {}, "yml": {}}
    try:
        settings["env"] = env_loader(env, package, filename=filename)
    except:
        logging.error("Unexpected error while loading hardware env content " + env)
    try:
        settings["yml"] = yaml.load(yml, Loader=yml_loader)
    except:
        logging.error("Failed to load yml content " + yml)
    return settings


def load_package_settings(folder, env_loader=None, yml_loader=None):
    if env_loader is None:
        env_loader = load_hw_env
    env = os.path.join(folder, "env")
    yml = os.path.join(folder, "yml")
    settings = {"env": {}, "yml": {}}
    try:
        settings["env"] = env_loader(env)
    except:
        logging.error("Unexpected error while loading hardware env file " + env)
    settings["yml"] = load_yml(yml)
    return settings


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    print("1", get_hw_packages("io"))
    print("2", get_hw_settings("cam"))
    print("3", get_hw_settings("cam", "/tmp"))
    print("4", get_hw_packages("cam-ip-avigilo"))
    print("5", get_hw_packages("cam-ip-avigilon"))
    print("all packages", get_package_folders())
    print("hardware only", get_package_folders("hw-"))
    print("avigilon only", get_package_folders("hw-avigilon"))
