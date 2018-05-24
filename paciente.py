from jinja2 import TemplateNotFound
from flask import Flask, render_template, request, url_for, redirect, Blueprint, abort
from NutripowerMysql import Alimento, db, Paciente, Refeicao, Dieta, Alimento_Refeicao, Refeicoes_Dieta
import json
from playhouse.shortcuts import model_to_dict

paciente_pages = Blueprint('paciente_pages', __name__,
                        template_folder='templates')

app = paciente_pages
##Paciente##
@app.route('/CadastroPaciente/', methods=["GET", "POST"])
def cadastraPaciente():
    if request.method=="POST":
        try:
            p = Paciente()
            p.nome = request.form["nome"]
            p.idade = request.form["idade"]
            p.peso = request.form["peso"]
            p.altura = request.form["altura"]
            p.cpf = request.form["cpf"]
            p.atividade_fisica = request.form["atividade"]
            p.sexo = request.form["sexo"]
            p.telefone = request.form["telefone"]
            p.email = request.form["email"]

            p.save()
            return render_template("/Paciente/Cadastro.html", form={})
        
        except Exception as e:
            return e
    else:
	        return render_template("/Paciente/Cadastro.html", form={})

@app.route('/ListarPacientes/', methods=["GET", "POST"])
def ListarPacientes():
    try:
        pagina = request.args.get("pag")
        
        lista = listarPacientes(pagina=pagina)
        return render_template('/Paciente/Listar.html', lista=lista)   
    except Exception, e:
        return u""+ str(e)

def listarPacientes(pagina=1):
    p = 1
    try:
        if pagina == None:
            pagina = p
            lista = Paciente.select().order_by(Paciente.nome).paginate(pagina, 10)
            return lista
        else:
            lista = Paciente.select().order_by(Paciente.nome).paginate(pagina, 10)
            return lista
    except Exception, e:
        return e
   
@app.route('/ExibirPacientes/', methods=["GET", "POST"])
def BuscaListaPacientes():
    result = Paciente.select(Paciente.nome)
    paciente = [model_to_dict(p)["nome"] for p in result]
    return render_template('/Paciente/Exibir.html', paciente=json.dumps(paciente), form={})

@app.route('/BuscarPaciente/', methods=["GET"])
def buscarPaciente():
    try:   
        nome = request.args.get('busca')
        paciente = Paciente.select().where(Paciente.nome == nome).get()
        return redirect("/Paciente/ExibirPacientes/%d/" % paciente.id_paciente)
    except Exception as e:
        return u""+ str(e)

@app.route('/ExibirPacientes/<id>/')
def exibirPacienteBuscado(id):
    try:
        result = Paciente.select(Paciente.nome)
        pacientes = [model_to_dict(p)["nome"] for p in result]
        paciente = Paciente.select().where(Paciente.id_paciente == id).get()
        return render_template('/Paciente/Exibir.html', paciente=paciente, pacientes=json.dumps(pacientes))
    except Exception as e:
        return u"" +str(e)

@app.route('/RemoverPaciente/', methods=["GET", "POST"])
def RemoverPaciente():
    if request.method == 'POST':
        try:
            cpf = request.form["cpf"]
            Paciente.delete().where(Paciente.cpf == cpf).execute()
            msg = "Paciente excluido com sucesso!"
            return render_template('/Paciente/Exibir.html', msg=msg)
        except Exception as e:
            return render_template('/Paciente/Exibir.html', msg=e)
      
@app.route('/BuscarPacienteAlterar/', methods=["GET"])
def buscarPacienteAlterar():
    try:   
        nome = request.args.get('busca')
        paciente = Paciente.select().where(Paciente.nome == nome).get()
        return redirect("/Paciente/AlterarPaciente/%d/" % paciente.id_paciente)
    except Exception as e:
        return u""+ str(e)

@app.route('/AlterarPaciente/<id>/')
def exibirPacienteAlterar(id):
    if request.method == 'POST':
        try:
            result = Paciente.select(Paciente.nome)
            pacientes = [model_to_dict(p)["nome"] for p in result]
            p = Paciente.select().where(Paciente.id_paciente == id).get()
            p.nome = request.form["nome"]
            p.idade = request.form["idade"]
            p.peso = request.form["peso"]
            p.altura = request.form["altura"]
            p.cpf = request.form["cpf"]
            p.atividade_fisica = request.form["atividade"]
            p.sexo = request.form["sexo"]
            p.telefone = request.form["telefone"]
            p.email = request.form["email"]
            p.save()
            msg = "Paciente Alterado com sucesso!"
            return render_template('/Paciente/Alterar.html', msg=msg ,paciente=p, pacientes=json.dumps(pacientes))
        except Exception as e:
            return render_template("/Paciente/Alterar.html", id = id,  msg = u"" +str(e), form = request.form.to_dict())
    else:
        p = Paciente.get(id)
        return render_template("/Paciente/Alterar.html",id = id, form=model_to_dict(p))

##Paciente##