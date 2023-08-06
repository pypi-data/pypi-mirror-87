"""This module implements SOIL's Command LIne Interface"""
import argparse
import sys
import os
import json
import getpass
import zipfile
from json import JSONDecodeError    # Flake8...
import subprocess   # nosec
import virtualenv   # type: ignore
import requests
import yaml

# pylint: disable=global-statement

env = dict()    # type: ignore
config = dict()

parser = argparse.ArgumentParser(prog='soil')
subparsers = parser.add_subparsers(dest='command')

configure_cmd = subparsers.add_parser('configure', help='Configure SOIL-CLI')
configure_cmd.add_argument('--reset', action='store_true', help="Reset the current configuration")

login_cmd = subparsers.add_parser('login', help='Login to configured soil instance')

init_cmd = subparsers.add_parser('init', help='Initialize a directory as a soil project')
init_cmd.add_argument('dirname', nargs='*', metavar='DIR', default='.',
                      help="Name of a directory to initialize as a soil app")

install_cmd = subparsers.add_parser('install', help='Installs the provided packages in the current soil project')
install_cmd.add_argument('packages', nargs='+', metavar='PACKAGE[S]', help="Package[s] to install")

run_cmd = subparsers.add_parser('run', help='Runs the provided module in the current soil project')
run_cmd.add_argument('chapter', metavar='chapter', help="Chapter in soil.yml (setup, data, migration, ...)")
run_cmd.add_argument('module', metavar='module', help="Module of chapter in soil.yml")
run_cmd.add_argument('module_args', nargs=argparse.REMAINDER, help="Arguments to be passed to the module")

test_cmd = subparsers.add_parser('test', help='Launches tests using SOIL. ')
test_cmd.add_argument('test_args', nargs=argparse.REMAINDER, help="Arguments to be passed to the test command")


def save_environment() -> None:
    """Saves the environment keys to a file, backing it up to prevent data loss."""

    global env  # pylint: disable=C0103
    os.rename(os.path.expanduser('~/.soil/soil.env'), os.path.expanduser('~/.soil/soil.env.bak'))
    env_file = open(os.path.expanduser('~/.soil/soil.env'), 'w')
    env_file.write(json.dumps(env, indent=4, sort_keys=True))
    env_file.close()
    os.remove(os.path.expanduser('~/.soil/soil.env.bak'))


def get_soil_root(relpath: str):    # type: ignore
    """Checks if the current dir is under a soil environment and returns its root. Returns None otherwise."""

    path = os.path.abspath(relpath) + '/'

    while path != "/":
        path, _ = os.path.split(path)
        if 'soil.yml' in os.listdir(path):
            return path

    return None


def soil_init() -> None:
    """Loads configuration and environment."""

    global env, config  # pylint: disable=C0103
    try:
        config_file = open(os.path.expanduser('~/.soil/soil.conf'), 'r')
        config = json.loads(config_file.read())
        config_file.close()
    except (IOError, JSONDecodeError):
        if sys.argv[1] != "configure":
            try:
                os.rename(os.path.expanduser('~/.soil/soil.conf.bak'), os.path.expanduser('~/.soil/soil.conf'))
            except IOError:
                print("Can not load soil configuration. Plase run soil configure to configure it.")
                sys.exit()
    try:
        env_file = open(os.path.expanduser('~/.soil/soil.env'), 'r')
        env = json.loads(env_file.read())
        env_file.close()
    except (IOError, JSONDecodeError):
        if sys.argv[1] != "configure":
            try:
                os.rename(os.path.expanduser('~/.soil/soil.conf.bak'), os.path.expanduser('~/.soil/soil.conf'))
            except IOError:
                print("Can not load soil environment. Plase run soil configure to initialize it.")
                sys.exit()


def configure(args: argparse.Namespace) -> None:
    """
    Allows the user to provide the configuration parameters interactively and stores them into a file.
    """

    global env, config  # pylint: disable=C0103
    try:
        os.makedirs(os.path.expanduser('~/.soil/'))
    except FileExistsError:
        # directory already exists
        pass

    try:
        if args.reset:
            try:
                os.rename(os.path.expanduser('~/.soil/soil.conf'), os.path.expanduser('~/.soil/soil.conf.bak'))
                os.rename(os.path.expanduser('~/.soil/soil.env'), os.path.expanduser('~/.soil/soil.env.bak'))
            except FileNotFoundError:
                print("Seems there is no previous configuration. Performing a clean config...")
                args.reset = False
        config_file = open(os.path.expanduser('~/.soil/soil.conf'), 'x')
        config["soil_url"] = input("Enter url of your soil instance: ")  # nosec - Input is safe in python3
        auth_url_msg = "Enter authentication provider URL: [https://auth.amalfianalytics.com] "
        config["auth_url"] = input(auth_url_msg)   # nosec - Input is safe in python3
        if config["auth_url"] == "":
            config["auth_url"] = "https://auth.amalfianalytics.com"
        config["auth_app_id"] = input("Enter your application id: ")  # nosec - Input is safe in python3
        config["auth_api_key"] = input("Enter your API key: ")  # nosec - Input is safe in python3
        config_file.write(json.dumps(config, indent=4, sort_keys=True))
        config_file.close()

        # Create the environment file
        env_file = open(os.path.expanduser('~/.soil/soil.env'), 'x')
        env_file.write("{\n}")
        env_file.close()

        if args.reset:
            os.remove(os.path.expanduser('~/.soil/soil.conf.bak'))
            os.remove(os.path.expanduser('~/.soil/soil.env.bak'))

    except FileExistsError:
        if not args.reset:
            print("Soil already configured (Use --reset to reconfigure):\n")
            for option, value in config.items():
                print(option + ": " + value)


def login() -> None:
    """
    Authenticates to the authentication backend and stores the credentials (JWT) in the environment
    """

    global env, config  # pylint: disable=C0103

    print(f"Authenticating to {config['auth_url']}...")
    if "auth" in env:
        username = input("Username: [" + env["auth"]["user"]["username"] + "]")  # nosec - Input is safe in python3
        if username == "":
            username = env["auth"]["user"]["username"]
    else:
        username = input("Username: ")  # nosec - Input is safe in python3
    password = getpass.getpass()

    request_json = {'loginId': username, 'password': password, 'applicationId': config['auth_app_id']}

    # print(request_json)

    resp = requests.post(config['auth_url']+"/api/login",
                         headers={'Authorization': config['auth_api_key']},
                         json=request_json)

    if resp.status_code == 200 or resp.status_code == 202:
        env["auth"] = json.loads(resp.content)
        save_environment()
        print('Successfully logged in as ' + env['auth']['user']['username'] + "!")
    elif resp.status_code == 404:
        print("The user was not found or the password was incorrect.")
        login()


def init(args: argparse.Namespace) -> None:
    """
    Initializes the current directory or the one provided as argument as a SOIL project by placing
    all the directory structure and creating a python virtual environment.
    """

    dirname = vars(args)["dirname"][0]

    if dirname != '.':
        try:
            os.mkdir(dirname)
        except FileExistsError:
            print("The directory " + dirname + " already exists")
            sys.exit()

    if get_soil_root(dirname):
        if dirname != '.':
            os.rmdir(dirname)
        print("This location is already a soil project")
        sys.exit()
    else:
        with zipfile.ZipFile(os.path.dirname(os.path.realpath(__file__))+'/template.zip', 'r') as template_zip:
            template_zip.extractall(os.path.abspath('./'+dirname))
        # create and activate the virtual environment
        virtualenv.cli_run([os.path.abspath('./'+dirname+'/.venv')])


def install(args: argparse.Namespace) -> None:
    """
    Invokes current project's virtual environment pip to install the provided packages.
    Also updates requirements.txt
    """

    soil_root = get_soil_root('.')
    if not soil_root:
        print("This folder is not initalized as a soil project. Please run soil init to initialize it.")
        sys.exit()

    packages = vars(args)["packages"]

    for package in packages:
        subprocess.check_call(['.venv/bin/python', "-m", "pip", "install", package])    # nosec
    f = open('requirements.txt', 'w')
    f.write(os.popen(soil_root + '/.venv/bin/pip freeze').read())    # nosec
    f.close()


def run(args: argparse.Namespace) -> None:
    """
    Runs the script provided as argument using the python in the virtual environment
    """

    soil_root = get_soil_root('.')
    if not soil_root:
        print("This folder is not initalized as a soil project. Please run soil init to initialize it.")
        sys.exit()

    chapter = vars(args)["chapter"]
    module = vars(args)["module"]
    module_args = vars(args)["module_args"]

    os.chdir(soil_root)
    with open('soil.yml') as f:
        conf = yaml.safe_load(f)
    try:
        script = [script for script in conf[chapter] if script.get(module) is not None][0][module]
    except (IndexError, KeyError):
        print('Script', module, 'not found.')
        sys.exit()
    params = script.get('params', {})
    params = [['--' + k, str(v)] for (k, v) in params.items()]
    params = [item for sublist in params for item in sublist]
    try:
        shell = ['.venv/bin/python', '-m', script['path']] + module_args + params
        print('Running:', ' '.join(shell))
        subprocess.run(shell, check=True)    # nosec
    except subprocess.CalledProcessError:
        sys.exit()


def test(args: argparse.Namespace) -> None:
    """
    Launches tests in the test folder.
    """
    soil_root = get_soil_root('.')
    if not soil_root:
        print("This folder is not initalized as a soil project. Please run soil init to initialize it.")
        sys.exit()

    test_args = vars(args)["test_args"]

    os.chdir(soil_root)
    try:
        subprocess.run(['.venv/bin/python', '-m', 'unittest'] + test_args, check=True)    # nosec
    except subprocess.CalledProcessError:
        sys.exit()


def main() -> None:
    """ main function"""

    args = parser.parse_args()

    soil_init()

    try:
        if args.command == 'configure':
            configure(args)
        elif args.command == 'login':
            login()
        elif args.command == 'init':
            init(args)
        elif args.command == 'install':
            install(args)
        elif args.command == 'run':
            run(args)
        elif args.command == 'test':
            test(args)
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt - Exit...")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0) # NOQA # pylint: disable=protected-access


if __name__ == "__main__":
    main()
