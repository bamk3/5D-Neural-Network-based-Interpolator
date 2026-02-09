# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
sys.path.insert(0, os.path.abspath('../../backend'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = '5D Neural Network Interpolator'
copyright = '2025, Makimona Kiakisolako (bamk3)'
author = 'Makimona Kiakisolako (bamk3)'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'sphinx.ext.intersphinx',
    'sphinx.ext.coverage',
    'sphinx_rtd_theme',
]

templates_path = ['_templates']
exclude_patterns = []

# Napoleon settings for Google/NumPy docstring support
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = False
napoleon_type_aliases = None
napoleon_attr_annotations = True

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_theme_options = {
    'canonical_url': '',
    'analytics_id': '',
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'style_nav_header_background': '#2980B9',
    'collapse_navigation': False,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False
}

# Custom CSS and JavaScript
html_css_files = [
    'custom.css',
]

html_js_files = [
    'custom.js',
]

# Intersphinx mapping
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
    'sklearn': ('https://scikit-learn.org/stable/', None),
}

# AutoDoc settings
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__'
}

# -- Options for LaTeX/PDF output --------------------------------------------

latex_engine = 'pdflatex'
latex_elements = {
    'papersize': 'letterpaper',
    'pointsize': '10pt',
    'preamble': r'''
        \usepackage{charter}
        \usepackage[defaultsans]{lato}
        \usepackage{inconsolata}
    ''',
    'figure_align': 'htbp',
    'fncychap': r'\usepackage[Bjornstrup]{fncychap}',
}

# LaTeX document setup
latex_documents = [
    ('index', '5D-Interpolator-Documentation.tex',
     '5D Neural Network Interpolator Documentation',
     'Makimona Kiakisolako (bamk3)', 'manual'),
]

# Logo for LaTeX/PDF output
latex_logo = None

# Show URLs in footnotes
latex_show_urls = 'footnote'

# -- Options for manual page output ------------------------------------------

man_pages = [
    ('index', '5d-interpolator', '5D Neural Network Interpolator Documentation',
     [author], 1)
]

# -- Options for Texinfo output ----------------------------------------------

texinfo_documents = [
    ('index', '5D-Interpolator', '5D Neural Network Interpolator Documentation',
     author, '5D-Interpolator', 'Neural network interpolation for 5D functions.',
     'Miscellaneous'),
]

# -- Options for Epub output -------------------------------------------------

epub_title = project
epub_author = author
epub_publisher = author
epub_copyright = copyright
epub_exclude_files = ['search.html']
