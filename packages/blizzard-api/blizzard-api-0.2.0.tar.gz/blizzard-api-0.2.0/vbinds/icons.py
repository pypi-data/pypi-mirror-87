
"""
vbinds - Functions for downloading in-game icon image files.
"""

# built-in
import os
import logging
from typing import Optional

# third-party
import requests

# internal
from vbinds.enums import IconSize, get_icon_url

LOG = logging.getLogger(__name__)


def get_icon(name: str, dest_root: str = ".",
             size: IconSize = IconSize.LARGE,
             size_subdir: bool = True) -> Optional[str]:
    """
    Write an image file to disk for a given icon. Return the path written.
    """

    # start the icon-query stream
    req = requests.get(get_icon_url(name, size), stream=True)
    if req.status_code != requests.codes["ok"]:
        LOG.error("error getting icon '%s': %d %s", name, req.status_code,
                  req.text)
        return None

    # write the file contents
    dest_dir = dest_root
    if size_subdir:
        dest_dir = os.path.join(dest_root, str(size.value))
    os.makedirs(dest_dir, exist_ok=True)
    full_path = os.path.abspath(os.path.join(dest_dir, "{}.jpg".format(name)))
    with open(full_path, "wb") as img_fd:
        for chunk in req.iter_content(chunk_size=256):
            img_fd.write(chunk)

    LOG.info("wrote icon '%s' to '%s'", name, full_path)
    return full_path
