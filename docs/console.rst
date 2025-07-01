.. _console-module:

Console Module
==============

The Console module is a robust library designed to enable ANSI escape character sequences for generating colored terminal text and cursor positioning. This library is a key addition to FileSystemPro as a third-party library, enhancing the toolkit for developers who require consistent terminal styling across different operating systems.

Features
--------

- **Universal Compatibility**: Ensures that applications or libraries utilizing ANSI sequences for colored output on Unix or macOS can now operate identically on Windows systems.
- **Simplified Integration**: With no dependencies other than the standard library, integrating Console into your projects is straightforward. It’s tested across multiple Python versions, ensuring reliability.
- **Enhanced Terminal Experience**: By converting ANSI sequences into appropriate win32 calls, Console allows Windows terminals to emulate the behavior of Unix terminals, providing a consistent user experience.
- **Effortless Transition**: For developers transitioning to FileSystemPro, incorporating Console into your workflow is effortless, enabling you to maintain the visual aspects of your terminal applications without platform constraints.

.. automodule:: filesystem.console
   :members:
   :undoc-members:
   :show-inheritance:

Constants
---------

These constants are used to control the appearance of text output in the terminal, including foreground and background colors, as well as text styles. By utilizing these constants, developers can enhance the readability and visual appeal of their terminal applications, ensuring a consistent experience across different operating systems.

+------------------+-------------------------------+
| Constants        | Colors                        |
+==================+===============================+
| foreground       | BLACK, RED, GREEN, YELLOW,    |
|                  | BLUE, MAGENTA, CYAN, WHITE,   |
|                  | RESET                         |
+------------------+-------------------------------+
| background       | BLACK, RED, GREEN, YELLOW,    |
|                  | BLUE, MAGENTA, CYAN, WHITE,   |
|                  | RESET                         |
+------------------+-------------------------------+
| style            | DIM, NORMAL, BRIGHT,          |
|                  | RESET_ALL                     |
+------------------+-------------------------------+

Examples
--------

.. note::
   For the color changes to work, your terminal must support ANSI escape sequences, which are used to set the color. Not all terminals do, so if you’re not seeing the colors as expected, that could be why.

**Printing a Red Foreground Text Message**

.. code-block:: python

   from filesystem import console as fsconsole

   # This will print a spaced text to your print message
   print(fsconsole.foreground.RED, "This is a warn message")

   # This will print a no space text to your print message
   print(fsconsole.foreground.RED + "This is another warn message")

   # You can use f-string format to assign the color to your print
   print(f'{fsconsole.foreground.RED}This is a new warn message{fsconsole.foreground.RESET}')

   # This text will be printed without color (default)
   print("This is a normal text")

**Output** (assuming ANSI-compatible terminal):

.. code-block:: text

   This is a warn message (in red)
   This is another warn message (in red)
   This is a new warn message (in red)
   This is a normal text

**Printing a Blue Background Text Message**

.. code-block:: python

   from filesystem import console as fsconsole

   # This will print a spaced text to your print message
   print(fsconsole.background.BLUE, 'This is a blue background message')

   # This will print a no space text to your print message
   print(fsconsole.background.BLUE + 'This is another blue background message')

   # You can use f-string format to assign the color to your print
   print(f'{fsconsole.background.BLUE}This is a new blue background message{fsconsole.background.RESET}')

   # This text will be printed without color (default)
   print('This is a normal text')

**Output** (assuming ANSI-compatible terminal):

.. code-block:: text

   This is a blue background message (with blue background)
   This is another blue background message (with blue background)
   This is a new blue background message (with blue background)
   This is a normal text

**Different Foregrounds, Backgrounds, and Styles**

.. code-block:: python

   from filesystem import console as fsconsole

   # Prints a red foreground text
   print(f'{fsconsole.foreground.RED}Some red text')

   # Prints a red foreground text with a green background
   print(f'{fsconsole.background.GREEN}And with a green background{fsconsole.style.RESET_ALL}')

   # Prints a dim normal text with no background
   print(f'{fsconsole.style.DIM}And in dim text{fsconsole.style.RESET_ALL}')

   # Prints a normal text
   print('Back to normal color')

**Output** (assuming ANSI-compatible terminal):

.. code-block:: text

   Some red text (in red)
   And with a green background (in red with green background)
   And in dim text (in dim style)
   Back to normal color