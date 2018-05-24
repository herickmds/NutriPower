#!/usr/bin/python
#encoding: utf-8
from NutripowerMysql import Alimento , db
import codecs


lista = Alimento.select()

for a in lista:
    print(u" %s"% a.nome)


