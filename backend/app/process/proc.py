import os
import json
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


    def register_categ(self, categs:list) -> None:
        categs = self._open_json()['categories']
        for categ in categs:
            name = categ['name']
            note = categ['note']
            pages = categ['pages']
            if not note:
                note = '-'
            relation = categ['relation']
            categ_info = {
                    'name':name,
                    'note':note
                    }
            self.db.register_category(categ_info)
            for menu_id in relation:
                relation_data = {
                        'name':name,
                        'menu_id':menu_id
                        }
                self.db.register_categ_relation(relation_data)
            for page in pages:
                page_data = {
                        'name':name,
                        'page':page
                        }
                self.db.register_categ_page(page_data)
    
    
    def register_items(self, items:list) -> None:
        items = self._open_json()['items']
        for item in items:
            menu_id = item['menuId']
            menu_name = item['menuName']
            note = item['note']
            price = item['price']
            cal = item['cal']
            solt_content = item['soltContent']
            hot = item['hot']
            size = item['size']
            new = item['new']
            seasonal = item['seasonal']
            popular = item['popular']
            wsize = item['wSize']
            wsize_price = item['wSizePrice']
            relation = item['relation']
            categories = item['categories']
            pages = item['pages']
            is_cal = True
            is_solt = True
            is_size = False
            is_wsize = False
            is_relation = False
            if not note:
                note = '-'
            if not cal:
                is_cal = False
            if not solt_content:
                is_solt = False
            if size:
                is_size = True
            if wsize:
                is_wsize = True
            if is_relation:
                is_relation = True
            menu_data = {
                    'menu_id':menu_id,
                    'menu_name':menu_name,
                    'note':note,
                    'price':price,
                    'hot':hot,
                    'new':new,
                    'seasonal':seasonal,
                    'popular':popular,
                    'categories':categories,
                    'is_cal':is_cal,
                    'is_solt':is_solt,
                    'is_size':is_size,
                    'is_wsize':is_wsize,
                    'is_relation':is_relation
                    }
            self.db.register_item_info(menu_data)
            if is_cal and is_size:
                cal_solt_data = {
                        'menu_id':menu_id,
                        'cal':cal,
                        'solt_content':solt_content
                        }
                self.db.register_item_cal_solt(cal_solt_data)
            if is_size:
                size_data = {
                        'menu_id':menu_id,
                        'size':size
                        }
                self.db.register_item_size(size_data)
            if is_wsize:
                wsize_data = {
                        'menu_id':menu_id,
                        'wsize_menu_id':wsize,
                        'wsize_price':wsize_price
                        }
                self.db.register_item_wsize(wsize_data)
            if is_relation:
                for r_menu_id in relation:
                    relation_data = {
                            'menu_id':menu_id,
                            'relaiton_menu_id':r_menu_id
                            }
                    self.db.register_item_relation(relation_data)
            for page in pages:
                page_data = {
                        'menu_id':menu_id,
                        'page':page
                        }
                self.db.register_item_page(page_data)


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
