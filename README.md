# UserStudyPoC

## Data
Add Data (dataset or grid images) into static/userStudyData/POC_dataset or POC_grid folder with their csv file which imPath is linked to static/userStudyData/...


## link to the data
go to userStudyPOC_with_reset.py/init_user_dataset_file(...) and link the right cvs file name inside this function


## output
output csv file will be stored into static/ouput folder


## Installation

After clonning the repository you need to create a virtual environment:

```
python3 -m venv .venv && \
.venv/bin/python -m pip install --upgrade pip && \
.venv/bin/python -m pip install -r requirements.txt
```

## Running the servers

After creating the virtual environment you can do:

```
.venv/bin/python app.py
```

### Note

You can run this from tmux or screen so you don't kill the process when leaving the server.
