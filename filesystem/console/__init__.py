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
from .ansi import fore, back, style, cursor
from .ansitowin32 import AnsiToWin32

# __version__ = '0.4.7dev1' - Colorama dev version
__version__ = '3.0.0.0' # Console Library version
class Console:
    def __init__(self):
        self._fore = None
        self._back = None
        self._styles = []

    # Methods to set styles
    def foreground(self, color):
        self._fore = color
        return self

    def background(self, color):
        self._back = color
        return self

    def bright(self):
        self._styles.append(style.BRIGHT)
        return self

    def dim(self):
        self._styles.append(style.DIM)
        return self

    def underline(self):
        self._styles.append(style.UNDERLINE)
        return self

    def strikethrough(self):
        self._styles.append(style.STRIKETHROUGH)
        return self
    
    def reset(self):
        self._styles.append(style.RESET_ALL)
        return self
    
    def reset_strikethrough(self):
        self._styles.append(style.RESET_STRIKETHROUGH)
        return self
    
    def reset_underline(self):
        self._styles.append(style.RESET_UNDERLINE)
        return self

    # Foregrounds
    def black(self):
        return self.foreground(fore.BLACK)
    
    def blue(self):
        return self.foreground(fore.BLUE)
    
    def cyan(self):
        return self.foreground(fore.CYAN)
    
    def green(self):
        return self.foreground(fore.GREEN)

    def magenta(self):
        return self.foreground(fore.MAGENTA)
    
    def red(self):
        return self.foreground(fore.RED)
    
    def yellow(self):
        return self.foreground(fore.YELLOW)
    
    def white(self):
        return self.foreground(fore.WHITE)
    
    def light_black(self):
        return self.foreground(fore.LIGHTBLACK_EX)
        
    def light_blue(self):
        return self.foreground(fore.LIGHTBLUE_EX)
    
    def light_cyan(self):
        return self.foreground(fore.LIGHTCYAN_EX)
    
    def light_green(self):
        return self.foreground(fore.LIGHTGREEN_EX)
    
    def light_magenta(self):
        return self.foreground(fore.LIGHTMAGENTA_EX)
    
    def light_red(self):
        return self.foreground(fore.LIGHTRED_EX)
    
    def light_white(self):
        return self.foreground(fore.LIGHTWHITE_EX)
    
    def light_yellow(self):
        return self.foreground(fore.LIGHTYELLOW_EX)
    
    # Backgrounds
    def black_bg(self):
        return self.background(back.BLACK)
    
    def blue_bg(self):
        return self.background(back.BLUE)
    
    def cyan_bg(self):
        return self.background(back.CYAN)
    
    def green_bg(self):
        return self.background(back.GREEN)
    
    def magenta_bg(self):
        return self.background(back.MAGENTA)
    
    def red_bg(self):
        return self.background(back.RED)
    
    def yellow_bg(self):
        return self.background(back.YELLOW)
    
    def white_bg(self):
        return self.background(back.WHITE)
    
    def light_black_bg(self):
        return self.background(back.LIGHTBLACK_EX)
        
    def light_blue_bg(self):
        return self.background(back.LIGHTBLUE_EX)
    
    def light_cyan_bg(self):
        return self.background(back.LIGHTCYAN_EX)
    
    def light_green_bg(self):
        return self.background(back.LIGHTGREEN_EX)
    
    def light_magenta_bg(self):
        return self.background(back.LIGHTMAGENTA_EX)
    
    def light_red_bg(self):
        return self.background(back.LIGHTRED_EX)
    
    def light_white_bg(self):
        return self.background(back.LIGHTWHITE_EX)
    
    def light_yellow_bg(self):
        return self.background(back.LIGHTYELLOW_EX)

    def __call__(self, text):
        output = ''
        if self._fore:
            output += self._fore
        if self._back:
            output += self._back
        for s in self._styles:
            output += s
        output += text + style.RESET_ALL
        
        self._fore = None
        self._back = None
        self._styles = []
        
        return output

console = Console()