# torchmojiartifact

BentoML artifact framework for the Torchmoji Model.

Installation:

    pip install torchmojiartifact==0.0.1

Usage example (decorate service):

    from torchmojiartifact.TorchmojiModelArtifact import TorchmojiModelArtifact

    @artifacts([TorchmojiModelArtifact('emojify')])
    class MyBentoService(BentoService):


Usage example (package model):

    svc = MyBentoService()

    svc.pack('emojify', model_path)

Alternatively, during training:

    svc.pack('emojify', {'state_dict': my_state_dict, 'emoji_list': my_emoji_list, 'pax_list': my_pax_list, 'vocabulary': my_vocab})
