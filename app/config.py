class DbConfig(object):
    DBUSER = 'postgres'
    DBPASS = 27101997
    DBHOST = 'localhost'
    DBNAME = 'fact_checking'

class AppConfig(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
        dbuser=DbConfig.DBUSER,
        dbpass=DbConfig.DBPASS,
        dbhost=DbConfig.DBHOST,
        dbname=DbConfig.DBNAME
    )

    SQLALCHEMY_TRACK_MODIFICATIONS=False
    PRODUCTION = False
    JSON_AS_ASCII = False
    UPLOAD_FOLDER = "./static/data/"
    SECRET_KEY='super secret key'
    SQLALCHEMY_ECHO = False
