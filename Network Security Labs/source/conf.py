# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'Network Security Lab'
copyright = '2021, NEXUS Lab'
author = 'Chen Xu, Matthew ONeil, Taylor Elder'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']
pygments_style = 'sphinx'
# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
highlight_language = 'none'
html_theme = 'sphinx_rtd_theme'
# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

master_doc = 'index'

sectry = 'Sectry'
ezsetup = 'EZSetup'
sectry_introduction = '**Sectry** is a novel Web application capable of creating a variety of user-defined cybersecurity practice environments (e.g., labs and competition scenarios) in one or more computing clouds (e.g., OpenStack or Amazon AWS). Sectry provides a web based user interface for users to design, deploy, and access labs and related materials. Facilitators can create practice scenarios by dragging and dropping icons visually and creating the links between them. This allows for customization and significantly reduces overhead in creating and using practice environments. Completely spared from the complexity of creating practice environments, end users can jump right in and fully concentrate on cybersecurity practice.'
ezsetup_introduction = '**EZSetup** is a novel Web application capable of creating a variety of user-defined cybersecurity practice enviornments (e.g., labs and competition scenarios). EZSetup provides a Web user interface for practice designers to create a practice scenario by dragging and dropping icons visually and the links between them thus allows for customization and significantly reduces overhead in creating and using practice environments. Completely spared from the complexity of creating practice environments, end users can jump right in and fully concentrate on cybersecurity practice.'

rst_epilog = """
.. |Description| replace:: {descr}
.. |platform| replace:: {plat}
""".format(
descr = ezsetup_introduction,
plat =ezsetup
)