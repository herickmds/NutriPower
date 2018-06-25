from jinja2 import TemplateNotFound
from flask import Flask, render_template, request, url_for, redirect, Blueprint, abort
from NutripowerMysql import Avaliacao_Fisica, db, Paciente
import json
from playhouse.shortcuts import model_to_dict
import math

avaliacao_pages = Blueprint('avaliacao_pages', __name__,
                        template_folder='templates')

app = avaliacao_pages

#avaliacaofisica#

@app.route('/CadastroAvaliacao/', methods=["GET", "POST"])
def CadastroAvaliacao():
    pacientes = Paciente.autocomplete()
    form={}

    if request.method=="POST":
        nome = request.form["busca"]
        paciente = Paciente.buscar(nome)
        return render_template("/AvaliacaoFisica/Cadastro.html", **locals())
    else:
	    return render_template("/AvaliacaoFisica/buscaPaciente.html", **locals())


@app.route('/CadastroAvaliacao/<id_paciente>/', methods=["GET","POST"])
def BuscarPaciente(id_paciente):
    form={}
    if request.method=="POST":
        try:
            paciente = Paciente.get_by_id(id_paciente)
            af = Avaliacao_Fisica()
            h = paciente.altura
            peso = paciente.peso
            sexo = paciente.sexo
            af.id_paciente = id_paciente   
            af.altura = h
            af.peso = peso
            quadril = 0
            af.pressao = request.form['pressao']
            af.objetivo = request.form['objetivo']
            af.data = request.form['data']
            af.observacoes = request.form['observacoes']
            af.porcentagem_gordura = request.form['gordura']
            af.metabolismo_basal = request.form['metabolismobasal']
            af.porcentagem_massa_muscular = request.form['massamuscular']
            imc = IMC(h,peso,sexo)
            af.imc = imc
            af.porcentagem_massa_magra = request.form['massamagra']
            af.save()
            return render_template('/AvaliacaoFisica/Cadastro.html', **locals())
        except Exception, e:
            return str(e)


def IMC(h,peso,sexo):
    h = float(h)
    peso = float(peso)
    sexo = sexo
    if (sexo == "M"):
        imc = peso / h ** 2
        return imc
    else:
        imc = peso / h ** 2
        return imc

@app.route('/ListarAvaliacao/', methods=["GET","POST"])
def ListarAvaliacao():
    try:
        pagina = request.args.get("page")
        tamanho = [t for t in Avaliacao_Fisica.select().order_by(Avaliacao_Fisica.id_paciente)]
        n = len(tamanho)
        if (n%10) > 1:
            paginacoes = ((n/10) + 1)
        else:
            paginacoes = (n/10)

        if(pagina == None):
            pagina = 1
        if pagina == 0:
            pagina = 1
            lista = Avaliacao_Fisica.listarAvaliacao(pagina=pagina)
            return render_template('/AvaliacaoFisica/Listar.html', paginacoes=paginacoes, lista=lista, page=int(pagina))
        lista = Avaliacao_Fisica.listarAvaliacao(pagina=int(pagina))
        return render_template('/AvaliacaoFisica/Listar.html', paginacoes=paginacoes, lista=lista, page=int(pagina))
    except Exception, e:
        return u""+ str(e)


@app.route('/Remover/<id>/', methods=["GET","POST"])
def Remover(id):
    try:
        Avaliacao_Fisica.delete_by_id(id)
        return redirect('/AvaliacaoFisica/ListarAvaliacao')
    except Exception, e:
        return u""+ str(e)

  
#avaliacaofisica#
