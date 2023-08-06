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

        self._model = clz(
            opts.get('model_type', 'roberta'),
            self._file_path(path),
            num_labels=opts.get('num_labels', 33),
            pos_weight=opts.get('pos_weight', None),
            args=opts.get('args', {
                'use_multiprocessing': False,
                'silent': True,
            }),
            use_cuda=opts.get('use_cuda', False),
            cuda_device=opts.get('cuda_device', None)
        )

    def _save_package_opts(self, path, opts):
        with open(os.path.join(path, 'package_opts.json'), 'w') as f:
            json.dump(opts, f)

    def pack(self, model, opts):
        if isinstance(model, str):
            if os.path.isdir(model):
                self._save_package_opts(model, opts)
                self._load_from_directory(model, opts)
                return self
        
        raise InvalidArgument('Expecting a path to the model directory')

    def load(self, path):
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
