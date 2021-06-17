import os
from pathlib import Path


pwd = str(Path(__file__).parent.absolute())
path = pwd + "/champion"
files = [file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))]

for file in files:
    os.rename(os.path.join(path, file.lower()), os.path.join(path, file))
    print(f"Renamed {file}")
