import os
import shutil

shutil.copyfile(os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png"),
                os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"), "entry.png"))
