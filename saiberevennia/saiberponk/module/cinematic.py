# Simple module for dumping text with some delays

from typing import Tuple,List
from evennia import utils

def sendText(obj,text):
    obj.msg(text)

def sendDelayedText(obj,text:str,delayTime:int):
    utils.delay(delayTime,sendText,obj=obj,text=text)

def sendArrayText(obj,arrayText:List[Tuple[str,int]]):
    """
    Send delayed text stored in array.
    each element in the array is a tuple (text,delay)
    Each delay is relative to the previous one
    """
    mainDelay:int = 0
    for elem in arrayText:
        text,delayTime = elem
        mainDelay += delayTime
        sendDelayedText(obj,text,mainDelay)

