See original README from fork at [./fork_readme.md](./fork_readme.md)

# Declaration
I Andrew Cloete, hereby declare that this is my own work and that all sources
that I have used are indicated and acknowledged by means of references. Github
Copilot was enabled during the development of this project. 


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

# Running the notebook
You can run the notebook by running the following command in the root of the project and selecting the notebook
```sh
python -m jupyter notebook
```
Personally, I prefer to run the notebook in VSCode. On opening, VSCode will prompt you to select the virtual environment to run the kernel. This assumes you have the Jupyter extension installed. 


# Request for visibility on process time
Since the Jupyter notebook cells show the execution time, I've split the cells
so as to easily see the time for specific operations as requested.

I've added local file caching logic to some of the repositories to speed things up so don't be alarmed as execution time variance.
