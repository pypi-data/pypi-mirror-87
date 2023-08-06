"""
`aiplugins.commons` module gathers base definitions
"""

from ._definitions import DATA_DIR, MODELS_DIR, PLOTS_DIR, ROOT_DIR, cloud_template_file
from ._utils import clean_input, create_word_cloud

__all__ = ['DATA_DIR',
           'MODELS_DIR',
           'PLOTS_DIR',
           'ROOT_DIR',
           'cloud_template_file',
           'clean_input',
           'create_word_cloud'
           ]