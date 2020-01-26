
# Python's Libraries
import os
import enum
import logging
import logging.config

# Third-party Libraries
from pathlib import Path
import yaml


# Set Logger
src_path = os.path.dirname(__file__)
config_file = f"{src_path}/config.yaml"

with open(config_file, 'r') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

logger = logging.getLogger(__name__)


class Types(enum.Enum):
    FILE = "file"
    FOLDER = "folder"


class Archive(object):

    def __init__(self, _path):
        self.path = _path

    def __str__(self):
        return self.path

    @property
    def name(self):
        name = Path(self.path).parts[-1]
        return name

    @property
    def parent_path(self):
        path_obj = Path(self.path)
        parent_path = path_obj.resolve().parent

        return f'{str(parent_path)}/'

    def exist(self, _check_type=None):
        if _check_type is None:
            msg_error = "You need provide a type to check"
            logger.error(msg_error)
            raise NameError(msg_error)

        if _check_type == Types.FOLDER:
            return os.path.isdir(self.path)

        if _check_type == Types.FILE:
            return os.path.isfile(self.path)


class Folder(Archive):

    def __init__(self, _path):
        Archive.__init__(self, _path)

    def exist(self):
        exist = super().exist(Types.FOLDER)
        return exist

    def delete(self):
        if self.exist() is False:
            msg_error = (
                f"File {self.path} does not exist "
                f"in {self.parent_path}"
            )
            logger.error(msg_error)
            raise NameError(msg_error)


class File(Archive):

    def __init__(self, _path):
        Archive.__init__(self, _path)

    @property
    def title(self):
        name = self.name
        title = os.path.splitext(name)[0]
        return title

    @property
    def extension(self):
        name = self.name
        extension = os.path.splitext(name)[1]
        return extension

    def exist(self):
        exist = super().exist(Types.FILE)
        return exist




# Note: os.path.exists() function may return False, if permission is not granted to execute os.stat() on the requested file, even if the path exists.