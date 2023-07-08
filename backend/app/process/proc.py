import os
import math
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


    def get_some_menu_id_from_categ(self, li_categ:list) -> list:
        """
        指定したカテゴリのメニュー番号の一覧を返却します
        """
        li_menu_id = self.db.get_some_menu_id_from_categ(li_categ)
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


    def _register_quiz_logs(self, session_id, mode, uid=""):
        pass


    def gen_questions(self, quiz_id:str, mode:int, li_q_data:list, num_of_q:int) -> list:
        if mode == 0:
            li_menu_id = self.get_some_menu_id_from_categ(li_q_data)
        elif mode == 1:
            li_menu_id = self.get_some_menu_id_from_page(li_q_data)
        else:
            return {}

        if not li_menu_id:
            return {}

        len_li_mid = len(li_menu_id)
        if num_of_q >= len_li_mid:
            return {}
        if num_of_q < 1:
            num_of_q = len_li_mid

        quiz_data = []
        li_ans_mid = []
        questions = random.sample(li_menu_id, num_of_q)
        for q_num in range(num_of_q):
            q = questions[q_num]
            li_ans_mid.append(q)
            tmp_li_ans_mid = li_menu_id.copy()
            tmp_li_ans_mid.remove(q)
            li_ans_mid = random.sample(tmp_li_ans_mid, 3)
            li_ans_mid.insert(random.randrange(4), q)
            answers = [ self.get_item_info(li_ans_mid[ans_num])['menu_name'] for ans_num in range(len(li_ans_mid)) ]
            question = {
                    'quiz_id':quiz_id,
                    'question':q,
                    'q_num':q_num,
                    'points':self.get_item_info(questions[q_num])['price'],
                    }
            question_id = self.db.create_question(question)
            question.pop('quiz_id')
            question['question_id'] = question_id
            question['answers'] = answers
            quiz_data.append(question)
            tmp_li_ans_mid.clear()
            li_ans_mid.clear()

        return quiz_data


    def gen_quiz(self, mode:int, uid:str="guest", categs:list=[], pages:list=[], num_of_q:int=0) -> dict:
        """
        モードに応じてクイズを生成します．
        カテゴリーやページは複数選択可能です．
        """
        if (mode == 0 or mode == 1) and (categs or pages):
            quiz_id = self.db.create_quiz(uid, mode) 
        else:
            return {}

        if mode == 0 and categs:
            questions = self.gen_questions(quiz_id, mode, categs, num_of_q)
        elif mode == 1 and pages:
            questions = self.gen_questions(quiz_id, mode, pages, num_of_q)
        else:
            return {}
        
        if num_of_q > 1:
            num_of_q = len(questions)

        #max_points = sum([ question_data['points'] for question_data in questions ])

        quiz_data = {
                'quiz_id':quiz_id,
                'mode':0,
                'num_of_q':num_of_q,
                'questions':questions
                }

        return quiz_data


    def check_ans(self, quiz_id:str, ans_data:list) -> dict:
        """
        クイズの結果を集計します
        """
        q_info = self.db.get_question_info_from_quiz_id(quiz_id)
        li_rst = []
        max_points = 0
        crr_points = 0
        incrr_points = 0
        ttl_points = 0
        corrects = 0
        incorrects = 0
        for q_data in q_info:
            q_id = q_data['question_id']
            q_mid = q_data['question']
            q_points = q_data['points']
            q_num = q_data['q_num']
            max_points += q_points
            ans_menu_name = ans_data[q_num]
            ans_mid = self.db.get_menu_id_from_menu_name([ans_menu_name])[0]
            if q_mid == ans_mid:
                correct = True
                points = q_points
                crr_points += points
                correct_menu_name = ans_menu_name
                tf_symb = '◯'
                corrects += 1
            else:
                correct = False
                points = -q_points
                incrr_points += points
                correct_menu_name = self.get_item_info(q_mid)['menu_name']
                tf_symb = '×'
                incorrects += 1

            ttl_points += points
            rst_ans = {
                    'quiz_id':quiz_id,
                    'question_id':q_id,
                    'ans_menu_id':ans_mid,
                    'answer':ans_mid,
                    'ans_num':q_num,
                    'correct':correct,
                    'earned_points':points,
                    'tf_symb':tf_symb,
                    'correct_menu_name':correct_menu_name,
                    'points':points
                    }
            rst_ans['answer_id'] = self.db.create_answer(rst_ans)
            rst_ans['ans_menu_name'] = ans_menu_name
            li_rst.append(rst_ans)

        rst = {
                'quiz_id':quiz_id,
                'num_of_q':len(li_rst),
                'max_points':max_points,
                'corrects_num':corrects,
                'incorrects_num':incorrects,
                'accuracy':math.ceil(corrects/len(li_rst)*100),
                'crr_points':crr_points,
                'incrr_points':incrr_points,
                'ttl_points':ttl_points,
                'ans_rst':li_rst
                }
        rst['result_id'] = self.db.create_resultqlogs(rst)

        return rst


    def register_result(self, quiz_id:str, ans_data:list) -> dict:
        """
        回答を確認し，ポイントを集計します．
        回答したした結果を辞書で返却します．
        """
        ans_rst = self.check_ans(quiz_id, ans_data)

        return rst
