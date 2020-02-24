

class Config(object):

    MYSQL_DB_HOST = "db"
    MYSQL_DB_USER = "user"
    MYSQL_DB_PASSWORD = "password"
    MYSQL_DB_PORT = "3306"
    MYSQL_DB_NAME = "app-db"

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(
        MYSQL_DB_USER,
        MYSQL_DB_PASSWORD,
        MYSQL_DB_HOST,
        MYSQL_DB_PORT,
        MYSQL_DB_NAME
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
