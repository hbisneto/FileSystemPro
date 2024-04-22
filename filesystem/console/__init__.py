# Copyright Jonathan Hartley 2013. BSD 3-Clause license, see LICENSE file.
from .initialise import init, deinit, reinit, console_text, just_fix_windows_console
from .ansi import foreground, background, style, cursor
from .ansitowin32 import AnsiToWin32

# __version__ = '0.4.7dev1' - Colorama dev version
__version__ = '1.0.0.0' # Console Library version

