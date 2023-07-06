import os
import json
import random
from uuid import uuid4 as uuid
from dotenv import load_dotenv
from datetime import time as tm
from datetime import datetime as dt

from .db import *


class Proc:
    def __init__(self):
        load_dotenv(override=True)
        self.db = DB()
        self.menu_fp = './menu.json'


    def _open_json(self) -> dict:
        with open(self.menu_fp, 'r') as f:
            menu_data = json.load(f)

        return menu_data


    def get_item_info(self, menu_id:str) -> dict:
        item_info = self.db.get_item_info(menu_id)
        return item_info


    def get_some_item_info(self, li_menu_id:list) -> dict:
        """
        複数のメニュー番号からメニューの情報を取得しlistで返却する
        """
        items_info = self.db.get_some_item_info(li_menu_id)
        return items_info


    def get_menu_id_from_page(self, page:int) -> list:
        """
        指定したページに掲載されているメニュー番号の一覧を返却します
        """
        li_menu_id = self.db.get_menu_id_from_page(page)
        return li_menu_id


    def get_some_menu_id_from_page(self, li_page:list) -> list:
        """
        指定したページに掲載されているメニュー番号の一覧を返却します
        """
        li_menu_id = self.db.get_some_menu_id_from_page(li_page)
        return li_menu_id


    def get_menu_id_from_categ(self, categ:str) -> list:
        """
        指定したカテゴリのメニュー番号の一覧を返却します
        """
        li_menu_id = self.db.get_menu_id_from_categ(categ)
        return li_menu_id


    def get_menu_id_from_menu_name(self, li_name:list) -> list:
        """
        料理名からメニュー番号の一覧を返却します
        """
        li_menu_id = self.db.get_menu_id_from_menu_name(li_name)
        return li_menu_id


    def get_menu_id_from_some_categ(self, li_categ:list) -> list:
        """
        指定したカテゴリのメニュー番号の一覧を返却します
        """
        li_menu_id = self.db.get_menu_id_from_some_categ(li_categ)
        return li_menu_id


    def get_all_categs(self) -> list:
        """
        すべてのカテゴリ名を一覧で返却します
        """
        li_categ = self.db.get_all_categs()
        return li_categ


    def get_categ_data(self, categ:str) -> dict:
        """
        カテゴリのデータを返却します
        """
        categ_info = self.db.get_categ_info(categ)
        return categ_info


    def _gen_qiz_from_categ(self, categs:list, num_of_q:int) -> list:
        li_menu_id = self.get_menu_id_from_some_categ(categs)
        len_li_mid = len(li_menu_id)
        if num_of_q >= len_li_mid:
            return {}
        if num_of_q < 1:
            num_of_q = len_li_mid

        quiz_data = []
        li_ans_mid = []
        questions = random.sample(li_menu_id, num_of_q)
        for i in range(num_of_q):
            li_ans_mid.append(questions[i])
            tmp_li_ans_mid = questions.copy()
            tmp_li_ans_mid.pop(i)
            li_ans_mid = random.sample(tmp_li_ans_mid, 3)
            li_ans_mid.insert(random.randrange(4), questions[i])
            answers = [ menu_data['menu_name'] for menu_data in self.get_some_item_info(li_ans_mid) ]
            question = {
                    'question':questions[i],
                    'points':self.get_item_info(questions[i])['price'],
                    'answers':answers
                    }
            quiz_data.append(question)
            tmp_li_ans_mid.clear()
            li_ans_mid.clear()

        return quiz_data


    def gen_quiz(self, mode:int, uid="", categs:list=[], pages:list=[], num_of_q:int=0) -> dict:
        """
        モードに応じてクイズを生成します．
        カテゴリーやページは複数選択可能です．
        """
        if mode == 0 and categs:
            quiz_data = self._gen_qiz_from_categ(categs, num_of_q)
        elif mode == 1 and pages:
            pass
        else:
            return {}

        if num_of_q < 1:
            num_of_q = len(quiz_data)

        max_points = sum([ question_data['points'] for question_data in quiz_data ])

        if uid == "":
            uid = uuid()


    def check_ans(self, quiz_id:str) -> dict:
        """
        回答を確認し，ポイントを集計します．
        回答したした結果を辞書で返却します．
        """
        pass
