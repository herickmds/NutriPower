#!/usr/bin/python
# -*- coding: utf-8 -*-
from jinja2 import TemplateNotFound
from flask import Flask, render_template, request, url_for, redirect, Blueprint, abort
from NutripowerMysql import Alimento, db, Paciente, Pais, Endereco, Estado, Cidade, Bairro
import json
from playhouse.shortcuts import model_to_dict
from pycep_correios import consultar_cep
from pycep_correios.excecoes import CEPInvalido
from werkzeug.utils import secure_filename
from login import login_required


paciente_pages = Blueprint('paciente_pages', __name__,
                           template_folder='templates')

app = paciente_pages
##Paciente##


def processa_upload(name_do_input):
    if name_do_input not in request.files:
        return ""
    else:
        arquivo_temporario = request.files[name_do_input]
        nome_do_arquivo = secure_filename(arquivo_temporario.filename)
        caminho_do_arquivo = "static/dist/img/" + nome_do_arquivo
        arquivo_temporario.save(caminho_do_arquivo)
        url_do_arquivo = "/"+caminho_do_arquivo
        return url_do_arquivo


@app.route('/CadastroPaciente/', methods=["GET", "POST"])
@login_required
def cadastraPaciente():
    if request.method == "POST":
        try:
            p = Paciente()
            foto = processa_upload("foto")
            p.foto = foto
            p.nome = request.form["nome"]
            p.idade = request.form["idade"]
            peso = request.form["peso"]
            p.peso = str(peso).replace(",", ".")
            h = request.form["altura"]
            p.altura = str(h).replace(",", ".")
            p.cpf = request.form["cpf"]
            p.atividade_fisica = request.form["atividade"]
            if request.form["sexo"] == 'Masculino':
                p.sexo = 'M'
            else:
                p.sexo = 'F'
            p.telefone = request.form["telefone"]
            p.email = request.form["email"]
            cep = request.form['cep']
            pais = "Brasil"
            nome_estado = request.form['uf']
            nome_bairro = request.form['bairro']
            nome_rua = request.form['rua']
            nome_cidade = request.form['cidade']
            numero_casa = request.form["num_casa"]
            complemento = request.form["complemento"]
            p.id_endereco = endereco(
                pais, nome_rua, nome_bairro, nome_cidade, nome_estado, cep, numero_casa, complemento)
            p.save()
            return render_template("/Paciente/Cadastro.html", form=request.form.to_dict(), foto=foto, msg='ok')
        except Exception as e:
            return render_template("/Paciente/Cadastro.html", form={}, msg_error=e[0])
    else:
        return render_template("/Paciente/Cadastro.html", form={}, msg='cad')


def endereco(pais, nome_rua, nome_bairro, nome_cidade, nome_estado, cep, numero_casa, complemento):
    try:
        p = Pais()
        p.nome_pais = pais
        p.save()
        e = Estado()
        e.nome_estado = nome_estado
        e.id_pais = p.id_pais
        e.save()
        c = Cidade()
        c.nome_cidade = nome_cidade
        c.id_estado = e.id_estado
        c.save()
        b = Bairro()
        b.nome_bairro = nome_bairro
        b.id_cidade = c.id_cidade
        b.save()
        r = Endereco()
        r.nome_rua = nome_rua
        r.id_pais = p.id_pais
        r.id_estado = e.id_estado
        r.id_cidade = c.id_cidade
        r.id_bairro = b.id_bairro
        r.cep = cep
        r.numero_casa = numero_casa
        r.complemento = complemento
        r.save()
        return r.id_endereco
    except Exception as e:
        return render_template("/Paciente/Cadastro.html", form={}, msg_error=e[0])


@app.route('/ListarPacientes/', methods=["GET"])
@login_required
def ListarPacientes():
    try:
        pagina = request.args.get("page")
        
        tamanho = [t for t in Paciente.select().order_by(Paciente.nome)]
        n = len(tamanho)
        if (n%10) > 1:
            paginacoes = ((n/10) + 1)
        else:
            paginacoes = (n/10)

        if(pagina == None):
            pagina = 1
        if pagina == 0:
            pagina = 1
            lista = listarPacientes(pagina=pagina)
            return render_template('/Paciente/Listar.html', lista=lista, paginacoes=paginacoes, page=int(pagina))
        lista = listarPacientes(pagina=int(pagina))
        return render_template('/Paciente/Listar.html', lista=lista, page=int(pagina), paginacoes=paginacoes)
    except Exception, e:
        return render_template("/Paciente/Listar.html", msg_error=e[0])


def listarPacientes(pagina=1):
    try:
        lista = Paciente.select().order_by(Paciente.nome).paginate(pagina, 10)
        return lista
    except Exception, e:
        return render_template("/Paciente/Cadastro.html", msg_error=e[0])


@app.route('/ExibirPacientes/', methods=["GET", "POST"])
@login_required
def BuscaListaPacientes():
    result = Paciente.select(Paciente.nome)
    paciente = [model_to_dict(p)["nome"] for p in result]
    return render_template('/Paciente/Exibir.html', paciente=json.dumps(paciente), form={})


@app.route('/BuscarPaciente/', methods=["GET"])
@login_required
def buscarPaciente():
    try:
        nome = request.args.get('busca')
        paciente = Paciente.select().where(Paciente.nome == nome).get()
        return redirect("/Paciente/ExibirPacientes/%d/" % paciente.id_paciente)
    except Exception as e:
        return u"" + str(e)


@app.route('/ExibirPacientes/<id>/')
@login_required
def exibirPacienteBuscado(id):
    try:
        result = Paciente.select(Paciente.nome)
        pacientes = [model_to_dict(p)["nome"] for p in result]
        paciente = Paciente.select().where(Paciente.id_paciente == id).get()
        return render_template('/Paciente/Exibir.html', paciente=paciente, pacientes=json.dumps(pacientes))
    except Exception as e:
        return u"" + str(e)


@app.route('/RemoverPaciente/<id>/', methods=["GET", "POST"])
@login_required
def RemoverPaciente(id):
    if request.method == 'POST':
        try:
            p = Paciente.select().where(Paciente.id_paciente == id).get()
            p.delete_instance()
            msg = "Paciente excluido com sucesso!"
            return redirect('/Paciente/ExibirPacientes/')
        except Exception as e:
            return render_template('/Paciente/ExibirPacientes/', msg=e[0])


@app.route('/BuscarPacienteAlterar/', methods=["GET"])
@login_required
def buscarPacienteAlterar():
    try:
        nome = request.args.get('busca')
        paciente = Paciente.select().where(Paciente.nome == nome).get()
        return redirect("/Paciente/AlterarPaciente/%d/" % paciente.id_paciente)
    except Exception as e:
        return u"" + str(e)


@app.route('/AlterarPaciente/<id>/', methods=["GET", "POST"])
@login_required
def exibirPacienteAlterar(id):
    p = Paciente.select().where(Paciente.id_paciente == id).get()
    result = Paciente.select(Paciente.nome)
    pacientes = [model_to_dict(pa)["nome"] for pa in result]
    if request.method == 'POST':
        try:
            p.nome = request.form["nome"]
            p.idade = request.form["idade"]
            peso = request.form["peso"]
            p.peso = str(peso).replace(",", ".")
            h = request.form["altura"]
            p.altura = str(h).replace(",", ".")
            p.cpf = request.form["cpf"]
            p.atividade_fisica = request.form["atividade"]
            if request.form["sexo"] == 'Masculino':
                p.sexo = 'M'
            else:
                p.sexo = 'F'
            p.telefone = request.form["telefone"]
            p.email = request.form["email"]
           
            p.save()
            msg = "Paciente Alterado com sucesso!"
            return render_template('/Paciente/Alterar.html', msg=msg, paciente=p, pacientes=json.dumps(pacientes))
        except Exception as e:
            return render_template("/Paciente/Alterar.html", id=id,  msg=u"" + str(e), form=request.form.to_dict() ,pacientes=json.dumps(pacientes))
    else:
        msg = "alt"
        return render_template("/Paciente/Alterar.html",msg=msg, id=id, paciente=p, form=model_to_dict(p), pacientes=json.dumps(pacientes))


@app.route('/AlterarPaciente/', methods=["GET", "POST"])
@login_required
def AlterarPaciente():   
    result = Paciente.select(Paciente.nome)
    pacientes = [model_to_dict(p)["nome"] for p in result]
    msg = "alt"
    return render_template('/Paciente/Alterar.html',msg=msg, pacientes=json.dumps(pacientes), form={})


##Paciente##
