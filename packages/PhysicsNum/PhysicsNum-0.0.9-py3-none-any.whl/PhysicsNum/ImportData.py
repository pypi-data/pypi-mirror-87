import numpy as np
try:
    import pandas as pd
except:
    print("[ImportData.py] Package pandas is not installed, and ImportCSV will therefore not work.")
def ImportCSV(Filepath):
    """Returns all data for an iterated Panda Dataframe, only works with file extensions such as
    .txt and .csv. Works upon the package pandas""""
    try:
        PandaFrame = pd.read_csv(Filepath)
    except Exception as E:
        raise E
    SizeOfPandaFrame = PandaFrame.size
    KeysPandaFrame = PandaFrame.keys()
    Data = [PandaFrame[key] for keys in KeysPandaFrame]
    return Data

def ImportTXT(FilePath):
    """Uses python standard open function, it returns the entire content of the file, so a parser might have to be in order."""
    try:
        with open(FilePath, 'r') as file:
            return(file.read())
    except Exception as e:
        raise e
