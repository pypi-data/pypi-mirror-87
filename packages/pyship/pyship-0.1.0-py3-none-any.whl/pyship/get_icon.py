from typing import Tuple, Callable
from pathlib import Path
import shutil

from typeguard import typechecked

from pyship import AppInfo, get_logger, __application_name__
import pyship

log = get_logger(__application_name__)


@typechecked()
def get_icon(target_app_info: AppInfo, ui_print: Callable) -> Path:
    """
    find either the target project's icon or the provided icon from pyship
    :param target_app_info: target app info
    :param ui_print: this function is called with a string to update the UI
    :return: icon's path
    """

    icon_file_name = f"{target_app_info.name}.ico"
    icon_paths = [
        # First try to use the icon provided by the target app
        Path(target_app_info.project_dir, icon_file_name).absolute(),
        Path(target_app_info.project_dir, target_app_info.name, icon_file_name).absolute(),
        # use pyship's icon if the target app doesn't have one (make this the last entry in this list)
        Path(Path(pyship.__file__).parent, f"{__application_name__}.ico").absolute(),
    ]

    icon_path = None
    for icon_path in icon_paths:
        if icon_path.exists():
            break

    if icon_path == icon_paths[-1]:
        s = f"{target_app_info.name} does not include its own icon - using {__application_name__} icon ({icon_path})"
        log.info(s)
        ui_print(s)

    return icon_path
