See original README from fork at [./fork_readme.md](./fork_readme.md)


# Getting started
```sh
# Clone the repo
git clone git@github.com:AndrewCloete/ds_code_challenge.git && cd ds_code_challenge

# Start a new virtual environment
rm -rf env # Remove any existing virtual environment
python3 -m venv env
activate
# or
source env/bin/activate

# Ensure the virtual environment is active
which python
# Be sure it points to <project-dir>/env/bin/python

# Restore dependencies
pip install -r requirements.txt

# Add your access credentials
vim .secrets.json
# Paste in the content from the super-duper secure link at
# https://cct-ds-code-challenge-input-data.s3.af-south-1.amazonaws.com/ds_code_challenge_creds.json
```

# Running the code
```sh
python src/main.py
```


# Cleaning up