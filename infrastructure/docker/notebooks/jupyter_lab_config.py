import os
import pathlib
from datetime import datetime

import psutil
import requests

from paystone.storage import PSStorage

COMMON_BASEDIR = pathlib.Path("common-notebooks")
PERSONAL_BASEDIR = pathlib.Path("personal-notebooks")
FILEPATH_ROOT = pathlib.Path("/home/paystone/work")

# get user email once at the beginning of JupyterLab setup from the metadata server
user_email = os.getenv("USERNAME", None)

c.ServerApp.token = "paystone"
c.ServerApp.password = ""

storage = PSStorage()


def upload_to_gcs_on_save(model, os_path, contents_manager, **kwargs):
    """Save both the current version of the notebook and a timestampped version to GCS."""
    notebook_path = pathlib.Path(os_path)

    # 1. don't save untitled notebooks
    if notebook_path.stem == "Untitled":
        contents_manager.log.info("Not saving an untitled notebook to GCS bucket")
        return

    # 2. don't save empty folders
    if os.path.isdir(os_path):
        contents_manager.log.info("Not saving a new folder to GCS bucket")
        return

    # 3. get notebook content to save
    with open(model["path"]) as notebook_file:
        content = notebook_file.read()

    # 4. is it a personal notebook?
    personal = "personal" in notebook_path.parts

    # 5. parse path for useful components
    relpath = pathlib.Path(*notebook_path.relative_to(FILEPATH_ROOT).parts[1:])
    filedir = relpath.parent
    filestem = notebook_path.stem
    fileext = notebook_path.suffix

    # 4. save a versioned edition of the notebook in versions/ if a common notebook
    if not personal:
        version_filestem = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        version_filepath = (
            COMMON_BASEDIR / "versions" / filedir / filestem / (version_filestem + fileext)
        )
        storage.write(content=content, target=str(version_filepath))

    # 5. save the notebook in place in GCS bucket
    if personal:
        if user_email is not None:
            filepath = PERSONAL_BASEDIR / user_email / (str(filestem) + str(fileext))
            storage.write(content=content, target=str(filepath))
            contents_manager.log.info(f"Saving {filepath} to GCS bucket")
        else:
            # save to sandbox on GCS only from Vertex Notebooks instance, not from local
            contents_manager.log.info("Not writing to GCS bucket from the local sandbox directory")
    else:
        filepath = COMMON_BASEDIR / filedir / (str(filestem) + str(fileext))
        storage.write(content=content, target=str(filepath))
        contents_manager.log.info(f"Saving {filepath} to GCS bucket")


c.FileContentsManager.post_save_hook = upload_to_gcs_on_save
c.ServerApp.allow_origin = "*"

# extension configuration

c.ResourceUseDisplay.mem_limit = psutil.virtual_memory().total
