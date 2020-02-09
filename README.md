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
The first, you must be install PostgreSQL 12.0 and create a database had some configuring settings:
```
dbuser='postgres'
dbpass=27101997
dbhost='localhost'
dbname='fact_checking'
```
# Running
To run app:<br>
```
python run.py
```
Your app will be running on url: <!-- markdownlint-capture --> [http://localhost:5050/](http://localhost:5050/)
### Getting Started
If you firstly run app, your database is empty, so you must import data having a lot of claims from folder *datasets*
### You can make dataset
If you would like to test app on more datasets, you can generate dataset by the argument `--num_of_claims` with a certain number: 
```
python ./utils/make_data.py --num_of_claims=100
```

