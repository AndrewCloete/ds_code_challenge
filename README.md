See original README from fork at [./fork_readme.md](./fork_readme.md)

# Declaration
I declare that this is my own work and that all sources that I have used are
indicated and acknowledged by means of references. I have not consulted any
prior attempts at this exercise. Github Copilot was enabled during the
development of this project. 

# Expectation and context
Thank you for a well thought out and structured exercise. I've enjoyed it.

Using this exercise as a reference, it seems that there may be a slight
misalignment in my expectation for this role. I've assumed that the
responsibilities of this would more to do with the design, implementation and
maintenance of OLAP systems, as opposed to the wrangling of the data for local
of analysis. Consequently, I had to brush off my rusty Pandas and matplotlib
skills and rediscovered the pains of Jupyter notebooks. But, I also understand
that these exercises can only be proxies and naturally need be limited in scope
and time so I look forward to discussing the full scope of the role with you.

# Requirements
- Python 3.10.* 
- venv

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

# Troubleshooting
If you get an error during install complaining about "gdal-config" not found,
please see:
https://stackoverflow.com/questions/65716089/no-such-file-or-directory-gdal-config

# Testing the repositories
Data access has been abstracted into repositories so that the logic in the notebook can stay in the business layer. Please run the test to ensure the repositories are configured correctly. These will also cache some data locally to speed up the notebook. 
```sh
python src/integration_test.py
```

# Running the notebook
I settled on using Jupyter notebooks as a way to document the process. One would
obviously not use a notebook in a production pipeline. (Personally, I'm not a
big fan of notebooks so I'm not sure why I did this to myself). You can run the
notebook by running the following command in the root of the project and
selecting `notebook.ipynb`. 
```sh
python -m jupyter notebook
```
I prefer to run the notebook in VSCode. On opening, VSCode will prompt you to select the virtual environment to run the kernel. This assumes you have the Jupyter extension installed. 


# Request for visibility on process time
Since the Jupyter notebook in VScode cells show the execution time, I've split
the cells so as to easily see the time for specific operations as requested. If running in the browser I've added the `%%time` magic command to the relevant cells.

I've added local file caching logic to some of the repositories to speed things
up so don't be alarmed as execution time variance.
