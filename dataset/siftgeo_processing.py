import numpy as np
import os
from tqdm.auto import tqdm

def siftgeo_read(filename, maxdes=None):
    if maxdes is None:
        maxdes = 100000000  # Large number as default
    
    with open(filename, 'rb') as f:
        f.seek(0, 2)
        total_size = f.tell()
        descriptor_size = (9 * 4 + 1 * 4 + 128)
        num_descriptors = total_size // descriptor_size
        num_descriptors = min(num_descriptors, maxdes)
        f.seek(0)
        
        meta = np.zeros((num_descriptors, 9), dtype=np.float32)
        v = np.zeros((num_descriptors, 128), dtype=np.float32)
        
        for i in range(num_descriptors):
            meta[i, :] = np.fromfile(f, dtype=np.float32, count=9)
            d = np.fromfile(f, dtype=np.int32, count=1)
            if d[0] != 128:
                raise ValueError("Expected 128 SIFT features but got {}".format(d[0]))
            v[i, :] = np.fromfile(f, dtype=np.uint8, count=d[0]).astype(np.float32)
    
    return v, meta

def load_key_desc_from_file(filename):
    keypoints = []
    descriptors = []
    
    with open(filename, 'r') as file:
        lines = file.readlines()[2:]  
        
    for line in lines:
        numbers = list(map(float, line.split()))
        keypoints.append(numbers[0:5])
        descriptors.append(numbers[5:])
    
    keypoints = np.array(keypoints)
    descriptors = np.array(descriptors)
    
    return descriptors, keypoints

def read_all_siftgeo(directory, maxdes=None):
    results = {}
    for filename in tqdm(os.listdir(directory)):
        if filename.endswith(".siftgeo"):
            filepath = os.path.join(directory, filename)
            descriptors, metadata = siftgeo_read(filepath, maxdes)
            results[filename] = (descriptors, metadata)
    return results

def read_all_sift(directory, maxdes=None):
    results = {}
    for filename in tqdm(os.listdir(directory)):
        if filename.endswith(".sift"):
            filepath = os.path.join(directory, filename)
            descriptors, metadata = load_key_desc_from_file(filepath)
            results[filename] = (descriptors, metadata)
    return results

if __name__ == '__main__':
    directory_path1 = '/home/leohsu-cs/siftgeo'
    all_files_data = read_all_siftgeo(directory_path1, maxdes=5000)

    directory_path2 = '/home/leohsu-cs/keypoints'
    all_files_data2 = read_all_sift(directory_path2)
    
    # for filename, data in tqdm(all_files_data.items()):
    #     print(f"File: {filename}")
    #     print("Descriptors:")
    #     print(data[0])
    #     print(data[0].shape)
    #     print("Metadata:")
    #     print(data[1])
    #     print(data[1].shape)

    length = len(all_files_data)
    keys1 = sorted(list(all_files_data.keys()))
    keys2 = sorted(list(all_files_data2.keys()))

    for i in range(length):
        filename1 = keys1[i][:5]
        filename2 = keys2[i][:5]
        print(filename1, filename2)
        
        data1 = all_files_data[keys1[i]]
        data2 = all_files_data2[keys2[i]]
        print(f"File: {filename1}", data1[0].shape, data2[0].shape)
