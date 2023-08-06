__all__ = ['add', 'clear', 'mkdir']


try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser
import os
import sys

"""
Linux:
/var/log

MacOS:
/usr/local/var/log
~/Library/Logs
"""

mac = "darwin" in sys.platform.lower()
UNIX_LOGS = "/var/log/supervisor"
MAC_LOGS = os.path.join(os.getenv("HOME"), "Library", "Logs", "supervisor")
SUPERVISOR_LOGS = MAC_LOGS if mac else UNIX_LOGS

if "SUPERVISOR_LOGS" in os.environ:
    SUPERVISOR_LOGS = os.getenv("SUPERVISOR_LOGS")


class Configuration:
    path = None

    def __init__(self, path):
        self.path = path
        config = ConfigParser()
        with open(path, "r") as f:
            config.read_file(f) if hasattr(
                config, "read_file") else config.readfp(f)
        self.config = config

    def clear(self):
        for section in self.config.sections():
            for key in ("stdout_logfile", "stderr_logfile"):
                path = self.config[section][key]
                if os.path.exists(path):
                    open(path, "w").write("")

    def mkdir(self):
        for section in self.config.sections():
            for key in ("stdout_logfile", "stderr_logfile"):
                path = os.path.expanduser(self.config[section][key])
                dirname = os.path.dirname(path)
                if not os.path.exists(dirname):
                    os.makedirs(dirname)

    def add(self):
        for section in self.config.sections():
            if "program:" not in section:
                continue
            name = section.split(":")[1]
            for f, key in [("err", "stderr_logfile"), ("out", "stdout_logfile")]:
                path = os.path.join(SUPERVISOR_LOGS, name, "%s.log" % f)
                if not hasattr(self.config[section], key):
                    self.config[section][key] = path
        self.save()

    def save(self):
        with open(self.path, 'w') as configfile:
            self.config.write(configfile)


def clear(path):
    """clear log files"""
    configuration = Configuration(path)
    configuration.clear()


def mkdir(path):
    """add stdout_logfile and stderr_logfile to supervisor config sections"""
    configuration = Configuration(path)
    configuration.mkdir()


def add(path):
    """add stdout_logfile and stderr_logfile to supervisor config sections"""
    configuration = Configuration(path)
    configuration.add()
