from sqlalchemy import create_engine, Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from random import randrange

Base = declarative_base()
# engine = create_engine('postgresql://localhost/testsemanphone')
engine = create_engine('postgresql:///testsemanphone')
DB_Session = sessionmaker(bind=engine)
SIZE = 10


class TestWords(Base):
    __tablename__ = 'testwords'
    word = Column(Text, primary_key=True)
    exp_time = Column(Integer)
    exp_cor_time = Column(Integer)
    con_time = Column(Integer)
    con_cor_time = Column(Integer)
    definitions = Column(Text)
    examples = Column(Text)
    asso_words = Column(Text)


Base.metadata.create_all(engine)
print('数据库初始化成功。')


def add_new_word(word, definitions, examples, asso_words):
    """
    add a new random word to 'testwords' table, and set definitions, examples, and asso_words columns to the given
    arguments, set other columns to 0

    :param word:
    :param definitions: a list of definitions
    :param examples: a list of examples
    :param asso_words: a list of associated words
    :return:
    """
    db_session = DB_Session()
    q = db_session.query(TestWords).filter_by(word=word.strip()).first()
    if not q:
        definitions = '\n'.join([s.replace('\n', ' ') for s in definitions])
        examples = '\n'.join([s.replace('\n', ' ') for s in examples])
        asso_words = '\n'.join([s.replace('\n', ' ') for s in asso_words])
        db_session.add(TestWords(word=word, definitions=definitions, examples=examples, asso_words=asso_words,
                                 exp_time=0, exp_cor_time=0, con_time=0, con_cor_time=0))
    db_session.commit()
    db_session.close()


def pick_words_4experience():
    """
    pick up SIZE random words for experience page
    :return: a list of random words
    """
    db_session = DB_Session()
    rows = db_session.query(TestWords)
    rows_amount = rows.count()
    random_words = []
    for i in range(SIZE):
        rand_idx = randrange(1, rows_amount + 1)
        rows[rand_idx].exp_time += 1
        random_words.append(rows[rand_idx].word)
    db_session.commit()
    db_session.close()
    return random_words


def pick_words_4control():
    """
    pick up SIZE random words for control page
    :return: a list of random words
    """
    db_session = DB_Session()
    rows = db_session.query(TestWords)
    rows_amount = rows.count()
    random_words = []
    for i in range(SIZE):
        rand_idx = randrange(1, rows_amount + 1)
        rows[rand_idx].con_time += 1
        random_words.append(rows[rand_idx].word)
    db_session.commit()
    db_session.close()
    return random_words


def get_asso_words(word):
    """
    get asso_words of the word
    :param word:
    :return: a list of asso_words
    """
    db_session = DB_Session()
    q = db_session.query(TestWords).filter_by(word=word).first()
    if q:
        asso_words = q.asso_words
        asso_words = asso_words.split('\n')
    else:
        asso_words = []
    db_session.commit()
    db_session.close()
    return asso_words


def get_definitions(word):
    """
    get definitions of the word
    :param word:
    :return: a list of (definition_string, part_of_speech)
    """
    db_session = DB_Session()
    q = db_session.query(TestWords).filter_by(word=word).first()
    if q:
        definitions = q.definitions.split('\n')
        definitions = [tuple(d.split('#')) for d in definitions]
    else:
        definitions = []
    db_session.commit()
    db_session.close()
    return definitions



def increase_experience_corrate(word):
    """
    increase exp_cor_time of the word
    :param word:
    :return:
    """
    db_session = DB_Session()
    q = db_session.query(TestWords).filter_by(word=word).first()
    if q:
        q.exp_cor_time += 1
    db_session.commit()
    db_session.close()


def increase_control_corrate(word):
    """
    increase con_cor_time of the word
    :param word:
    :return:
    """
    db_session = DB_Session()
    q = db_session.query(TestWords).filter_by(word=word).first()
    if q:
        q.con_cor_time += 1
    db_session.commit()
    db_session.close()
