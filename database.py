from sqlalchemy import create_engine, Column, Integer, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()
engine = create_engine('postgresql://localhost/semanphone')
DB_Session = sessionmaker(bind=engine)


class Query(Base):
    __tablename__ = 'query'
    word = Column(Text, primary_key=True)
    times = Column(Integer)
    recommendations = relationship('Recommendation', back_populates='query')


class Recommendation(Base):
    __tablename__ = 'recommendation'
    id = Column(Integer, primary_key=True)
    word = Column(Text)
    times = Column(Integer)
    query_word = Column(Text, ForeignKey('query.word'))
    query = relationship('Query', back_populates='recommendations')


Base.metadata.create_all(engine)
print('数据库初始化成功。')


def db_query_word(word):
    db_session = DB_Session()
    q = db_session.query(Query).filter_by(word=word).first()
    if q:
        q.times += 1
    else:
        db_session.add(Query(word=word, times=1))
    db_session.commit()
    db_session.close()


def db_init_comparison(word, comparison):
    db_session = DB_Session()
    for c, _ in comparison:
        a = db_session.query(Recommendation).filter_by(word=c, query_word=word).first()
        if not a:
            db_session.add(Recommendation(word=c, times=0, query_word=word))
    db_session.commit()
    db_session.close()


def db_approve_word(q_word, r_word):
    db_session = DB_Session()
    q = db_session.query(Query).filter_by(word=q_word).first()
    if q:
        result = db_session.query(Query, Recommendation) \
            .filter(Query.word == q_word, Recommendation.word == r_word) \
            .first()
        if result:
            r = result[1]
            r.times += 1
    db_session.commit()
    db_session.close()


def db_disapprove_word(q_word, r_word):
    db_session = DB_Session()
    q = db_session.query(Query).filter_by(word=q_word).first()
    if q:
        result = db_session.query(Query, Recommendation) \
            .filter(Query.word == q_word, Recommendation.word == r_word) \
            .first()
        if result:
            r = result[1]
            r.times -= 1
    db_session.commit()
    db_session.close()
