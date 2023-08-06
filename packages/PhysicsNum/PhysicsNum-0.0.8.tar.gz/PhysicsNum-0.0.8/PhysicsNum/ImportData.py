import numpy as np
import pandas as pd

def ImportCSV(Filepath):
    """Returns all data for an iterated Panda Dataframe"""
    try:
        PandaFrame = pd.read_csv(Filepath)
    except Exception as E:
        raise E
    SizeOfPandaFrame = PandaFrame.size
    KeysPandaFrame = PandaFrame.keys()
    Data = [PandaFrame[key] for keys in KeysPandaFrame]
    return Data
