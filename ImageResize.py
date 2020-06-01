# Python's Libraries
from PIL import Image
import os
from io import BufferedReader


class ImageResize:

    def __init__(self, _image_object, _filename, _format="jpeg", _convert_mode="RGB",
                 _optimize=True, _quality=30, _tmp_folder='media/'):
        self.image_object = self.extract_File(_image_object)
        self.file_name = _filename
        self.file_extension = _format
        self.optimize = _optimize
        self.quality = _quality
        self.path_folder = _tmp_folder

        self.convert_ToMode(_convert_mode)

    def convert_ToMode(self, _convert_mode):
        if self.image_object.mode != _convert_mode:
            self.image_object = self.image_object.convert(_convert_mode)

    def extract_File(self, _image):
        if type(_image) == BufferedReader:
            return Image.open(_image)
        else:
            return Image.open(_image.file)

    def get_Resized(self, width, heigth):
        resized_image = self.image_object.resize((width, heigth))
        filename = self.file_name
        path = self.get_PathFile(filename)
        resized_image.save(
            path, format=self.file_extension
        )
        file = open(path, 'rb')
        os.remove(path)
        return file

    def get_InMaxSize(self, width, heigth):
        image_width, image_heigth = self.image_object.size
        if image_heigth > heigth or image_width > width:
            resized_image = self.image_object.resize((width, heigth))
        else:
            resized_image = self.image_object
        filename = self.file_name
        path = self.get_PathFile(filename)
        resized_image.save(
            path, format=self.file_extension
        )
        file = open(path, 'rb')
        os.remove(path)
        return file

    def get_Optimized(self):
        filename = self.file_name
        path = self.get_PathFile(filename)
        self.image_object.save(
            path, format=self.file_extension,
            optimize=self.optimize, quality=self.quality)
        file = open(path, 'rb')
        os.remove(path)
        return file

    def get_PathFile(self, filename):
        if filename:
            path = os.path.relpath(
                self.path_folder + filename + '.' + self.file_extension)
        else:
            path = os.path.relpath(
                self.path_folder + self.file_name + '.' + self.file_extension)
        return path
