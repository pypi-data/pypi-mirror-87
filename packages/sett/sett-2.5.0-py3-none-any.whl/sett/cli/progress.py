import sys
import time
import locale

from ..utils.progress import ProgressInterface


class CliProgress(ProgressInterface):
    """Terminal progress bar

    :param prefix: prefix string (Optional)
    :param suffix: suffix string (Optional)
    :param decimals: positive number of decimals in percent complete
    :param bar_length: character length of bar
    :param fill: Fill character for the bar
    :param initial_print: If true, do an intial print at :intital_fraction:
    :param initial_fraction: The initial position, the progress bar will start at
    """

    def __init__(self,
                 prefix: str = '',
                 suffix: str = '',
                 decimals: int = 1,
                 bar_length: int = 60,
                 fill: str = '█',
                 initial_print: bool = True,
                 initial_fraction: float = 0.):
        _, encoding = locale.getlocale()
        if encoding != "UTF-8" and fill == '█':
            fill = '#'

        self.total = 1.0
        self.n0 = initial_fraction
        self.n = initial_fraction
        self.prefix = prefix + ' ' if prefix else ''
        self.suffix = ' ' + suffix if suffix else ''
        self.decimals = decimals
        self.bar_length = bar_length
        self.fill = fill
        self.t0 = time.time()
        self.t = self.t0
        self.line_length = 0
        self._update_precision = decimals + 2
        if initial_print:
            self.print_current()

    def update(self, completed_fraction: float) -> None:
        t = time.time()
        completed_fraction_rounded = round(completed_fraction,
                                           self._update_precision)
        # != also handles reseting progress
        if completed_fraction_rounded != self.n or t - self.t > 1.:
            self.n = completed_fraction_rounded
            self.t = t
            self.print_current()

    def get_completed_fraction(self) -> float:
        return self.n

    def print_current(self):
        percent = (
            "{0:." + str(self.decimals) + "f}").format(100 * (self.n / float(self.total)))
        filled_length = int(self.bar_length * self.n // self.total)
        char_bar = self.fill * filled_length \
            + '-' * (self.bar_length - filled_length)
        if self.n == self.n0:
            eta_str = ''
        else:
            eta = self.t - self.t0
            if self.n != self.total:
                eta *= (self.total - self.n) / (self.n - self.n0)

            eta_str = ' (' + format_eta(eta) + 's)'
        line = '\r' + self.prefix + '|' + char_bar + '| ' + \
            percent + '%' + eta_str + self.suffix
        fill_space = (' ' * max(0, self.line_length - len(line)))
        self.line_length = len(line)

        sys.stdout.write(line + fill_space)
        if self.n == self.total:
            sys.stdout.write('\n')
        sys.stdout.flush()


def format_eta(eta_secs: float) -> str:
    eta_h, eta_secs = divmod(eta_secs, 3600)
    eta_min, eta_secs = divmod(eta_secs, 60)
    if eta_h != 0.:
        return f"{int(eta_h):02d}:{int(eta_min):02d}:{int(eta_secs):02d}"
    if eta_min != 0.:
        return f"{int(eta_min):02d}:{int(eta_secs):02d}"
    return str(int(eta_secs))
