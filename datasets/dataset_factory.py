# from srn import SRNDataset
# from .co3d import CO3DDataset

# from .nmr import NMRDataset
from .objaverse import ObjaverseDataset
from .front3d import Front3DDataset

from .gso import GSODataset


def get_dataset(cfg, name):
    # if cfg.data.category == "cars" or cfg.data.category == "chairs":
    #     return SRNDataset(cfg, name)
    # if cfg.data.category == "hydrants" or cfg.data.category == "teddybears":
    #     return CO3DDataset(cfg, name)
    # elif cfg.data.category == "nmr":
    #     return NMRDataset(cfg, name)
    if cfg.data.category == "objaverse":
        return ObjaverseDataset(cfg, name)
    elif cfg.data.category == "front3d":
        print("YOU SELECTED 3D-FRONT DATASET")
        return Front3DDataset(cfg, name)
    elif cfg.data.category == "gso":
        return GSODataset(cfg, name)
