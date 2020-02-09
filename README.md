# Prerequisites
### Installation
This repo is tested on Python 3.6.8.
You should install this program on [conda](https://docs.conda.io/projects/conda/en/latest/index.html).<br>
If you're unfamiliar with conda, check out the [user guide](https://docs.conda.io/projects/conda/en/latest/user-guide/index.html). <br>
Create a conda environment with the version of Python you're going to use and activate it. <br>
You should also install the additional packages required by this project:

```
pip install -r requirements.txt
```
### Database
This project use [PostgreSQL](https://www.postgresql.org/) which has version 12.0 for purpose of saving data.  
Firstly, you must install PostgreSQL 12.0 and create a database with the following configurations:
```
dbuser='postgres'
dbpass=27101997
dbhost='localhost'
dbname='fact_checking'
``` 
Command line for creating `fact_checking` database with password `27101997`:
```
psql -U postgres -c "create database fact_checking" 
```
# Running
To run the app:<br>
```
python run.py
```
Your app will be run on the url: <!-- markdownlint-capture --> [http://localhost:5050/](http://localhost:5050/)
### Getting Started
If you first run the app, your database will be empty. So you need to import data from the `datasets` folder which contain a lot of claims. <br>
The app use the template of *Snopes* datasets, you can find *Snopes* datasets at [here](http://www.snopes.com/food/ingredient/turkey.asp).
### You can make dataset
If you would like to test the app with more datasets, you can generate dataset by using the following command with the argument `--num_of_claims`: 
```
python ./utils/make_data.py --num_of_claims=100
```

