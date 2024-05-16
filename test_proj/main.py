import argparse
import numpy as np
import pandas as pd
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_images_dir", type = str)
    parser.add_argument("--dataset_pickle_path", type = str)
    parser.add_argument("--target_image_path", type = str)
    parser.add_argument("--target_pickle_path", type = str)
    args = parser.parse_args()

    dataset_images_dir = args.dataset_images_dir
    dataset_pickle_path = args.dataset_pickle_path
    target_image_path = args.target_image_path
    target_pickle_path = args.target_pickle_path

    dataset_df = pd.read_pickle(dataset_pickle_path)
    target_df = pd.read_pickle(target_pickle_path)

if __name__ == '__main__':
    main()
