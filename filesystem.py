
# Python's Libraries
import os
import enum
import shutil
import logging

# Third-party Libraries
from pathlib import Path
from bs4 import BeautifulSoup


class Types(enum.Enum):
    FILE = "file"
    FOLDER = "folder"


class Archive(object):

    def __init__(self, _path, _logger=None):
        self.path = _path
        self.logger = _logger or logging.getLogger(__name__)

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
        self.logger.info(
            f"Checking if {self.name} exist "
            f"in {self.parent_path}."
        )

        if _check_type is None:
            msg_error = "You need provide a type to check"
            self.logger.error(msg_error)
            raise NameError(msg_error)

        if _check_type == Types.FOLDER:
            return os.path.isdir(self.path)

        if _check_type == Types.FILE:
            return os.path.isfile(self.path)

    def move_To(self, _to_path):
        self.logger.info(
            f"Moving {self.name} to "
            f"{_to_path}"
        )
        shutil.move(self.path, _to_path)


class Folder(Archive):

    def __init__(self, _path, _logger=None):
        Archive.__init__(self, _path, _logger)
        self.type = Types.FOLDER

    def exist(self):
        exist = super().exist(Types.FOLDER)
        return exist

    def delete(self):
        self.logger.info(
            f"Deleting {self.name} on "
            f"in {self.parent_path}."
        )

        shutil.rmtree(self.path)

    def get_Content(self, _name=None):
        label_name = f"with name '{_name}'" if _name else ""
        self.logger.info(
            f"Retrieving object(s) of {self.path} {label_name}"
        )
        list_objects = []
        elements = os.walk(self.path)

        for current_path, children_folders, children_files in elements:
            for folder_name in children_folders:
                if _name:
                    if folder_name != _name:
                        continue

                path = os.path.join(current_path, folder_name)
                list_objects.append(Folder(path, self.logger))

            for file_name in children_files:
                if _name:
                    if file_name != _name:
                        continue

                path = os.path.join(current_path, file_name)
                list_objects.append(File(path, self.logger))

        return list_objects

    def get_Files(self, _name=None, _extension=None):
        label_name = f"with name '{_name}'" if _name else ""
        label_ext = f"and extension '{_extension}'" if _extension else ""
        self.logger.info(
            f"Retrieving file(s) of {self.path} {label_name} {label_ext}"
        )
        list_objects = []
        elements = os.walk(self.path)

        for current_path, children_folders, children_files in elements:
            for file_name in children_files:
                if _name:
                    if file_name != _name:
                        continue

                if _extension:
                    (title, extension) = os.path.splitext(file_name)

                    if _extension != extension:
                        continue

                path = os.path.join(current_path, file_name)
                list_objects.append(File(path, self.logger))

        return list_objects

    def get_Folders(self, _name=None):
        label_name = f"with name '{_name}'" if _name else ""
        self.logger.info(
            f"Retrieving folder(s) of {self.path} {label_name}"
        )
        list_objects = []
        elements = os.walk(self.path)

        for current_path, children_folders, children_files in elements:
            for folder_name in children_folders:
                if _name:
                    if folder_name != _name:
                        continue

                path = os.path.join(current_path, folder_name)
                list_objects.append(Folder(path, self.logger))

        return list_objects


class File(Archive):

    def __init__(self, _path, _logger=None):
        Archive.__init__(self, _path, _logger)
        self.type = Types.FOLDER
        self.content = None

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

    def delete(self):
        self.logger.info(
            f"Deleting {self.name} on "
            f"in {self.parent_path}."
        )
        os.remove(self.path)

    def read(self):
        if self.extension.upper() in ['.XML', '.HTML']:
            try:
                file_obj = open(self.path, 'r')
                self.content = BeautifulSoup(
                    file_obj.read(),
                    features=self.extension.replace('.', '')
                )

            except Exception as e:
                raise NameError(str(e))
        else:
            msg_error = f'Extensión {self.extension} aun no soportada'
            self.logger.error(msg_error)
            raise NameError(msg_error)


class FileAdmin(object):

    def __init__(self, _init_path, _logger=None):
        self.origin_folder = Folder(_init_path, _logger)
        self.logger = _logger or logging.getLogger(__name__)

    def move_FilesTo(self, _to_path, _extension=None):
        self.logger.info(
            f"Moviendo archivos con extension {_extension} "
            f"a {_to_path}"
        )
        if self.origin_folder.exist() is False:
            self.logger.error("No existe la carpeta origen")

        to_folder = Folder(_to_path, self.logger)
        if to_folder.exist() is False:
            self.logger.error("No existe la carpeta origen")

        list_objects = self.origin_folder.get_Files(_extension=".ogg")
        self.logger.info(f"{len(list_objects)} Encontrados")

        cont = 0
        for obj in list_objects:
            obj.move_To(to_folder.path)
            cont += 1

        self.logger.info(f"Se movieron {cont} archivos")
