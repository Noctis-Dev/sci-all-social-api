from sqlalchemy import create_engine, MetaData
from databases import Database

DATABASE_URL = "mysql://admin:admin12345@sci-database.cvowgimmgxc3.us-east-1.rds.amazonaws.com:3306/sci_social_db"

database = Database(DATABASE_URL)
metadata = MetaData()

engine = create_engine(DATABASE_URL)
