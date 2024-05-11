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

def read_all_siftgeo(directory, maxdes=None):
    results = {}
    for filename in tqdm(os.listdir(directory)):
        if filename.endswith(".siftgeo"):
            filepath = os.path.join(directory, filename)
            descriptors, metadata = siftgeo_read(filepath, maxdes)
            results[filename] = (descriptors, metadata)
    return results

if __name__ == '__main__':
    directory_path = '/home/leohsu-cs/siftgeo'
    all_files_data = read_all_siftgeo(directory_path, maxdes=5000)
    
    for filename, data in tqdm(all_files_data.items()):
        print(f"File: {filename}")
        print("Descriptors:")
        print(data[0])
        print("Metadata:")
        print(data[1])
