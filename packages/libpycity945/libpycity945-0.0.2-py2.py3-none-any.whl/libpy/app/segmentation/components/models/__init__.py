from .HardNet import HardNet
from .ERFNet import ERFNet

def get_model(name):
    return {
        "HardNet": HardNet,
        "ERFNet": ERFNet,
    }[name]
