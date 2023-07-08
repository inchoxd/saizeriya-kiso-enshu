import os
import json
from dotenv import load_dotenv
from uuid import uuid4 as uuid

from sqlalchemy import create_engine, func
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import *

from datetime import datetime as dt


Base = declarative_base()


class Session(Base):
    __tablename__ = 'session'
    __table_args__=({"mysql_charset": "utf8mb4"})

    session_id = Column(String(36), primary_key=True)           # 一意のユーザ管理ID
    uid = Column(String(36))                                    # 一意のユーザ管理ID
    mode = Column(Integer)                                      # クイズのモード(0: menu_idを答える, 1: 料理名を答える)
    created_at = Column(DateTime)                               # 作成日時
    updated_at = Column(DateTime)                               # 更新日時
    exp = Column(DateTime)                                      # 有効期限


class QuizLogs(Base):
    __tablename__ = 'quizlogs'
    __table_args__=({"mysql_charset": "utf8mb4"})

    quiz_id = Column(String(36), primary_key=True)              # クイズ識別ID
    uid = Column(String(36))                                    # 一意のユーザ管理ID
    mode = Column(Integer)                                      # クイズのモード(0: menu_idを答える, 1: 料理名を答える)
    created_at = Column(DateTime)                               # 作成日時
    updated_at = Column(DateTime)                               # 更新日時

    r_quizlogs_ans_info = relationship('ResultQuizLogs', backref='quizlogs')
    r_questionlogs = relationship('QuestionLogs', backref='quizlogs')
    r_answerlogs = relationship('AnswerLogs', backref='quizlogs')


class ResultQuizLogs(Base):
    __tablename__ = 'resultqlogs'
    __table_args__=({"mysql_charset": "utf8mb4"})

    result_id = Column(String(36),primary_key=True)             # 結果識別ID
    quiz_id = Column(String(36), ForeignKey('quizlogs.quiz_id'))
    num_of_q = Column(Integer)                                  # 出題数
    max_points = Column(Integer)                                # 獲得できる最大のポイント
    corrects_num = Column(Integer)                              # 正解した数
    incorrects_num = Column(Integer)                            # 不正解の数
    accuracy = Column(Integer)                                  # 正答率
    crr_points = Column(Integer)                                # 正解したポイントの合計
    incrr_points = Column(Integer)                             # 不正解したポイントの合計
    ttl_points = Column(Integer)                                # 獲得したポイントの合計点数
    created_at = Column(DateTime)                               # 作成日時
    updated_at = Column(DateTime)                               # 更新日時


class QuestionLogs(Base):
    __tablename__ = 'questionlogs'
    __table_args__=({"mysql_charset": "utf8mb4"})

    question_id = Column(String(36), primary_key=True)          # 出題ID
    quiz_id = Column(String(36), ForeignKey('quizlogs.quiz_id'))
    question = Column(String(4))                                # 出題内容(メニュー番号)
    q_num = Column(Integer)                                     # 出題番号
    points = Column(Integer)                                    # 正解すると獲得できるポイント．不正解なら-1倍.
    created_at = Column(DateTime)                               # 作成日時
    updated_at = Column(DateTime)                               # 更新日時

    r_answerlogs = relationship('AnswerLogs', backref='questionlogs')


class AnswerLogs(Base):
    __tablename__ = 'answerlogs'
    __table_args__=({"mysql_charset": "utf8mb4"})

    answer_id = Column(String(36), primary_key=True)            # 回答ID
    quiz_id = Column(String(36), ForeignKey('quizlogs.quiz_id'))
    question_id = Column(String(36), ForeignKey('questionlogs.question_id'))
    answer = Column(String(4))                                  # 回答内容(メニュー番号)
    ans_num = Column(Integer)                                   # 回答番号
    correct = Column(Boolean)                                   # 正解したかどうか
    earned_points = Column(Integer)                             # 獲得したポイント
    created_at = Column(DateTime)                               # 作成日時
    updated_at = Column(DateTime)                               # 更新日時


class Categories(Base):
    __tablename__ = 'categories'
    __table_args__=({"mysql_charset": "utf8mb4"})

    name = Column(String(32), primary_key=True)                 # カテゴリ名
    note = Column(String(256))                                  # 料理の説明
    created_at = Column(DateTime)                               # 作成日時
    updated_at = Column(DateTime)                               # 更新日時

    r_pages = relationship('CategsPage', backref='categories')


class CategsPage(Base):
    __tablename__ = 'categories_page'
    __table_args__=({"mysql_charset": "utf8mb4"})

    page_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32), ForeignKey('categories.name'))    # カテゴリ名
    page = Column(Integer)                                      # 掲載されているページ
    created_at = Column(DateTime)                               # 作成日時
    updated_at = Column(DateTime)                               # 更新日時


class Items(Base):
    __tablename__ = 'items'
    __table_args__=({"mysql_charset": "utf8mb4"})

    menu_id = Column(String(4), primary_key=True)               # メニュー番号
    menu_name = Column(String(128))                             # 料理名
    note = Column(String(256))                                  # 料理の説明
    price = Column(Integer)                                     # 価格(税込み)
    hot = Column(Integer)                                       # 辛さ
    new = Column(Boolean)                                       # 新商品
    seasonal = Column(Boolean)                                  # 季節商品
    popular = Column(Boolean)                                   # 人気商品
    category = Column(String(32))                               # カテゴリ
    is_size = Column(Boolean)                                   # 容量に関するデータを含むか
    is_cal = Column(Boolean)                                    # カロリーの情報が含まれているか
    is_solt = Column(Boolean)                                   # 塩分情報が含まれているか
    is_relation = Column(Boolean)                               # 関連メニューがあるか
    created_at = Column(DateTime)                               # 作成日時
    updated_at = Column(DateTime)                               # 更新日時

    r_cal_solt = relationship('ItemsCalSolt', backref='items')
    r_cal_solt = relationship('ItemsSize', backref='items')
    r_cal_solt = relationship('ItemsRelation', backref='items')
    r_cal_solt = relationship('ItemsPage', backref='items')


class ItemsCalSolt(Base):
    __tablename__ = 'items_cal_solt'
    __table_args__=({"mysql_charset": "utf8mb4"})

    cal_solt_id = Column(Integer, primary_key=True, autoincrement=True)
    menu_id = Column(String(4), ForeignKey('items.menu_id'))    # メニュー番号
    cal = Column(Integer)                                       # カロリー[cal]
    solt_content = Column(Float(8))                             # 塩分[mg]
    created_at = Column(DateTime)                               # 作成日時
    updated_at = Column(DateTime)                               # 更新日時


class ItemsSize(Base):
    __tablename__ = 'items_size'
    __table_args__=({"mysql_charset": "utf8mb4"})

    size_id = Column(Integer, primary_key=True, autoincrement=True)
    menu_id = Column(String(4), ForeignKey('items.menu_id'))    # メニュー番号
    size = Column(Integer)                                      # 容量[ml]
    created_at = Column(DateTime)                               # 作成日時
    updated_at = Column(DateTime)                               # 更新日時


class ItemsRelation(Base):
    __tablename__ = 'items_relation'
    __table_args__=({"mysql_charset": "utf8mb4"})

    relation_id = Column(Integer, primary_key=True, autoincrement=True)
    menu_id = Column(String(4), ForeignKey('items.menu_id'))    # メニュー番号
    relation_menu_id = Column(String(4))                        # メニュー番号
    created_at = Column(DateTime)                               # 作成日時
    updated_at = Column(DateTime)                               # 更新日時


class ItemsPage(Base):
    __tablename__ = 'items_page'
    __table_args__=({"mysql_charset": "utf8mb4"})

    page_id = Column(Integer, primary_key=True, autoincrement=True)
    menu_id = Column(String(4), ForeignKey('items.menu_id'))    # メニュー番号
    page = Column(Integer)                                      # 掲載ページ
    created_at = Column(DateTime)                               # 作成日時
    updated_at = Column(DateTime)                               # 更新日時


class DB:
    def __init__(self):
        load_dotenv(override=True)
        user = os.environ['DB_USER']
        pswd = os.environ['PASSWORD']
        host = os.environ['HOST']
        db_name = os.environ['DATABASE']
        db_path = f'mysql+mysqlconnector://{user}:{pswd}@{host}/{db_name}'
        self.engine = create_engine(db_path)
        Base.metadata.create_all(bind=self.engine)
        self.Session = sessionmaker(bind=self.engine)


    ##################################################
    # セッション関連
    ##################################################
    def session_info(self, session_id:str) -> bool:
        session = self.Session()
        try:
            target = session.query(Session).filter_by(session_id=session_id).one()
            session.close()
        except NoResultFound:
            return False
        else:
            info = {
                    'session_id':target.session_id,
                    'uid':target.uid,
                    'mode':target.mode,
                    'points':target.points,
                    'created_at':target.created_at,
                    'updated_at':target.updated_at,
                    'exp':target.exp
                    }

            return info


    ##################################################
    # メニュー登録・更新関連
    ##################################################
    def register_category(self, categories:dict) -> bool:
        name = categories['name']
        note = categories['note']
        created_at = dt.now()
        category = Categories(name=name, note=note, created_at=created_at, updated_at=created_at)
        session = self.Session()
        session.add(category)
        session.commit()
        session.close()
        
        return True


    def register_categ_page(self, page_data:dict) -> bool:
        name = page_data['name']
        page = page_data['page']
        created_at = dt.now()
        categ = CategsPage(name=name, page=page, created_at=created_at, updated_at=created_at)
        session = self.Session()
        session.add(categ)
        session.commit()
        session.close()

        return True


    def register_item_info(self, menu_data:dict) -> bool:
        """
        メニューの基本情報の登録を行う関数．
        """
        menu_id = menu_data['menu_id']
        menu_name = menu_data['menu_name']
        note = menu_data['note']
        price = menu_data['price']
        hot = menu_data['hot']
        new = menu_data['new']
        seasonal = menu_data['seasonal']
        popular = menu_data['popular']
        category = menu_data['category']
        is_cal = menu_data['is_cal']
        is_solt = menu_data['is_solt']
        is_size = menu_data['is_size']
        is_relation = menu_data['is_relation']
        created_at = dt.now()
        menu = Items(menu_id=menu_id, menu_name=menu_name, note=note, price=price, is_cal=is_cal, is_solt=is_solt, hot=hot, is_size=is_size, new=new, seasonal=seasonal, popular=popular, category=category, is_relation=is_relation, created_at=created_at, updated_at=created_at)
        session = self.Session()
        session.add(menu)
        session.commit()
        session.close()
        
        return True


    def register_item_cal_solt(self, cal_solt_data:dict) -> bool:
        menu_id = cal_solt_data['menu_id']
        cal = cal_solt_data['cal']
        solt_content = cal_solt_data['solt_content']
        created_at = dt.now()
        menu = ItemsCalSolt(menu_id=menu_id, cal=cal, solt_content=solt_content, created_at=created_at, updated_at=created_at)
        session = self.Session()
        session.add(menu)
        session.commit()
        session.close()

        return True


    def register_item_size(self, size_data:dict) -> bool:
        menu_id = size_data['menu_id']
        size = size_data['size']
        created_at = dt.now()
        menu = ItemsSize(menu_id=menu_id, size=size, created_at=created_at, updated_at=created_at)
        session = self.Session()
        session.add(menu)
        session.commit()
        session.close()

        return True


    def register_item_relation(self, relation_data:dict) -> bool:
        menu_id = relation_data['menu_id']
        relation_menu_id = relation_data['relation_menu_id']
        created_at = dt.now()
        menu = ItemsRelation(menu_id=menu_id, relation_menu_id=relation_menu_id, created_at=created_at, updated_at=created_at)
        session = self.Session()
        session.add(menu)
        session.commit()
        session.close()

        return True


    def register_item_page(self, page_data:dict) -> bool:
        menu_id = page_data['menu_id']
        page = page_data['page']
        created_at = dt.now()
        menu = ItemsPage(menu_id=menu_id, page=page, created_at=created_at, updated_at=created_at)
        session = self.Session()
        session.add(menu)
        session.commit()
        session.close()

        return True


    ##################################################
    # 出題・回答登録，取得
    ##################################################
    def create_quiz(self, uid:str, mode:int) -> str:
        quiz_id = str(uuid())
        created_at = dt.now()
        session = self.Session()
        quiz = QuizLogs(quiz_id=quiz_id, uid=uid, mode=mode, created_at=created_at, updated_at=created_at)
        session.add(quiz)
        session.commit()
        session.close()

        return quiz_id


    def create_question(self, question_data:dict) -> str:
        question_id = str(uuid())
        quiz_id = question_data['quiz_id']
        q = question_data['question']
        q_num = question_data['q_num']
        points = question_data['points']
        created_at = dt.now()
        session = self.Session()
        question = QuestionLogs(question_id=question_id, quiz_id=quiz_id, question=q, q_num=q_num, points=points, created_at=created_at, updated_at=created_at)
        session.add(question)
        session.commit()
        session.close()

        return question_id


    def create_answer(self, answer_data:dict) -> str:
        answer_id = str(uuid())
        quiz_id = answer_data['quiz_id']
        question_id = answer_data['question_id']
        answer = answer_data['answer']
        ans_num = answer_data['ans_num']
        correct = answer_data['correct']
        earned_points = answer_data['earned_points']
        created_at = dt.now()
        session = self.Session()
        answer = AnswerLogs(answer_id=answer_id, quiz_id=quiz_id, question_id=question_id, answer=answer, ans_num=ans_num, correct=correct, earned_points=earned_points, created_at=created_at, updated_at=created_at)
        session.add(answer)
        session.commit()
        session.close()

        return answer_id


    def create_resultqlogs(self, result_data:dict) -> str:
        result_id = str(uuid())
        quiz_id = result_data['quiz_id']
        num_of_q = result_data['num_of_q']
        max_points = result_data['max_points']
        corrects_num = result_data['corrects_num']
        incorrects_num = result_data['incorrects_num']
        accuracy = result_data['accuracy']
        crr_points = result_data['crr_points']
        incrr_points = result_data['incrr_points']
        ttl_points = result_data['ttl_points']
        created_at = dt.now()
        session = self.Session()
        answer = ResultQuizLogs(result_id=result_id, quiz_id=quiz_id, num_of_q=num_of_q, max_points=max_points, corrects_num=corrects_num, incorrects_num=incorrects_num, accuracy=accuracy, crr_points=crr_points, incrr_points=incrr_points, ttl_points=ttl_points, created_at=created_at, updated_at=created_at)
        session.add(answer)
        session.commit()
        session.close()

        return result_id


    def get_quiz_info(self, quiz_id:str) -> dict:
        session = self.Session()
        try:
            quiz_data = session.query(ItemsCalSolt).filter_by(quiz_id=quiz_id).one()
        except NoResultFound:
            return {}
        finally:
            quiz_info = {
                    'quiz_id':quiz_data.quiz_id,
                    'uid':quiz_data.uid,
                    'mode': quiz_data.mode,
                    'num_of_q':quiz_data.num_of_q,
                    'max_points':quiz_data.max_points
                    }

        return quiz_info


    def get_question_info_from_quiz_id(self, quiz_id:str) -> list:
        session = self.Session()
        try:
            question_data = session.query(QuestionLogs).filter_by(quiz_id=quiz_id).order_by(QuestionLogs.q_num).all()
        except NoResultFound:
            return {}
        finally:
            question_info = [ {'question_id':data.question_id, 'question':data.question, 'q_num':data.q_num, 'points':data.points} for data in question_data ]
            
            return question_info


    ##################################################
    # 各種データ取得
    ##################################################
    def _get_item_sub_info(self, sub_info_flg:dict) -> dict:
        """
        カロリーや塩分表示, サイズなど，一部のメニュー情報に紐付いたサブ情報をdbから取得し返却する内部関数
        sub_info_flg = {
            'is_cal':bool,
            'is_solt:bool.
            'is_size':bool,
            'is_relation':bool
            }
        """
        session = self.Session()
        menu_id = sub_info_flg['menu_id']
        try:
            if sub_info_flg['is_cal'] and sub_info_flg['is_solt']:
                cal_solt_info = session.query(ItemsCalSolt).filter_by(menu_id=menu_id).one()
                cal = cal_solt_info.cal
                solt_content = cal_solt_info.solt_content
            else:
                cal = None
                solt_content = None
            if sub_info_flg['is_size']:
                size_info = session.query(ItemsSize).filter_by(menu_id=menu_id).one()
                size = size_info.size
            else:
                size = None
            if sub_info_flg['is_relation']:
                relaitons_info = session.query(ItemsRelation).filter_by(menu_id=menu_id).all()
                relations = [ relation_info.relation_menu_id for relation_info in relaitons_info ]
            else:
                relations = []

            pages_info = session.query(ItemsPage).filter_by(menu_id=menu_id)
            pages = [ page_info.page for page_info in pages_info ]

            session.close()

        except NoResultFound:
            return {}
        finally:
            sub_info = {
                    'cal':cal,
                    'solt_content':solt_content,
                    'size':size,
                    'relations':relations,
                    'pages':pages
                    } 

            return sub_info


    def get_item_info(self, menu_id:str) -> dict:
        session = self.Session()
        try:
            base_data = session.query(Items).filter_by(menu_id=menu_id).one()
            sub_data_flg = {
                    'menu_id':base_data.menu_id,
                    'is_cal':base_data.is_cal,
                    'is_solt':base_data.is_solt,
                    'is_size':base_data.is_size,
                    'is_relation':base_data.is_relation
                    }

            session.close()
        except NoResultFound:
            return {}
        finally:
            sub_data = self._get_item_sub_info(sub_data_flg)
            item_info = {
                    'menu_id':base_data.menu_id,
                    'menu_name':base_data.menu_name,
                    'note':base_data.note,
                    'price':base_data.price,
                    'cal':sub_data['cal'],
                    'solt_content':sub_data['solt_content'],
                    'hot':base_data.hot,
                    'size':sub_data['size'],
                    'new':base_data.new,
                    'seasonal':base_data.seasonal,
                    'popular':base_data.popular,
                    'relations':sub_data['relations'],
                    'category':base_data.category,
                    'pages':sub_data['pages']
                    }
        
            return item_info


    def get_some_item_info(self, li_menu_id:list) -> dict:
        session = self.Session()
        try:
            bases_data = session.query(Items).filter(Items.menu_id.in_(li_menu_id)).all()
            
            session.close()
        except NoResultFound:
            return {}
        finally:
            items_info = []
            for base_data in bases_data:
                sub_data_flg = {
                        'menu_id':base_data.menu_id,
                        'is_cal':base_data.is_cal,
                        'is_solt':base_data.is_solt,
                        'is_size':base_data.is_size,
                        'is_relation':base_data.is_relation
                        }
    
                sub_data = self._get_item_sub_info(sub_data_flg)
                item_info = {
                        'menu_id':base_data.menu_id,
                        'menu_name':base_data.menu_name,
                        'note':base_data.note,
                        'price':base_data.price,
                        'cal':sub_data['cal'],
                        'solt_content':sub_data['solt_content'],
                        'hot':base_data.hot,
                        'size':sub_data['size'],
                        'new':base_data.new,
                        'seasonal':base_data.seasonal,
                        'popular':base_data.popular,
                        'relations':sub_data['relations'],
                        'category':base_data.category,
                        'pages':sub_data['pages']
                        }
                items_info.append(item_info)
        
            return items_info


    def get_menu_id_from_page(self, page:int) -> list:
        """
        指定したページに掲載されているメニュー番号の一覧を返却します
    """
        session = self.Session()
        try:
            pages_data = session.query(ItemsPage.menu_id).filter_by(page=page).all()
            
            session.close()
        except NoResultFound:
            return {}
        finally:
            li_menu_id = [ page_data.menu_id for page_data in pages_data ]

        return li_menu_id


    def get_some_menu_id_from_page(self, li_page:list) -> list:
        """
        指定したページに掲載されているメニュー番号の一覧を返却します
        """
        session = self.Session()
        try:
            pages_data = session.query(ItemsPage.menu_id).filter(ItemsPage.page.in_(li_page)).all()
            
            session.close()
        except NoResultFound:
            return {}
        finally:
            li_menu_id = [ page_data.menu_id for page_data in pages_data ]

        return li_menu_id


    def get_menu_id_from_menu_name(self, li_name:list) -> list:
        """
        料理名からメニュー番号の一覧を返却します
        """
        session = self.Session()
        try:
            menus_data = session.query(Items).filter(Items.menu_name.in_(li_name)).all()
            
            session.close()
        except NoResultFound:
            return {}
        finally:
            li_menu_id = [ menu_data.menu_id for menu_data in menus_data ]

        return li_menu_id


    def get_menu_id_from_categ(self, categ:str) -> list:
        """
        指定したカテゴリのメニュー番号の一覧を返却します
        """
        session = self.Session()
        try:
            categs_data = session.query(Items.menu_id).filter_by(category=categ).all()
            
            session.close()
        except NoResultFound:
            return {}
        finally:
            li_menu_id = [ categ_data.menu_id for categ_data in categs_data ]

            return li_menu_id


    def get_some_menu_id_from_categ(self, li_categ:list) -> list:
        """
        指定したカテゴリのメニュー番号の一覧を返却します
        """
        session = self.Session()
        try:
            categs_data = session.query(Items.menu_id).filter(Items.category.in_(li_categ)).all()
            
            session.close()
        except NoResultFound:
            return {}
        finally:
            li_menu_id = [ categ_data.menu_id for categ_data in categs_data ]

            return li_menu_id


    def get_all_categs(self) -> list:
        """
        すべてのカテゴリ名を一覧で返却します
        """
        session = self.Session()
        try:
            categs_data = session.query(Categories.name).all()
            
            session.close()
        except NoResultFound:
            return {}
        finally:
            li_categs = [ categ_name.name for categ_name in categs_data ]

            return li_categs


    def get_categ_info(self, categ:str) -> dict:
        """
        カテゴリのデータを返却します
        """
        session = self.Session()
        try:
            categ_data = session.query(Categories).filter_by(name=categ).one()
            
            session.close()
        except NoResultFound:
            return {}
        finally:
            categ_info = {
                    'name':categ_data.name,
                    'note':categ_data.note
                    }
        
        return categ_info


    def get_some_categ_info(self, li_categ:list) -> list:
        """
        カテゴリのデータを返却します
        """
        session = self.Session()
        try:
            categs_data = session.query(Categories).filter(Categories.name.in_(li_categ)).all()
            
            session.close()
        except NoResultFound:
            return {}
        finally:
            categs_info = []
            for categ_data in categs_data:
                categ_info = {
                        'name':categ_data.name,
                        'note':categ_data.note
                        }
                categs_info.append(categ_info)
        
        return categs_info
