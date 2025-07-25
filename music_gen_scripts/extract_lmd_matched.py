import tarfile
import os

archive_path = os.path.join('data', 'lmd_matched.tar.gz')
extract_path = os.path.join('data')

with tarfile.open(archive_path, 'r:gz') as tar:
    tar.extractall(path=extract_path)
    print(f'Extracted {archive_path} to {extract_path}') 