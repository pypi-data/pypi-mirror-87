"""
    Geo-Instruments
    Sitecheck Scanner
    Command Line argument Parser for Scanner
    Provides handling of arguments passed from command line
    These can be made permenant by adding them to your shortcut path

"""
import argparse
import logging
import os
from pathlib import Path

from . import config
from . import utlis

logger = logging.getLogger('config')
projects = config.read_config_file()
version = utlis.get_version()

ROOT_card: str = utlis.ensure_exists(str(
    Path(os.environ.get('OneDriveCommercial', '~') + "//Scanner//")
    ))

data_choice = [
    'print', 'file',
    'list', 'card',
    'mqtt',
    ]

btins = [
    'force-all',
    'qv', 'amp',
    ]

chrome_args = ['--window-size=1980,944']  # '--kiosk''


class Formatter(argparse.RawDescriptionHelpFormatter):
    """argparse.RawDescriptionHelpFormatter
        Provides formatting settings for argument "Help" messages.
        Can add argparse.ArgumentDefaultsHelpFormatter for defaults.
    """
    pass


class arg_text:
    """ Text for --help """
    main: str = (f""
                 f"\n    Automated Sitecheck Toolkit - Version: {version}\n"
                 f"\nSensors are sorted into three categories:"
                 f"\nUp-to-date:    Most recent data is within 24 hours"
                 f"\nOverdue:       Instrument is behind"
                 f"\nOld:           Reading has been missing for over a week\n"
                 f"\nSensor information is published via paho MQTT client"
                 f"\nFor entire runlog, Sub to topic 'Scanner/#' "
                 # f"\nFor more specific options, Please see --mqtt-help\n"
                 f"")
    info: str = 'Set logging level to Info'
    debug: str = 'Set logging level to Debug'
    log: str = f'Saves runlog to file'
    edit: str = 'Opens projects file in notepad(win) or Vim(unix)'
    watchdog: str = 'Set number of hours to mark as \'Up-to-date\''
    test: str = 'Run program up until time of browser creation for testing.'
    Update: str = 'Pub full project info to mqtt store'
    old: str = 'Include in report sensors missing for Longer than a week. ' \
               'This is off by default, Assumes sensors missing for 7 days ' \
               'are discussed. (pending depricated)'
    new: str = 'Include in report sensors that pass checks. This is off by ' \
               'default to prevent unnecessary spam (pending depricated)'
    headless: str = 'Enables Pyppeteer\'s Headless mode. The browser ' \
                    'will run invisibly, Known Issues with Qv navigation ' \
                    'are being addressed'
    output: str = 'Set card output directory (depricated)'
    value: str = 'Include current Sensor data in output (Currently AMP only)'
    sensor: str = 'Run until this Sensor name is found. Implies --detach'
    screenshot: str = 'Screenshot missing sensors'
    repl: str = 'read–eval–print loop (REPL) Interactive command mode'
    data: str = f'Selects Output format (Usage: --data mqtt) ' \
                f'Options: {data_choice}'
    project: str = f'Define a single project to run. ' \
                   f'Builtins include: {str(btins)}. ' \
                   f'-- Configured Projects: {str(projects.sections())}. '


parser = argparse.ArgumentParser(
    description=arg_text.main,
    prog='Sitecheck Scanner',
    formatter_class=Formatter
    )

parser.add_argument('-H', '--headless', action='store_true',
                    default=os.environ.get('SCANNER_HEADLESS', False),
                    help=argparse.SUPPRESS)  # help=arg_text.hadless)

parser.add_argument('-a', '--autoclose', action='store_true',
                    default=os.environ.get('SCANNER_AUTOCLOSE', True),
                    help=argparse.SUPPRESS)  # help=arg_text.hadless)

parser.add_argument('-i', '--info', action='store_true',
                    default=os.environ.get('SCANNER_INFO', True),
                    help=arg_text.info)

parser.add_argument('-d', '--debug', action='store_true',
                    default=os.environ.get('SCANNER_DEBUG', False),
                    help=arg_text.debug)

parser.add_argument('-l', '--log', action='store_true',
                    default=os.environ.get('SCANNER_LOG', False),
                    help=arg_text.log)

parser.add_argument('-e', '--edit', action='store_true',
                    default=os.environ.get('SCANNER_EDIT', False),
                    help=arg_text.edit)

parser.add_argument('-w', '--watchdog',
                    default='24',
                    metavar='', type=int,
                    help=arg_text.watchdog)

parser.add_argument('--test', action='store_true',
                    default=os.environ.get('SCANNER_TEST', False),
                    help=arg_text.test)

parser.add_argument('--update', action='store_true',
                    default=os.environ.get('SCANNER_RESET', False),
                    help=arg_text.Update)

parser.add_argument('-O', '--old', action='store_true',
                    default=os.environ.get('SCANNER_OLD', False),
                    help=argparse.SUPPRESS)  # help=arg_text.old)

parser.add_argument('-N', '--new', action='store_true',
                    default=os.environ.get('SCANNER_NEW', False),
                    help=argparse.SUPPRESS)  # help=arg_text.new)

parser.add_argument('-o', '--output', action='store', type=str, metavar='',
                    default=ROOT_card,
                    help=argparse.SUPPRESS)  # help=arg_text.output)

parser.add_argument('-v', '--value', action='store_true', default=False,
                    help=arg_text.value)

parser.add_argument('--sensor', default='',
                    type=str,
                    metavar='',
                    help=arg_text.sensor)

parser.add_argument('-s', '--screenshot', action='store_true', default=False,
                    help=arg_text.screenshot)

parser.add_argument('-r', '--repl', action='store_true',
                    default=os.environ.get('SCANNER_REPL', False),
                    help=arg_text.repl)

parser.add_argument('--data', default='mqtt',
                    choices=data_choice, metavar='',
                    help=arg_text.data)

parser.add_argument('-p', '--project', default='All',
                    choices=projects.sections(), metavar='',
                    help=arg_text.project)

args = parser.parse_args()

os.environ['imagelist'] = 'fakesensor1,fakesensor2'
os.environ['SCANNER_OUTPUT_TYPE'] = str(args.data)
os.environ['Repl']: bool = str(args.repl)
os.environ['Edit']: bool = str(args.edit)
os.environ['Update']: bool = str(args.update)
os.environ['Output']: str = args.output
os.environ['DETACH']: bool = args.sensor
Headless: bool = args.headless
Autoclose: bool = args.autoclose
Project: str = args.project
Info: bool = args.info
Debug: bool = args.debug
Log: bool = args.log
Test: bool = args.test
PrintOld: bool = args.old
PrintNew: bool = args.new
Getvalue: bool = args.value
Screenshot: bool = args.screenshot

Watchdog: int = int(args.watchdog * 3600)
Oldperiod: int = 604800
