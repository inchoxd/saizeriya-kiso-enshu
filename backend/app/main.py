from fastapi import FastAPI, HTTPException, Request, Header, Form, Body
from fastapi.responses import HTMLResponse
from fastapi.encoders import jsonable_encoder
from typing import Optional
from pydantic import BaseModel
from process import *
import os
import json


app = FastAPI()
proc = Proc()

##################################################
# fastapi_BaseModel
##################################################
#class Session(BaseModel):
#    session_id:str
#
#
##################################################
@app.get('/quiz')
async def gen_quiz(mode:int):
    if not is_session:
        return quiz_data


@app.post('/quiz/answer')
async def gen_answer(session_id: str):
    if not is_session:
        # 400を返す
        raise HTTPException(
                status_code=400,
                detail='invalid error'
                )
    else:
        return ans_data
