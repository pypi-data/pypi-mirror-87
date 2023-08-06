import os

ROOT_DIR = os.environ.get("PLUGINS_HOME")
if ROOT_DIR is None:
    raise ValueError("please make sure to setup the environment variable PLUGINS_HOME to point for the root of the project")
MODELS_DIR = os.path.join(ROOT_DIR, "saved_models")
PLOTS_DIR = os.path.join(ROOT_DIR, "saved_performance")
DATA_DIR = os.path.join(ROOT_DIR, "saved_datasets")
cloud_template_file = os.path.join(DATA_DIR, "cloud.png")

