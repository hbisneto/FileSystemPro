# -*- coding: utf-8 -*-
#
# filesystem/console/__init__.py
# FileSystemPro
#
# Created by Heitor Bisneto on 12/11/2025.
# Copyright © 2023–2025 hbisneto. All rights reserved.
#
# This file is part of FileSystemPro.
# FileSystemPro is free software: you can redistribute it and/or modify
# it under the terms of the MIT License. See LICENSE for more details.
#

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
"""
# Console

---

## Overview
This module provides a simple, chainable API for applying ANSI color codes, backgrounds, and styles to console text output, inspired by Colorama. It supports cross-platform compatibility (including Windows via AnsiToWin32 wrapping) and ensures styles reset after application to avoid persistent formatting. The `Console` class can be chained for fluid styling, and a global `console` instance is provided for immediate use. Version: 3.0.0.0.

## Features
- **Color Foregrounds:** Set text colors (black, blue, cyan, green, magenta, red, yellow, white) with light variants (light_*).
- **Background Colors:** Apply colored backgrounds (e.g., red_bg, light_blue_bg) to text.
- **Text Styles:** Add effects like bright, dim, underline, strikethrough, with reset options (reset, reset_underline).
- **Chaining Support:** Method chaining for combining multiple styles (e.g., console.red().bold().underline()).
- **Automatic Reset:** Styles are applied and reset automatically when invoking the instance as a callable.
- **Global Instance:** Pre-instantiated `console` object for quick use without class instantiation.

## Usage
To use this module, import it and apply styles via the `Console` class or the global `console` instance:

```python
from filesystem import console
```

### Examples:

- Basic colored text output:

```python
colored_text = console.red()("This text is red!")
print(colored_text)  # Outputs red text, then resets
```

- Chained styles with background and effects:

```python
styled_text = console.blue().bright().underline().yellow_bg()("Bright blue underlined text on yellow background!")
print(styled_text)  # Applies all styles and resets
```

- Using light colors and partial resets:

```python
text = console.light_green()("Light green text").reset_underline()(" without underline")
print(text)  # Light green, then plain text
```

- Custom instance for persistent state (though resets are automatic):

```python
my_console = console.Console()
output = my_console.magenta().dim()("Dim magenta text")
print(output)
```
"""