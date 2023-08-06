import json
import os

from bentoml.exceptions import (
    InvalidArgument,
    MissingDependencyException,
)
from bentoml.service import BentoServiceArtifact
import torch


class SimpleTransformersModelArtifact(BentoServiceArtifact):

    def __init__(self, name):
        super(SimpleTransformersModelArtifact, self).__init__(name)
        print('SimpleTransformersModelArtifact name:', name)
        self._model = None

    def _file_path(self, base_path):
        return os.path.join(base_path, self.name)

    def _load_from_directory(self, path, opts):
        print('opts:', json.dumps(opts, indent=4))
        try:
            classname = opts['classname']
            mod = __import__(opts['classpackage'], fromlist=[classname])
            clz = getattr(mod, classname)
        except Exception as e:
            print(str(e))
            raise MissingDependencyException(
                'a simpletransformers.classification model is required to use SimpleTransformersModelArtifact'
            )

        kwargs = {
            'model_type': 'roberta',
            'num_labels': 33,
            'args': {
                'use_multiprocessing': False,
                'silent': True,
            },
            'use_cuda': False,
        }
        kwargs.update(opts)

        self._model = clz(
            opts.get('model_type', 'roberta'),
            self._file_path(path),
            **kwargs
        )
    
    def _load_from_dict(self, model):
        if not model.get('model'):
            raise InvalidArgument(
                "'model' key is not found in the dictionary. "
                "Expecting a dictionary with keys 'model'"
            )

        self._model = model

    def _save_package_opts(self, path, opts):
        with open(os.path.join(path, 'package_opts.json'), 'w') as f:
            json.dump(opts, f)

    def pack(self, model, opts=None):
        if opts is None:
            opts = {}

        if isinstance(model, str):
            if os.path.isdir(model):
                self._load_from_directory(model, opts)
            else:
                raise InvalidArgument('Expecting a path to the model directory')
        elif isinstance(model, dict):
            self._load_from_dict(model)
        else:
            raise InvalidArgument('Expecting model to be a path to the model directory or a dict')

        self._save_package_opts(model, opts)
        return self

    def load(self, path):
        path = self._file_path(path)
        with open(os.path.join(path, 'package_opts.json'), 'r') as f:
            opts = json.load(f)

        return self.pack(path, opts)

    def save(self, dst):
        path = self._file_path(dst)
        os.makedirs(path, exist_ok=True)
        model = self._model.model
        model_to_save = model.module if hasattr(model, 'module') else model
        model_to_save.save_pretrained(path)
        self._model.tokenizer.save_pretrained(path)
        torch.save(self._model.args, os.path.join(path, 'training_args.bin'))
        return path

    def get(self):
        return self._model
