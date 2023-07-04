# Translator
A telegram bot that can translate texts to 90 different languages. It is based on YandexTranslate API.
___
## Installation
To install this project you need to clone it from this github repo
```
git clone https://github.com/bitwopi/Translator.git
```
After you need to create virtual environment in project directory.

 __For windows:__

```
python -m venv venv
venv\Scripts\activate
```
__For Linux:__
```
python -m venv venv
source venv/bin/activate
```

When venv already created you need to install a project dependencies.
```
pip install -r requirements.txt
```

___
## .env
To start up project you need to setup env variables
To do this you need to create .env file in project folder and assign values to variables.
```
IAM_TOKEN="your yandex IAM_TOKEN"
FOLDER_ID="your yandex folder_id"
API_TOKEN="your telegram API_TOKEN"
```

## Migrations
When it's done you want to make migrations and migrate. To do this you need to be in the root directory of a project.
if you don't want to use my alembic configuration you can delete alembic directory and alembic.ini file. 
And then execute this commands:
```
alembic init alembic_directory_name
alembic revision --autogenerate -m "name of migration"
alembic upgrade head
```
If you are using my configuration you need to execute this command:
```
alembic upgrade head
```
## Run
To run application you need to run main.py file.
```
python main.py
```

## Tests
To run tests you need to configure root directory paths and then run tests.



