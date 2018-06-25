#!/usr/bin/python
# -*- coding: latin-1 -*-
from peewee import mysql, CharField, Model, MySQLDatabase, AutoField, IntegerField, DoubleField, ForeignKeyField, DateField
import peewee as pw
from playhouse.shortcuts import model_to_dict
import json

# Connect to a MySQL database on network.
db = MySQLDatabase('nutripower', user='root', password='2016hmds',
                   host='localhost', port=3306)


class BaseModel(Model):
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

    @staticmethod
    def listar(pagina=1):
        try:
            lista = Alimento.select().order_by(Alimento.nome).paginate(pagina, 10)
            return lista
        except Exception, e:
            return e

    @staticmethod
    def autocomplete():
        result = Alimento.select(Alimento.nome)
        alimentos = [model_to_dict(ali)["nome"] for ali in result]
        return json.dumps(alimentos)

    @staticmethod
    def buscar(nome):
        try:
            alimento = Alimento.select().where(Alimento.nome == nome).get()
            return alimento.id_alimento
        except Exception as e:
            return u"" + str(e)


class Pais(BaseModel):
    id_pais = AutoField(primary_key=True)
    nome_pais = CharField(200)


class Estado(BaseModel):
    id_estado = AutoField(primary_key=True)
    id_pais = ForeignKeyField(Pais, column_name="id_pais")
    nome_estado = CharField(200),


class Cidade(BaseModel):
    id_cidade = AutoField(primary_key=True)
    id_estado = ForeignKeyField(Estado, column_name="id_estado")
    nome_cidade = CharField(200)


class Bairro(BaseModel):
    id_bairro = AutoField(primary_key=True)
    id_cidade = ForeignKeyField(Cidade, column_name="id_cidade")
    nome_bairro = CharField(200),


class Endereco(BaseModel):
    id_endereco = AutoField(primary_key=True)
    id_pais = ForeignKeyField(Pais, column_name="id_pais")
    id_estado = ForeignKeyField(Estado, column_name="id_estado")
    id_cidade = ForeignKeyField(Cidade, column_name="id_cidade")
    id_bairro = ForeignKeyField(Bairro, column_name="id_bairro")
    cep = IntegerField()
    nome_rua = CharField(200)
    numero_casa = IntegerField()
    complemento = CharField(200)


class Refeicao(BaseModel):
    id_refeicao = AutoField(primary_key=True)
    horario_refeicao = CharField(45)
    nome_refeicao = CharField(200)

    @staticmethod
    def listarRefeicao(pagina=1):
        try:
            lista = Refeicao.select().order_by(Refeicao.nome_refeicao).paginate(pagina, 10)
            return lista
        except Exception, e:
            return e

    @staticmethod
    def autocomplete():
        result = Refeicao.select(Refeicao.nome_refeicao)
        refeicoes = [model_to_dict(ref)["nome_refeicao"] for ref in result]
        return json.dumps(refeicoes)

    @staticmethod
    def buscar(nome):
        try:
            refeicao = Refeicao.select().where(Refeicao.nome_refeicao == nome).get()
            return refeicao.id_refeicao
        except Exception as e:
            return u"" + str(e)
    

    def proteina(self):
        proteina = 0.0
        id_refeicao = self.id_refeicao
        a = Alimentos_Refeicao.select().where(
            Alimentos_Refeicao.id_refeicao == id_refeicao)
        for ar in a:
            ali = Alimento.get_by_id(ar.id_alimento)
            if ali.proteina == 'NA' or ali.proteina == 'Tr' or ali.proteina == '*':
                proteina = 0.0 + proteina
            else:
                proteina = ((float(ali.proteina) * ar.porcao)/100) + proteina

        return proteina

    def carboidrato(self):
        carboidrato = 0.0
        id_refeicao = self.id_refeicao
        a = Alimentos_Refeicao.select().where(
            Alimentos_Refeicao.id_refeicao == id_refeicao)
        for ar in a:
            ali = Alimento.get_by_id(ar.id_alimento)
            if ali.carboidrato == 'NA' or ali.carboidrato == 'Tr' or ali.carboidrato == '*':
                carboidrato = 0.0 + carboidrato
            else:
                carboidrato = ((float(ali.carboidrato) * ar.porcao)/100) + carboidrato

        return carboidrato

    def caloria(self):
        Kcal = 0.0
        id_refeicao = self.id_refeicao
        a = Alimentos_Refeicao.select().where(
            Alimentos_Refeicao.id_refeicao == id_refeicao)
        for ar in a:
            ali = Alimento.get_by_id(ar.id_alimento)
            if ali.Kcal == 'NA' or ali.Kcal == 'Tr' or ali.Kcal == '*':
                Kcal = 0.0 + Kcal
            else:
                Kcal = ((float(ali.Kcal) * ar.porcao)/100) + Kcal

        return Kcal

    def gordura(self):
        lipidio = 0.0
        id_refeicao = self.id_refeicao
        a = Alimentos_Refeicao.select().where(
            Alimentos_Refeicao.id_refeicao == id_refeicao)
        for ar in a:
            ali = Alimento.get_by_id(ar.id_alimento)
            if ali.lipidio == 'NA' or ali.lipidio == 'Tr' or ali.lipidio == '*':
                lipidio = 0.0 + lipidio
            else:
                lipidio = ((float(ali.lipidio) * ar.porcao)/100) + lipidio

        return lipidio

    def colesterol(self):
        colesterol = 0.0
        id_refeicao = self.id_refeicao
        a = Alimentos_Refeicao.select().where(
            Alimentos_Refeicao.id_refeicao == id_refeicao)
        for ar in a:
            ali = Alimento.get_by_id(ar.id_alimento)
            if ali.colesterol == 'NA' or ali.colesterol == 'Tr' or ali.colesterol == '*':
                colesterol = 0.0 + colesterol
            else:
                colesterol = ((float(ali.colesterol) * ar.porcao)/100) + colesterol

        return colesterol


class Alimentos_Refeicao(BaseModel):
    id_alimentos_refeicao = AutoField(primary_key=True, column_name="id_alimentos_refeicao")
    id_alimento = ForeignKeyField(Alimento, column_name="id_alimento")
    porcao = DoubleField()
    id_refeicao = ForeignKeyField(Refeicao, column_name="id_refeicao", backref="alimentos_refeicao")

    def proteina(self):
        prot = self.id_alimento.proteina
        if prot == 'NA' or prot == 'Tr' or prot == '*':
            return 0.0
        else:
            return ((float(prot) * self.porcao)/100)

    def carboidrato(self):
        carb = self.id_alimento.carboidrato
        if carb == 'NA' or carb == 'Tr' or carb == '*':
            return 0.0
        else:
            return ((float(carb) * self.porcao)/100)

    def caloria(self):
        cal = self.id_alimento.Kcal
        if cal == 'NA' or cal == 'Tr' or cal == '*':
            return 0.0
        else:
            return ((float(cal) * self.porcao)/100)

    def gordura(self):
        gord = self.id_alimento.lipidio
        if gord == 'NA' or gord == 'Tr' or gord == '*':
            return 0.0
        else:
            return ((float(gord) * self.porcao)/100)

    def colesterol(self):
        col = self.id_alimento.colesterol
        if col == 'NA' or col == 'Tr' or col == '*':
            return 0.0
        else:
            return ((float(col) * self.porcao)/100)


class Modelo_Refeicao(BaseModel):
    id_modelo_refeicao = AutoField(primary_key=True)
    horario_refeicao = CharField(45)
    nome_refeicao = CharField(200)
    objetivo_refeicao = CharField(200)


class Alimento_Modelo_Refeicao(BaseModel):
    id_alimentos_modelo_refeicao = AutoField(primary_key=True)
    id_alimento = ForeignKeyField(Alimento, column_name="id_alimento")
    id_modelo_refeicao = ForeignKeyField(
        Modelo_Refeicao, column_name="id_modelo_refeicao")


class Dieta(BaseModel):
    id_dieta = AutoField(primary_key=True)
    nome_dieta = CharField(200)
    objetivo = CharField(200)

    @staticmethod
    def listarDieta(pagina=1):
        try:
            lista = Dieta.select().order_by(Dieta.nome_dieta).paginate(pagina, 10)
            return lista
        except Exception, e:
            return e

    @staticmethod
    def autocomplete():
        result = Dieta.select(Dieta.nome_dieta)
        dietas = [model_to_dict(diet)["nome_dieta"] for diet in result]
        return json.dumps(dietas)

    @staticmethod
    def buscar(nome):
        try:
            dieta = Dieta.select().where(Dieta.nome_dieta == nome).get()
            return dieta.id_dieta
        except Exception as e:
            return u"" + str(e)

    def proteina(self):
        prot = 0.0
        for rd in self.refeicoes_dieta:
            r = Refeicao.get_by_id(rd.id_refeicao)
            prot = Refeicao.proteina(r) + prot
            
        return prot

    def carboidrato(self):
        carb = 0.0
        for rd in self.refeicoes_dieta:
            r = Refeicao.get_by_id(rd.id_refeicao)
            carb = Refeicao.carboidrato(r) + carb
            
        return carb


    def caloria(self):
        cal = 0.0
        for rd in self.refeicoes_dieta:
            r = Refeicao.get_by_id(rd.id_refeicao)
            cal = Refeicao.caloria(r) + cal
            
        return cal

    def gordura(self):
        gord = 0.0
        for rd in self.refeicoes_dieta:
            r = Refeicao.get_by_id(rd.id_refeicao)
            gord = Refeicao.gordura(r) + gord
            
        return gord


    def colesterol(self):
        col = 0.0
        for rd in self.refeicoes_dieta:
            r = Refeicao.get_by_id(rd.id_refeicao)
            col = Refeicao.colesterol(r) + col
            
        return col


class Refeicoes_Dieta(BaseModel):
    id_refeicoes_dieta = AutoField(
        primary_key=True, column_name="id_refeicoes_dieta")
    id_refeicao = ForeignKeyField(Refeicao, column_name="id_refeicao")
    id_dieta = ForeignKeyField(
        Dieta, column_name="id_dieta", backref="refeicoes_dieta")


    def nome(self):
        r = Refeicao.get_by_id(self.id_refeicao)
        return r.nome_refeicao

    def proteina(self):
        r = Refeicao.get_by_id(self.id_refeicao)
        prot = Refeicao.proteina(r)
        return prot

    def carboidrato(self):
        r = Refeicao.get_by_id(self.id_refeicao)
        carb = Refeicao.carboidrato(r)
        return carb
        
    def caloria(self):
        r = Refeicao.get_by_id(self.id_refeicao)
        cal = Refeicao.caloria(r)
        return cal
        

    def gordura(self):
        r = Refeicao.get_by_id(self.id_refeicao)
        gord = Refeicao.gordura(r)
        return gord
        

    def colesterol(self):
        r = Refeicao.get_by_id(self.id_refeicao)
        col = Refeicao.colesterol(r)
        return col
        

class Nutricionista(BaseModel):
    id_nutricionista = AutoField(primary_key=True)
    foto = CharField(200)
    nome = CharField(200)
    senha = CharField(400)
    frase_secreta = CharField(200)

    @staticmethod
    def autocomplete():
        result = Nutricionista.select(Nutricionista.nome)
        nutricionistas = [model_to_dict(nut)["nome"] for nut in result]
        return json.dumps(nutricionistas)

    @staticmethod
    def buscar(nome):
        try:
            nutricionista = Nutricionista.select().where(Nutricionista.nome == nome).get()
            return nutricionista.id_nutricionista
        except Exception as e:
            return u"" + str(e)


class Paciente(BaseModel):
    id_paciente = AutoField(primary_key=True)
    id_endereco = ForeignKeyField(Endereco, column_name="id_endereco")
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
    
    @staticmethod
    def autocomplete():
        result = Paciente.select(Paciente.nome)
        pacientes = [model_to_dict(pac)["nome"] for pac in result]
        return json.dumps(pacientes)

    @staticmethod
    def buscar(nome):
        try:
            paciente = Paciente.select().where(Paciente.nome == nome).get()
            return paciente
        except Exception as e:
            return u"" + str(e)



class Avaliacao_Fisica (BaseModel):
    id_avaliacao = AutoField(primary_key=True)
    id_paciente = ForeignKeyField(Paciente, column_name="id_paciente" , backref="avaliacao_fisica")
    porcentagem_gordura = DoubleField()
    metabolismo_basal = DoubleField()
    porcentagem_massa_muscular = DoubleField()
    altura = DoubleField()
    imc = DoubleField()
    porcentagem_massa_magra = DoubleField()
    pressao = DoubleField()
    objetivo = CharField(450)
    data = CharField()
    peso = DoubleField()
    observacoes = CharField(450)

    @staticmethod
    def listarAvaliacao(pagina=1):
        try:
            lista = Avaliacao_Fisica.select().order_by(Avaliacao_Fisica.id_paciente).paginate(pagina, 10)
            return lista
        except Exception, e:
            return e

    @staticmethod
    def autocomplete():
        result = Dieta.select(Dieta.nome_dieta)
        dietas = [model_to_dict(diet)["nome_dieta"] for diet in result]
        return json.dumps(dietas)




class Consulta(BaseModel):
    id_consulta = AutoField(primary_key=True)
    id_paciente = ForeignKeyField(Paciente, column_name="id_paciente", backref="consulta")
    id_avaliacao = ForeignKeyField(Avaliacao_Fisica, column_name="id_avaliacao", backref="consulta")
    id_dieta = ForeignKeyField(Dieta, column_name="id_dieta", backref="consulta")
    id_nutricionista = ForeignKeyField(Nutricionista, column_name="id_nutricionista", backref="consulta")
    objetivo = CharField(450)
    proxima_consulta = CharField(200)
    data = CharField(15)

    @staticmethod
    def listarConsulta(pagina=1):
        try:
            lista = Consulta.select().order_by(Consulta.id_paciente).paginate(pagina, 10)
            return lista
        except Exception, e:
            return e


