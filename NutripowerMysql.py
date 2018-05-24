#!/usr/bin/python
# -*- coding: latin-1 -*-
from peewee import mysql ,CharField ,Model, MySQLDatabase, AutoField, IntegerField, DoubleField, ForeignKeyField, DateField
import peewee as pw

# Connect to a MySQL database on network.
db = MySQLDatabase('nutripower2', user='root', password='2016hmds',
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

class Pais(BaseModel):
    id_pais = AutoField(primary_key=True)
    nome_pais = CharField(200)
    
class Estado(BaseModel):
    id_estado = AutoField(primary_key=True)
    id_pais = ForeignKeyField(Pais)
    nome_estado = CharField(200),
   
class Cidade(BaseModel):
    id_cidade = AutoField(primary_key=True)
    id_estado = ForeignKeyField(Estado)
    nome_cidade = CharField(200)


class Bairro(BaseModel):
    id_bairro = AutoField(primary_key=True)
    id_cidade = ForeignKeyField(Cidade)
    nome_bairro = CharField(200),

class Endereco(BaseModel):
    id_endereco = AutoField(primary_key=True)
    id_pais = ForeignKeyField(Pais)
    id_estado = ForeignKeyField(Estado)
    id_cidade = ForeignKeyField(Cidade)
    id_bairro = ForeignKeyField(Bairro)
    cep = IntegerField()
    nome_rua = CharField(200)
    numero_casa = IntegerField()
    complemento = CharField(200)



class Alimento_Refeicao(BaseModel):
    id_alimentos_refeicao = IntegerField(primary_key=True)
    id_alimento = ForeignKeyField(Alimento)

class Refeicao(BaseModel):
    id_refeicao = AutoField(primary_key=True)
    id_alimentos_refeicao = ForeignKeyField(Alimento_Refeicao)
    proteinas = DoubleField()
    calorias = DoubleField()
    horario_refeicao = CharField(45),
    gorduras = DoubleField()
    carboidratos = DoubleField()
    nome_refeicao = CharField(200),


class Alimento_Modelo_Refeicao(BaseModel):
    id_alimentos_modelo_refeicao = IntegerField(primary_key=True)
    id_alimento = ForeignKeyField(Alimento)

class Modelo_Refeicao(BaseModel):
    id_modelo_refeicao = AutoField(primary_key=True)
    id_alimentos_modelo_refeicao = ForeignKeyField(Alimento_Modelo_Refeicao)
    proteinas = DoubleField()
    calorias = DoubleField()
    horario_refeicao = CharField(45)
    gorduras = DoubleField()
    carboidratos = DoubleField()
    nome_refeicao = CharField(200)
    objetivo_refeicao = CharField(200)


class Refeicoes_Dieta(BaseModel):
    id_refeicoes_deita = IntegerField(primary_key=True)
    id_refeicao = ForeignKeyField(Refeicao)


class Dieta(BaseModel):
    id_dieta = AutoField(primary_key=True)
    id_refeicoes_deita = ForeignKeyField(Refeicoes_Dieta)
    nome_dieta = CharField(200)
    carboidratos = DoubleField()
    objetivo = CharField(200)
    proteinas = DoubleField()
    gorduras = DoubleField()
    calorias = DoubleField()


class Nutricionista(BaseModel):
    id_nutricionista  = AutoField(primary_key=True)
    foto = CharField(200)
    nome = CharField(200)
    senha = CharField(400)

class Paciente(BaseModel):
    id_paciente = AutoField(primary_key=True)
    endereco = CharField(200)
    peso = DoubleField()
    sexo = CharField()
    cpf = CharField(45)
    altura = DoubleField()
    telefone = CharField(45)
    nome = CharField(200)
    idade = IntegerField()
    email = CharField(200)
    atividade_fisica = CharField(200)
    foto = CharField(200)


class Avaliacao_Fisica (BaseModel):
    id_avaliacao = AutoField(primary_key=True)
    id_paciente = ForeignKeyField(Paciente)
    porcentagem_gordura = DoubleField()
    metabolismo_basal = DoubleField()
    porcentagem_massa_muscular = DoubleField()
    altura = DoubleField()
    imc = DoubleField()
    porcentagem_massa_magra = DoubleField()
    pressao = DoubleField()
    objetivo = CharField(450),
    data = DateField('dd/mm/aaaa')
    peso = DoubleField()
    observacoes = CharField(450)


class Consulta(BaseModel): 
    id_consulta = AutoField(primary_key=True)
    id_paciente = ForeignKeyField(Paciente)
    id_avaliacao = ForeignKeyField(Avaliacao_Fisica)
    id_dieta = ForeignKeyField(Dieta)
    id_nutricionista = ForeignKeyField(Nutricionista)
    objetivo = CharField(450)
    proxima_consulta = CharField(200)
    data = DateField('dd/mm/aaaa')
