# # Configuration file for the Sphinx documentation builder.
# #
# # This file only contains a selection of the most common options. For a full
# # list see the documentation:
# # https://www.sphinx-doc.org/en/master/usage/configuration.html

# # -- Path setup --------------------------------------------------------------

# # If extensions (or modules to document with autodoc) are in another directory,
# # add these directories to sys.path here. If the directory is relative to the
# # documentation root, use os.path.abspath to make it absolute, like shown here.
# #
# # import os
# # import sys
# # sys.path.insert(0, os.path.abspath('.'))


# # -- Project information -----------------------------------------------------

# project = 'FileSystemPro'
# copyright = '2025, Heitor Bardemaker A. Bisneto'
# author = 'Heitor Bardemaker A. Bisneto'


# # -- General configuration ---------------------------------------------------

# # Add any Sphinx extension module names here, as strings. They can be
# # extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# # ones.
# extensions = [
# ]

# # Add any paths that contain templates here, relative to this directory.
# templates_path = ['_templates']

# # List of patterns, relative to source directory, that match files and
# # directories to ignore when looking for source files.
# # This pattern also affects html_static_path and html_extra_path.
# exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# # -- Options for HTML output -------------------------------------------------

# # The theme to use for HTML and HTML Help pages.  See the documentation for
# # a list of builtin themes.
# #
# html_theme = 'alabaster'

# # Add any paths that contain custom static files (such as style sheets) here,
# # relative to this directory. They are copied after the builtin static files,
# # so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['_static']

# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

import os
import sys
sys.path.insert(0, os.path.abspath('../..'))  # Ajusta para a raiz do repositório onde está o diretório filesystem/

# Adiciona a raiz do repositório ao sys.path
sys.path.insert(0, os.path.abspath('.'))
print("sys.path:", sys.path)
print("Current directory:", os.getcwd())
print("Filesystem module path:", os.path.abspath('.'))
try:
    import filesystem
    print("Filesystem module found at:", filesystem.__file__)
except ImportError as e:
    print("Failed to import filesystem:", str(e))

# -- Project information -----------------------------------------------------

project = 'FileSystemPro'
copyright = '2025, Heitor Bardemaker A. Bisneto'
author = 'Heitor Bardemaker A. Bisneto'
release = '2.0.1.0'  # Versão do projeto, igual ao pyproject.toml

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = [
    'sphinx.ext.autodoc',    # Gera documentação a partir do código
    'sphinx.ext.napoleon',   # Suporta docstrings no formato Google/NumPy
    'sphinx.ext.viewcode',   # Adiciona links para o código-fonte
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.
html_theme = 'sphinx_rtd_theme'  # Usa o tema ReadTheDocs

# Add any paths that contain custom static files (such as style sheets).
html_static_path = ['_static']