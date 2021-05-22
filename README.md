# Data analysis
- Document here the project: email_sorter
- Description: Project Description
- Data Source:
- Type of analysis:

Please document the project the better you can.

# Startup the project

The initial setup.

Create virtualenv and install the project:
```bash
sudo apt-get install virtualenv python-pip python-dev
deactivate; virtualenv ~/venv ; source ~/venv/bin/activate ;\
    pip install pip -U; pip install -r requirements.txt
```

Unittest test:
```bash
make clean install test
```

Check for email_sorter in gitlab.com/{group}.
If your project is not set please add it:

- Create a new project on `gitlab.com/{group}/email_sorter`
- Then populate it:

```bash
##   e.g. if group is "{group}" and project_name is "email_sorter"
git remote add origin git@github.com:{group}/email_sorter.git
git push -u origin master
git push -u origin --tags
```

Functionnal test with a script:

```bash
cd
mkdir tmp
cd tmp
email_sorter-run
```

# Install

Go to `https://github.com/{group}/email_sorter` to see the project, manage issues,
setup you ssh public key, ...

Create a python3 virtualenv and activate it:

```bash
sudo apt-get install virtualenv python-pip python-dev
deactivate; virtualenv -ppython3 ~/venv ; source ~/venv/bin/activate
```

Clone the project and install it:

```bash
git clone git@github.com:{group}/email_sorter.git
cd email_sorter
pip install -r requirements.txt
make clean install test                # install and test
```
Functionnal test with a script:

```bash
cd
mkdir tmp
cd tmp
email_sorter-run
```
