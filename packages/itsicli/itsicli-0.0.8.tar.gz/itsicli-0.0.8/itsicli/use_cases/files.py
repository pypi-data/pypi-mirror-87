import copy
import json
import os
from pathlib import Path

from itsimodels.core.base_models import ConfModel, ImageModel
from itsicli.use_cases.model_formats import to_conf, to_image, image_file_extension
from itsicli.use_cases.content_types import ContentTypes


USE_CASE_SCREENSHOTS_DIR = 'screenshots'


class UseCaseConfig(object):

    file_name = 'config.json'
    attr_id = 'id'
    attr_title = 'title'
    attr_description = 'description'
    attr_version = 'version'

    def __init__(self, home_path):
        self.path = home_path.joinpath(self.file_name)
        self.data = {}

        self.read()

    def read(self):
        if not self.exists():
            return

        with open(self.path, 'r') as fobj:
            contents = fobj.read()

        self.data = json.loads(contents)

    def update(self, data):
        self.data.update(data)

    def write(self):
        data = copy.deepcopy(self.data)

        data.setdefault(self.attr_description, '')
        data.setdefault(self.attr_version, '1')

        with open(self.path, 'w') as fobj:
            fobj.write(json.dumps(data, sort_keys=True, indent=4))

    def exists(self):
        return self.path.exists()

    def __getattr__(self, name):
        if name in (
                self.attr_id,
                self.attr_title,
                self.attr_description,
                self.attr_version
        ):
            return self.data.get(name)

        raise self.__getattribute__(name)


class UseCaseManifest(UseCaseConfig):

    file_name = 'manifest.json'
    attr_main_screenshot = 'main_screenshot'
    attr_screenshots = 'screenshots'

    def add_use_case_model(self, use_case_model):
        content_type = use_case_model.content_type
        content_objects = self.data.setdefault(content_type, [])

        file_name = str(use_case_model.model_file.file_name)
        content_objects.append(file_name)

    def write(self):
        data = copy.deepcopy(self.data)

        data.setdefault(self.attr_main_screenshot, {
            'thumb': None,
            'path': None
        })
        data.setdefault(self.attr_screenshots, [])

        for content_type in ContentTypes.keys():
            content_objects = data.get(content_type, [])
            if not content_objects:
                continue

            data[content_type] = sorted(list(set(content_objects)))

        with open(self.path, 'w') as fobj:
            fobj.write(json.dumps(data, sort_keys=True, indent=4))

    def __getattr__(self, name):
        if name in (
            self.attr_main_screenshot,
            self.attr_screenshots
        ):
            return self.data.get(name)

        raise self.__getattribute__(name)


class ModelFile(object):

    file_extension = 'json'

    def __init__(self, model):
        self.model = model

    @property
    def contents(self):
        json_str = json.dumps(self.model.to_dict(), sort_keys=True, indent=4)
        return json_str.encode('utf-8')

    @property
    def file_name(self):
        return Path(
            '{model_key}.{ext}'.format(
                model_key=self.model.get_key(),
                ext=self.file_extension
            )
        )


class ModelConfFile(ModelFile):

    file_extension = 'conf'

    @property
    def contents(self):
        return to_conf(self.model).encode('utf-8')


class ModelImageFile(ModelFile):

    @property
    def contents(self):
        return to_image(self.model)

    @property
    def file_extension(self):
        return image_file_extension(self.model)


class UseCaseModel(object):

    model_file_types = {
        ConfModel: ModelConfFile,
        ImageModel: ModelImageFile
    }

    @classmethod
    def create_model_file(cls, model):
        model_file_class = ModelFile

        for base_model_class, file_class in cls.model_file_types.items():
            if issubclass(model.__class__, base_model_class):
                model_file_class = file_class
                break

        return model_file_class(model)

    def __init__(self, root_path, model):
        self.root_path = root_path
        self.model_file = self.create_model_file(model)

    def write(self):
        path = self.path

        os.makedirs(path.parent, exist_ok=True)

        with open(path, 'wb') as fobj:
            fobj.write(self.model_file.contents)

    @property
    def content_type(self):
        for content_type, model_class in ContentTypes.items():
            if model_class == self.model_file.model.__class__:
                return content_type
        return None

    @property
    def path(self):
        content_type_dir = self.root_path.joinpath(self.content_type)

        return content_type_dir.joinpath(self.model_file.file_name)