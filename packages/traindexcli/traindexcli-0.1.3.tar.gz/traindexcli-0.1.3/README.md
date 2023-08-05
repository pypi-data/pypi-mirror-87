## Traindex-cli

Traindex-cli is the tool for uploading the dataset to Foretheta-devop s3 bucket. You can install it as follows.


### How to install.
Nevigate to this folder using terminal and run the following commands in sequence.

1. `$ python3 setup.py install`
2. `$ python3 setup.py sdist bdist_wheel`
3. `pip install -e .`

it will install the package to your computer.

### Usage.

`$ traindex_cli --filename=PATH_TO_FILE_TO_UPLOAD --foldername=FOLDER_ON_S3_FOR_YOUR_FILE`

### Requirements.
You need to have the credentials in your OS for S3 bucket, which we will provide you.

