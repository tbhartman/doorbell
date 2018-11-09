# -*- coding: utf-8 -*-
# import os
# import sys
# sys.path.insert(0, os.path.abspath(os.path.join('..','src')))


# -- Project information -----------------------------------------------------
project = 'doorbell'
copyright = '2018, Tim Hartman'
author = 'Tim Hartman'

# version handled by rtd
version = ''
release = ''


# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.coverage',
    'sphinx.ext.napoleon',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
language = None
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
pygments_style = None

autodoc_default_options = {
    'exclude-members': '_VisitorMethod',
    'member-order': 'bysource',
    'members': None,
    'private-members': None,
    'show-inheritance': None,
}
autosummary_generate = True

rst_epilog = '.. |project_name| replace:: %s' % project

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'
# html_theme_options = {}
html_static_path = ['_static']
# html_sidebars = {}

# -- Options for HTMLHelp output ---------------------------------------------
htmlhelp_basename = 'doorbelldoc'

# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # 'papersize': 'letterpaper',
    # 'pointsize': '10pt',
    # 'preamble': '',
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'doorbell.tex', 'doorbell Documentation',
     'Tim Hartman', 'manual'),
]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'doorbell', 'doorbell Documentation',
     [author], 1)
]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'doorbell', 'doorbell Documentation',
     author, 'doorbell', 'One line description of project.',
     'Miscellaneous'),
]


# -- Options for Epub output -------------------------------------------------

# Bibliographic Dublin Core info.
epub_title = project

# epub_identifier = ''
# epub_uid = ''

# A list of files that should not be packed into the epub file.
epub_exclude_files = ['search.html']

# -- Extension configuration -------------------------------------------------

todo_include_todos = True
