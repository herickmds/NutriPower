#!/usr/bin/python
# -*- coding: latin-1 -*-
import xlrd
import unicodecsv as csv
from peewee import mysql ,CharField ,Model, MySQLDatabase,IntegerField
import peewee as pw

# Connect to a MySQL database on network.
db = MySQLDatabase('nutripower', user='root', password='2016hmds',
                         host='localhost', port=3306)



class BaseModel(Model):
    """A base model that will use our MySQL database"""
    class Meta:
        database = db


class Alimento(BaseModel):
        id_alimento = IntegerField(primary_key=True)
        nome = CharField()
        umidade = CharField()
        Kcal = CharField()
        Kj = CharField()
        proteina = CharField()
        lipidio = CharField()
        colesterol = CharField()
        carboidrato = CharField()
        fibra_Alimentar = CharField()
        cinzas = CharField()
        calcio = CharField()
        magnezio = CharField()
        manganes = CharField()
        fosforo = CharField()
        ferro = CharField()
        sodio = CharField()
        potacio = CharField()
        cobre = CharField()
        zinco = CharField()
        retinol = CharField()
        re = CharField()
        rae = CharField()
        tiamina = CharField()
        riboflavina = CharField()
        piridoxina = CharField()
        niacina = CharField()
        vitamina_c = CharField()


def csv_from_excel():
    wb = xlrd.open_workbook('Taco.xlsx')
    sh = wb.sheet_by_name('Plan1')
   # your_csv_file = open('Taco.csv', 'w')
   # wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL,  encoding='utf-8')

    for rownum in range(sh.nrows):
		colunas = sh.row_values(rownum)
		a = Alimento.insert(id_alimento = colunas[0],
			nome                 = colunas[1],
			umidade              = colunas[2],
			Kcal                 = colunas[3],
			Kj                   = colunas[4],
			proteina             = colunas[5],
			lipidio              = colunas[6],
			colesterol           = colunas[7],
			carboidrato          = colunas[8],
			fibra_Alimentar      = colunas[9],
			cinzas               = colunas[10],
			calcio               = colunas[11],
			magnezio             = colunas[12],
			manganes             = colunas[13],
			fosforo              = colunas[14],
			ferro                = colunas[15],
			sodio                = colunas[16],
			potacio              = colunas[17],
			cobre                = colunas[18],
			zinco                = colunas[19],
			retinol              = colunas[20],
			re                   = colunas[21],
			rae                  = colunas[22],
			tiamina              = colunas[23],
			riboflavina          = colunas[24],
			piridoxina           = colunas[25],
			niacina              = colunas[26],
			vitamina_c           = colunas[27]).execute()

# runs the csv_from_excel function:
csv_from_excel()

