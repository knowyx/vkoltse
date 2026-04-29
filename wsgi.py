"""This module was an entry point (EP) of site. Gunicorn runs through
that file"""

import os
import runpy

BASE_DIR = "base_dir of project deploy"

module = runpy.run_path(os.path.join(BASE_DIR, "run_app.py"))
application = module["application"]
