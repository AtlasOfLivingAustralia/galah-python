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
import os
import sys
import galah

# -- Project information -----------------------------------------------------

project = 'Galah'
copyright = 'Atlas of Living Australia'
author = 'Amanda Buyan, Atlas of Living Australia'

# The full version, including alpha/beta/rc tags
release = '0.1.0'

# try this
sys.path.insert(0,"../../galah/src/galah/")

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
# 'sphinx.ext.autosectionlabel',
extensions = [
	'myst_parser',
	'sphinx-prompt',
	'sphinxcontrib.programoutput',
	'sphinx_design',
    'sphinx.ext.napoleon',
]

'''
	'autoapi.extension',
	'sphinx_autodoc_typehints'
	'sphinx.ext.autodoc',
	'sphinx.ext.autosummary',
'''

napoleon_use_param = True

#autoapi_member_order = "alphabetical"

myst_enable_extensions = ["colon_fence"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']
version = str(galah.__version__)
release = version
source_path = os.path.dirname(os.path.abspath(__file__))

# where all the API documentation lives
#autoapi_dirs = ['../../galah/src/galah/'] # see if this is the case

# don't automaticalliy generate api docs
#autoapi_generate_api_docs=False

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['apply_data_profile.py','get_api_url.py']

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'pydata_sphinx_theme'

html_theme_options = {
	"navbar_align": "content",
	"github_url": "https://github.com/AtlasOfLivingAustralia/galah_python",
	"page_sidebar_items": ["page-toc"],
    "logo": {
		"image_light": "logo.png",
        "image_dark": "logo.png", 
	},
}

# was image_light
html_sidebars = {
	"index": [],
	"search": [],
    "**": ["sidebar-nav-bs"]
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".

html_static_path = ['_static']

html_logo = "_static/logo/logo.png"

html_favicon = '_static/logo/favicon.ico'

html_css_files = ['css/extra.css']

html_style = 'css/extra.css'
