"""
    Geo-Instruments
    Sitecheck Scanner

Loads program configuration as a project.tuple object

Config file looks for file in the following hierarchy:
1. Argument
2. Default
3. File_dialog
4. Generate_default

http://docs.python.org/library/configparser.html

"""
import configparser
import os.path
import subprocess
import sys
import paho.mqtt.client as mqtt
import paho.mqtt.publish as pub
import paho.mqtt.subscribe as sub

from . import *

logger = logging.getLogger('config')


def edit_project():
    """
    Subprocess edit Project configuration file in notepad.

    ::returns:: Edit subprocess returncode
    """
    logger.info("Project config file opened. Please close to continue..")
    if os.path.exists(projectstore):
        if os.supports_bytes_environ:
            subprocess.Popen(["mousepad", projectstore]).wait()
        else:
            subprocess.run(f'notepad.exe {projectstore}')


def edit_config_option(project, option, value):
    """
    Change an option in the projects.ini file
    :param project: Project who's config to edit
    :param option: Option to edit
    :param value: New value of the option
    Example - edit_config_option(
    """
    config = configparser.ConfigParser()
    config.read(projectstore)
    config[project][option] = value
    try:
        with open(projectstore, 'w') as configfile:
            config.write(configfile)
            logger.debug(f'Editted config file: {project}, {option}, {value}')
    except configparser.Error as err:
        return err


def file_dialog():
    """
        Check and use Tkinter for file dialog, or call generate_default.

        ::returns:: filename
    """
    try:
        import tkinter
        from tkinter import filedialog

        options = {}
        options['defaultextension'] = '.ini'
        options['filetypes'] = [('ini config files', '.ini')]
        options['initialdir'] = os.environ['ROOT_DIR']
        options['initialfile'] = 'projects.ini'
        options['title'] = 'Select Project Configuration File'
        root = tkinter.Tk()
        filename = filedialog.askopenfilename(**options)
        root.destroy()
        return filename
    except ImportError:
        pass


def read_config_file():
    """
    Prompts user to select projects.ini configuration and returns contents as list
    Default projects.ini is ROOT_DIR+"\\project.ini"

    :rtype: list
    """
    if os.path.isfile(projectstore):
        config_file = projectstore
    else:
        config_file = file_dialog()

    if config_file == '':
        sys.exit("No Config selected. Exiting..")
    elif not os.path.isfile(config_file):
        logger.warning("file (%s) not found. " % config_file)
        sys.exit("Exiting..")

    config = configparser.ConfigParser()
    try:
        config.read(config_file)
    except configparser.DuplicateSectionError as e:
        logger.warn('Duplicate Section Error found in config, '
                    'Please locate the error in notepad \n' + str(e))
        edit_project()
        logger.warn("Rerunning config check..")
        read_config_file()
    except configparser.DuplicateOptionError as e:
        logger.warn('Duplicate Setup found in config, '
                    'Please locate the error in notepad \n' + str(e))
        edit_project()
        logger.warn("Rerunning config check..")
        read_config_file()

    return config


def postData(msgs):
    """
    Pub multible messages in same session
    :param msgs: dict
        {
            'topic':   f'Scanner/config/{project}/name',
            'payload': config[project]['name'],
            'retain':  True
        },
    
    """
    pub.multiple(msgs, hostname=hostname, port=port)


class fetch_config:
    """
    Create's tuple object from given section "project"
    ::return:: self
    """

    def __init__(self, project):
        self.project = project
        # self.fileConfig()
        self.name = self.fetchData('name')
        self.planarray = self.fetchData('planarray')
        self.site = self.fetchData('site')
        self.skip = self.fetchData('skip')

    def fetchData(self, var):
        data = sub.simple(
            f'Scanner/config/{self.project}/{var}',
            hostname=hostname, port=port, keepalive=1)
        sub.callback(
            self.on_message_set,
            f'Scanner/config/{self.project}/{var}',
            hostname=hostname, port=port)
        return str(data.payload)

    def on_message_set(self, client, userdata, message):
        print("%s %s" % (message.topic, message.payload))

    def fileConfig(self):
        config = configparser.ConfigParser()
        config.read(projectstore)
        self.name = config[self.project]['name']
        self.planarray = config[self.project]['planarray']
        self.site = config[self.project]['site']
        self.skip = config[self.project]['skip']
        # elif os.environ['SCANNER_CONFIG'] == 'mqtt':


class pubFullConfig:
    def __init__(self):
        projects = read_config_file()
        config = configparser.ConfigParser()
        config.read(projectstore)
        for project in projects.sections():
            postData([
                {
                    'topic':   f'Scanner/config/{project}/name',
                    'payload': config[project]['name'],
                    'retain':  True
                    },
                {
                    'topic':   f'Scanner/config/{project}/planarray',
                    'payload': config[project]['planarray'],
                    'retain':  True
                    },
                {
                    'topic':   f'Scanner/config/{project}/site',
                    'payload': config[project]['site'],
                    'retain':  True
                    },
                {
                    'topic':   f'Scanner/config/{project}/skip',
                    'payload': config[project]['skip'],
                    'retain':  True
                    }
                ])
