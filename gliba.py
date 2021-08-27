import time
start_time = time.time()
import random
import numpy as np
import sqlite3
from emoch import *
import asyncio
import pymorphy2
import pymorphy2_dicts_ru
import spacy
from spacy.lang.ru import Russian
from spacy.util import minibatch, compounding


connector = sqlite3.connect('data.db')
cursor = connector.cursor()

import os                                                     #


async def get_word(text):
    cursor.execute('SELECT out FROM words WHERE inp = (?)', (text,))
    rez = cursor.fetchall()
    try:
        return(rez[0][0])
    except:
        return


async def emoch_sost():
    rez = 0.0
    for i in emochii:
        rez = rez + emochii[i][0]*emochii[i][1]

    print(rez)
    return(rez)


async def morhy(text):
    pass


async def gharmonium():
    pass

#asyncio.run(emoch_sost())






print(f"--- {round((time.time() - start_time),2)} seconds ---")