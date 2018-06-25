#!/usr/bin/python
#encoding: utf-8
from NutripowerMysql import Alimento ,Estado, Pais, db

lista = [ Alimento ,Estado, Pais ]
db.connect()
db.create_tables(lista)