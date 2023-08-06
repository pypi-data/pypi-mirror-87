import json
import os

import torch
from bentoml.exceptions import InvalidArgument
from bentoml.service import BentoServiceArtifact


class TorchmojiModelArtifact(BentoServiceArtifact):

    def __init__(self, name):
        super(TorchmojiModelArtifact, self).__init__(name)
        self._model = None

    def _file_path(self, base_path):
        return os.path.join(base_path, self.name)
    
    def _load_from_dict(self, model):
        if not model.get('state_dict'):
            raise InvalidArgument(
                "'state_dict' key is not found in the dictionary. "
                "Expecting a dictionary with keys 'state_dict', 'emoji_list', 'pax_list', 'vocabulary'"
            )

        self._model = model

    def _load_from_directory(self, path):
        emoji_list = []
        with open(os.path.join(path, 'emoji_list.txt'), 'r') as f:
            for line in f:
                emoji_list.append(line.strip())

        pax_list = []
        with open(os.path.join(path, 'pax_list.txt'), 'r') as f:
            for line in f:
                pax_list.append(line.strip())
        
        with open(os.path.join(path, 'vocabulary.json'), 'r') as f:
            vocabulary = json.load(f)

        state_dict = torch.load(os.path.join(path, 'pytorch_model.bin'))
        self._model = {
            'state_dict': state_dict,
            'emoji_list': emoji_list,
            'pax_list': pax_list,
            'vocabulary': vocabulary,
        }

    def pack(self, model):
        if isinstance(model, str):
            if os.path.isdir(model):
                self._load_from_directory(model)
            else:
                raise InvalidArgument('Expecting a path to the model directory')
        else if isinstance(model dict):
            self._load_from_dict(model)

        if self._model is None:
            raise InvalidArgument('Expecting a pathor dict ')

        return self
    
    def load(self, path):
        path = self._file_path(path)
        return self.pack(path)
    
    def save(self, dest):
        path = self._file_path(dest)
        os.makedirs(path, exist_ok=True)

        with open(os.path.join(path, 'vocabulary.json'), 'w') as f:
            json.dump(self._model['vocabulary'], f)

        with open(os.path.join(path, 'pax_list.txt'), 'w') as f:
            for line in self._model['pax_list']:
                f.write('%s\n' % line)

        with open(os.path.join(path, 'emoji_list.txt'), 'w') as f:
            for line in self._model['emoji_list']:
                f.write('%s\n' % line)

        torch.save(self._model['state_dict'], os.path.join(path, 'pytorch_model.bin'))

    def get(self):
        return self._model
