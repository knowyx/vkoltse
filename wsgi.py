"""This module was an entry point (EP) of site. Gunicorn runs through
that file"""

import os
import runpy

BASE_DIR = "/home/knowyx/proj/py/vkoltse3/vkoltse"

module = runpy.run_path(os.path.join(BASE_DIR, "index.wsgi"))
application = module["application"]
