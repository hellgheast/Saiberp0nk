# Simple module for dumping text with some delays

from typing import Tuple,List
from evennia import utils

def sendText(obj,text):
    obj.msg(text)

def sendDelayedText(obj,text:str,delayTime:int):
    utils.delay(delayTime,sendText,obj=obj,text=text)

def sendArrayText(obj,arrayText:List[Tuple[str,int]]):
    for elem in arrayText:
        text,delayTime = elem
        sendDelayedText(obj,text,delayTime)

