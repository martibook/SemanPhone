from sqlalchemy import create_engine, Column, Integer, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = None
Session = None
Base = declarative_base()


class Query(Base):
    __tablename__ = 'query'
    word = Column(Text, primary_key=True)
    times = Column(Integer)
    recommendations = relationship('Recommendation', back_populates='query')


class Recommendation(Base):
    __tablename__ = 'recommendation'
    id = Column(Integer, primary_key=True)
    word = Column(Text)
    query_word = Column(Text, ForeignKey('query.word'))
    query = relationship('Query', back_populates='recommendations')


def init_db_connection():
    global engine, Session
    engine = create_engine('postgresql://localhost/semanphone')
    Session = sessionmaker(bind=engine)

    Base.metadata.create_all(engine)
    print('数据库初始化成功。')


if __name__ == '__main__':
    init_db_connection()
