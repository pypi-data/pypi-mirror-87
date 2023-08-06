import abc
import os

from click import secho

from tktl.core.config import settings


def set_grpc_verbosity(verbose):
    if verbose:
        os.environ["GRPC_TRACE"] = "channel,http"
        os.environ["GRPC_VERBOSITY"] = "debug"
    else:
        os.environ.pop("GRPC_TRACE", None)
        os.environ.pop("GRPC_VERBOSITY", None)


class Logger(abc.ABC):
    verbose = False

    @abc.abstractmethod
    def log(self, msg, *args, **kwargs):
        pass

    @abc.abstractmethod
    def warning(self, msg, *args, **kwargs):
        pass

    @abc.abstractmethod
    def error(self, msg, *args, **kwargs):
        pass

    def debug(self, msg, *args, **kwargs):
        pass


class MuteLogger(Logger):
    def log(self, msg, *args, **kwargs):
        pass

    def warning(self, msg, *args, **kwargs):
        pass

    def error(self, msg, *args, **kwargs):
        pass


class CliLogger(Logger):
    @staticmethod
    def _log(message, color=None, err=False):
        message = str(message)
        color = color if settings.USE_CONSOLE_COLORS else None
        secho(message, fg=color, err=err)

    def trace(self, message, color=None, err=False):
        if self.verbose:
            self._log(message, color=color, err=err)

    def log(self, message, color=None, err=False):
        self._log(message, color=color, err=err)

    def error(self, message, *args, **kwargs):
        color = "red" if settings.USE_CONSOLE_COLORS else None
        self._log(message, color=color, err=True)

    def warning(self, message, *args, **kwargs):
        color = "yellow" if settings.USE_CONSOLE_COLORS else None
        self._log(message, color=color)

    def debug(self, message, *args, **kwargs):
        if settings.DEBUG:
            self._log("DEBUG: {}".format(message))


SdkLogger = CliLogger
LOG = CliLogger()
