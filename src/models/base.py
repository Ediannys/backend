from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(f'postgresql://postgres:1234@localhost/cursosDB')
Session = sessionmaker(bind=engine)
Base = declarative_base()






