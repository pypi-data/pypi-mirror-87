__all__ = [
    "PlumberLogger",
    "PlumberFormatter",
]

import logging


class PlumberFormatter(logging.Formatter):

    """
    Custom formatter for pyPlumber logger
    """

    black = "0;30"
    red = "0;31"
    green = "0;32"
    yellow = "0;33"
    blue = "0;34"
    magenta = "0;35"
    cyan = "0;36"
    white = "0;37"

    bold_black = "1;30"
    bold_red = "1;31"
    bold_green = "1;32"
    bold_yellow = "1;33"
    bold_blue = "1;34"
    bold_magenta = "1;35"
    bold_cyan = "1;36"
    bold_white = "1;37"

    reset_seq = "\033[0m"
    color_seq = "\033[%(color)sm"
    colors = {
        "DEBUG": cyan,
        "INFO": green,
        "WARNING": bold_yellow,
        "ERROR": red,
        "FATAL": bold_red,
    }

    def __init__(self, msg="[%(levelname)s] %(asctime)s: %(message)s", color=True):

        """Inits PlumberFormatter.

        Args:
            msg: the message format.
            color: enables/disables coloring
        """

        if color:
            super(PlumberFormatter, self).__init__(
                self.color_seq + msg + self.reset_seq
            )
        else:
            super(PlumberFormatter, self).__init__(msg)

    def format(self, record):
        if not (hasattr(record, "nl")):
            record.nl = True
        levelname = record.levelname
        if not "color" in record.__dict__ and levelname in self.colors:
            record.color = self.colors[levelname]
        return super(PlumberFormatter, self).format(record)


class PlumberLogger(logging.Logger):

    """
    Custom Logger class for pyPlumber
    """

    def __init__(
        self,
        name="PlumberLogger",
        level=logging.NOTSET,
        formatter=None,
    ):

        """Inits PlumberLogger.

        Args:
            name: the logger name.
            level: the logger level.
            formatter: custom formatting. Default is
                PlumberFormatter.
        """

        super(PlumberLogger, self).__init__(name, level)
        self.propagate = False
        for handler in self.handlers.copy():
            self.removeHandler(handler)
        formatter = formatter or PlumberFormatter(color=True)
        handler = logging.StreamHandler()
        handler.setLevel(level)
        handler.setFormatter(formatter)
        self.addHandler(handler)
