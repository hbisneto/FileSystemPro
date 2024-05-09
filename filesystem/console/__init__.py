"""
# Console

---

## Overview
The Console module is a part of the Colorama library that provides terminal text coloring capabilities.
It is designed to enhance the visual presentation of text output in terminal applications,
allowing developers to add color and style to their console logs and messages.

## Features
- `Cross-Platform:` Works on Windows, Mac, and Linux terminals.
- `Easy to Use:` Simple API for adding color and style to text.
- `Automatic Reset:` Automatically resets text style after each print statement.

## How It Works
The `Console` class within the module is used to wrap text with ANSI escape sequences that terminals understand to display color. 
It provides methods like `foreground`, `background`, and `style` to specify text color, background color, and styles respectively.

### Text Styling
With `Console`, you can easily change the color and style of text. For example:
- `foreground:` Changes the color of the text.
- `background:` Changes the background color of the text.
- `style:` Changes the style of the text (e.g., bold, underline).

### Results
Using Console, styled text can be printed to the terminal, enhancing readability and user experience. 
The module handles the complexities of cross-platform text styling, providing a consistent interface across different operating systems.

## Usage
To use the `Console` module, simply import the desired classes and wrap your text:

```python
from filesystem import console as fsconsole

print(fsconsole.foreground.RED, "This is a red message")
print(fsconsole.foreground.BLUE, "This is a blue message")
```

"""

# Copyright Jonathan Hartley 2013. BSD 3-Clause license, see LICENSE file.
from .initialise import init, deinit, reinit, console_text, just_fix_windows_console
from .ansi import foreground, background, style, cursor
from .ansitowin32 import AnsiToWin32

# __version__ = '0.4.7dev1' - Colorama dev version
__version__ = '1.1.0.0' # Console Library version