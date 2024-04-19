import os
import sys

sys.path.append(os.path.abspath('..'))

project = 'ContactBook'
copyright = '2024, Student'
author = 'Student'

extensions = ['sphinx.ext.autodoc']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

autodoc_mock_imports = ["sqlalchemy"]

html_theme = 'classic'
html_static_path = ['_static']