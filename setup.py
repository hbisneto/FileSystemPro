# -*- coding: utf-8 -*-
#
# setup.py
# FileSystemPro
#
# Created by Heitor Bisneto on 12/11/2025.
# Copyright © 2023–2025 hbisneto. All rights reserved.
#
# This file is part of FileSystemPro.
# FileSystemPro is free software: you can redistribute it and/or modify
# it under the terms of the MIT License. See LICENSE for more details.
#

from setuptools import setup, Extension, find_packages

with open("README.md", "r") as fh:
    readme = fh.read()

project_urls = {
    'Homepage': 'https://github.com/hbisneto/FileSystemPro',
    'Repository': 'https://github.com/hbisneto/FileSystemPro.git',
}

setup(
    name = 'filesystempro',
    version = '3.0.0.0',
    url = 'https://github.com/hbisneto/FileSystemPro',
    license = 'MIT License',
    
    author = 'Heitor Bisneto',
    author_email = 'heitor.bardemaker@live.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
    ],
    description = u'FileSystemPro is a powerful toolkit designed to handle file and directory operations with ease and efficiency across various operating systems.',
    install_requires = [
        'requests',
    ],
    long_description = readme,
    long_description_content_type = "text/markdown",
    keywords=[
        'filesystem', 'file-operations', 'directory-management', 'cross-platform',
        'file-io', 'pathlib-wrapper', 'compression-utils', 'file-watcher',
        'os-agnostic', 'linux', 'macos', 'windows'
    ],
    packages=find_packages(),
    platforms = 'any',
    python_requires= '>=3.10',
    project_urls=project_urls,
)