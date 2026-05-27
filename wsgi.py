"""This module was an entry point (EP) of site. Gunicorn runs through
that file"""

import os
import runpy

from config.cfg_handler import get_config_data

BASE_DIR = get_config_data("base-dir")

module = runpy.run_path(os.path.join(BASE_DIR, "run_app.py"))
application = module["application"]
