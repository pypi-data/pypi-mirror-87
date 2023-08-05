#!/usr/bin/env python
"""
A very simple progress bar which keep track of the progress as we consume an
iterator.
"""
import sys
import threading
import time

# progress bar
from prompt_toolkit.shortcuts import ProgressBar
from prompt_toolkit.styles import Style
from prompt_toolkit.shortcuts.progress_bar import formatters

tab = '\t'.expandtabs(4)

style = Style.from_dict(
    {
        "title": "#5f87ff",
        "label": "#5f87ff",
        "percentage": "#00ff00",
        "bar-a": "bg:#00ff00 #004400",
        "bar-b": "bg:#00ff00 #000000",
        "bar-c": "#000000 underline",
        "current": "#448844",
        "total": "#448844",
        "time-elapsed": "#444488",
        "time-left": "bg:#88ff88 #000000",
    }
)

style = Style.from_dict(
    {
        "title": "#5f87ff",
        "label": "#5f87ff",
        "percentage": "#00ff00",
        "bar-a": "#00ff00",
        "bar-b": "bg:#00ff00 #000000",
        "bar-c": "#aaaaaa",
        "current": "#448844",
        "total": "#448844",
        "time-elapsed": "#444488",
        "time-left": "bg:#88ff88 #000000",
    }
)


custom_formatters = [
    formatters.Text(tab),
    formatters.Label(suffix=': '),
    formatters.Bar(start=' |', end='|', sym_a='#', sym_b='#', sym_c='.'),
    formatters.Text(' '),
    formatters.Progress(),
    formatters.Text(' '),
    formatters.Percentage(),
    formatters.Text(' [elapsed: '),
    formatters.TimeElapsed(),
    formatters.Text(' left: '),
    formatters.TimeLeft(),
    formatters.Text(']'),
    formatters.Text(tab),
]


class ProgressBarMain(threading.Thread):
    def __init__(self, label='Working', delay=0.1, cycles=500):
        super(ProgressBarMain, self).__init__()
        self.label = label
        self.delay = delay  # interval between updates
        self.running = False
        self.end = int(cycles)

    def start(self):
        self.running = True
        super(ProgressBarMain, self).start()

    def run(self):
        with ProgressBar(style=style, formatters=custom_formatters) as pb:
            for i in pb(range(self.end), label=self.label):
                time.sleep(self.delay)
                if not self.running:
                    break

    def stop(self):
        self.running = False
        self.join()  # wait for run() method to terminate
        sys.stdout.write('\r' + len(self.label)*' ' + '\r')  # clean-up
        sys.stdout.flush()


def main():
    with ProgressBar(
        style=style, title="Updating local AWS access keys\n"
    ) as pb:
        for i in pb(range(1600), label="Please wait..."):
            time.sleep(0.01)


if __name__ == "__main__":
    main()
