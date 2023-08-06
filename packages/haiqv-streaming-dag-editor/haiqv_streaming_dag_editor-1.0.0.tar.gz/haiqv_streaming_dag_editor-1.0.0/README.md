# Code Editor Plugin for Haiqv-streaming
A plugin for [Apache Airflow](https://github.com/apache/airflow) that allows you to edit DAGs in browser.
It provides a file managing interface within specified directories and it can be used to edit and download your files.
The DAGs are stored in a Git repository. You may use it to view Git history, review local changes and commit.

[![PyPI version](https://badge.fury.io/py/airflow-code-editor.svg)](https://badge.fury.io/py/airflow-code-editor)
[![PyPI](https://img.shields.io/pypi/pyversions/airflow-code-editor.svg)](https://pypi.org/project/airflow-code-editor)
[![Downloads](https://pepy.tech/badge/airflow-code-editor/month)](https://pepy.tech/project/airflow-code-editor/month)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

### System Condition

* Airflow Versions
    * dev 2.0.0


### Deployment Instructions

1. Install the plugin in container 

    Add a below code on dockerflie for haiqv-streaming
    RUN pip install airflow-code-editor

2. Start Haiqv-streaming

3. Open Admin - DAGs Code Editor


### Config Options

You can edit your *airflow.cfg* adding any of the following settings in the \[code_editor\] section.

* **git_cmd**  git command (optional path)
* **git_default_args**  git arguments added to each call (default: -c color.ui=true)
* **git_author_name** human-readable name in the author/committer (default logged user first and last names)
* **git_author_email** email for the author/committer (default: logged user email)
* **git_init_repo**  initialize a git repo in DAGs folder (default: True)
* **root_directory**  root folder (default: Airflow DAGs folder)
* **mount_name**  configure additional file folder name (mount point)
* **mount_path**  configure additional file path

Example:
```
   [code_editor]
   git_cmd = /usr/bin/git
   git_default_args = -c color.ui=true
   git_init_repo = False
   root_directory = /home/airflow/dags
   mount_name = data
   mount_path = /home/airflow/data
   mount1_name = logs
   mount1_path = /home/airflow/logs
```

### Links

* Apache Airflow - https://github.com/apache/airflow
* Codemirror, In-browser code editor - https://github.com/codemirror/codemirror
* Git WebUI, A standalone local web based user interface for git repositories - https://github.com/alberthier/git-webui

