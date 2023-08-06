ZeroLoader
==

ZeroLoader is a part of [0archive project](https://0archive.tw/). Its purpose is to read 0archive's public data from [google drive](https://drive.google.com/drive/u/1/folders/1ckDs03tdXhLdeF0N2St5OP0EeqxFC1bm) into csv format.

## Setup
 
1. Get google api credentials

    Follow Step 1 from [this tutorial](https://developers.google.com/drive/api/v3/quickstart/python).

2. Installation
    It's recommended to use a [virtualenv](https://docs.python-guide.org/dev/virtualenvs/) or [conda env](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html).
     
    ```shell script
    $ pip install -U zeroloader.py
    ```

3. Create environment file

    ```shell script
    touch .env
    echo GDRIVE_PUBLIC_FILE_MAPPING_ID=1OwAGYg7dJob_VMW8vt2FP4fO5Ie7B3EW > .env
    ```

4. Load data

    You need the producer_id to successfully load. The id of each producer could be found from google drive folder name or from this [csv](https://drive.google.com/file/d/1JpHclJLrfRO1Yz5oiPdfacEWggUoGTes/view?usp=sharing).
    
    ```python
    import zeroloader as zl
 
    df = zl.load_data(:producer_id, :yyyy-mm, :path-to-gdrive-api-credentials)
   
    # e.g. Load 2020 June's data of storm.mg into a csv
    df = zl.load_data("5030bba7-81fe-11ea-8627-f23c92e71bad", "2020-06", "service.json") 
    ```