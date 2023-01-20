import sqlalchemy as db

# specify database configurations
# docker run --name=db_demo -d -p 3306:3306 mysql/mysql-server:latest
#db_user: root
#db_pass: admin
#&0y7M0Gp0#Ua/7p28nevL#;B1:YLbP,*
# https://phoenixnap.com/kb/mysql-docker-container
# https://medium.com/swlh/how-to-connect-to-mysql-docker-from-python-application-on-macos-mojave-32c7834e5afa

config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'db_master',
    'password': 'admin',
    'database': 'test_db'
}
db_user = config.get('user')
db_pwd = config.get('password')
db_host = config.get('host')
db_port = config.get('port')
db_name = config.get('database')
# specify connection string
connection_str = f'mysql+pymysql://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}'
# connect to database
engine = db.create_engine(connection_str)
connection = engine.connect()
# pull metadata of a table
metadata = db.MetaData(bind=engine)
metadata.reflect(only=['test_table'])

test_table = metadata.tables['test_table']
test_table