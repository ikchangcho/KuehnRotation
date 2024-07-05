import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob

def load_data(filename_pattern, indices=None):
    files = sorted(glob.glob(filename_pattern))
    if indices is None:
        indices = range(len(files))
    data_list = []
    for idx in indices:
        if idx < len(files):
            data = pd.read_csv(files[idx]).values
            data_list.append(data)
        else:
            print(f"Index {idx} is out of range for available files.")
    return data_list

if __name__ == "__main__":
    data_list = load_data("data_to_plot*.csv", indices=[1, 2, 3])
    print(data_list)