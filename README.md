# ez2share
----

__ez2share__ is a file-sharing system based on [Django](https://www.djangoproject.com/).

## Install

First, you'll need to install Django (see [here](https://www.djangoproject.com/download/)) with python 3.

Then, clone this project.
```
git clone https://github.com/Yepikae/ez2share.git
```


## Use

### Create a new repository

In the root of *ez2share*, the following command creates a new repository. A password is required.

```
python manage.py create_repo --password=123
```

You can choose a specific name for your repository, if you don't want a random one.

```
python manage.py create_repo --name=myrepo --password=123
```
