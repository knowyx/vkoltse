import os
import runpy

BASE_DIR = os.path.dirname(__file__)

module = runpy.run_path(os.path.join(BASE_DIR, "index.wsgi"))
application = module["application"]
