.. _watcher-module:

Watcher Module
==============

The Watcher module serves as a monitoring system for the file system. It keeps track of any changes made within the file system, such as the creation of new files, modification of existing files, or deletion of files. This feature allows for real-time updates and can be particularly useful in scenarios where maintaining the integrity and up-to-date status of the file system is crucial, such as in a backup system or a live syncing service.

Features
--------

- **Initialization**: The constructor method initializes the Watcher object with a root directory to watch and saves the current state of the file system.
- **State Retrieval**: Returns a dictionary of all files in the given path with their metadata.
- **Change Detection**: Compares the current state of the file system with the saved state to identify any changes (created, updated, or removed files) and returns a list of dictionaries with the metadata of changed files and the type of change.
- **String Representation**: Returns a string representation of the Watcher object.

.. automodule:: filesystem.watcher
   :members:
   :undoc-members:
   :show-inheritance:

Methods
-------

The Watcher module in FileSystemPro brings a comprehensive set of methods that streamline and enhance file system monitoring.

.. code-block:: python

   from filesystem import watcher as wat

.. list-table::
   :header-rows: 1
   :widths: auto

   * - Method
     - Description
   * - init(self, root)
     - This is the constructor method that initializes the Watcher object with a root directory to watch. It also saves the current state of the file system in **self.saved_state**.
   * - get_state(self, path)
     - This method returns a dictionary where the keys are the absolute paths of all files in the given path and the values are file metadata obtained from the **wrapper.enumerate_files(path)** function.
   * - diff(self)
     - This method compares the current state of the file system with the saved state and identifies any changes (created, updated, or removed files). It returns a list of dictionaries where each dictionary contains the metadata of a changed file and an additional key "change" indicating the type of change.
   * - str(self)
     - This method returns a string representation of the **Watcher** object.

Examples
--------

**Monitoring Documents Folder**

The following example is designed to monitor changes in the **Documents** directory and print out the changes as they occur.

.. code-block:: python

   # Native library
   import time
   from datetime import datetime

   # FileSystemPro
   import filesystem as fs
   from filesystem import watcher as wat

   # Create a new instance of Watcher class
   watcher = wat.Watcher(f'{fs.documents}')

   # Run `diff` method to get directory changes
   while True:
       changes = watcher.diff()
       if changes:
           print(f"Changes detected at: {datetime.now()}:")
           for change in changes:
               print(f"{change['abspath']} was {change['change']}")
       time.sleep(5)  # Awaits for 5 seconds before a new verification