#!/usr/bin/python
#encoding: utf-8
from AlimentoMysql import Alimento , db
import codecs

lista = Alimento.select()
for a in lista:
    print(a.nome)


db.close()