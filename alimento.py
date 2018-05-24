from jinja2 import TemplateNotFound
from flask import Flask, render_template, request, url_for, redirect, Blueprint, abort
from NutripowerMysql import Alimento, db, Paciente, Refeicao, Dieta, Alimento_Refeicao, Refeicoes_Dieta
import json
from playhouse.shortcuts import model_to_dict

alimento_pages = Blueprint('simple_page', __name__,
                        template_folder='templates')

app = alimento_pages
##Alimento##
@app.route('/ExibirAlimento/<id>/')
def exibirBuscado(id):
    try:
        result = Alimento.select(Alimento.nome)
        alimentos = [model_to_dict(ali)["nome"] for ali in result]
        alimento = Alimento.select().where(Alimento.id_alimento == id).get()
        return render_template('/Alimento/Exibir.html', alimento=alimento, alimentos=json.dumps(alimentos))
    except Exception as e:
        return u"" +str(e)

@app.route('/ExibirAlimento/', methods=["GET", "POST"])
def exibirListar():
    result = Alimento.select(Alimento.nome)
    alimentos = [model_to_dict(ali)["nome"] for ali in result]
    return render_template('Alimento/Exibir.html', alimentos=json.dumps(alimentos))
    
@app.route('/BuscarAlimento/', methods=["GET"])
def buscar():
    try:   
        nome = request.args.get('busca')
        alimento = Alimento.select().where(Alimento.nome == nome).get()
        return redirect("/Alimento/ExibirAlimento/%d/" % alimento.id_alimento)
    except Exception as e:
        return u""+ str(e)

@app.route('/ListarAlimento/')
def listar():
    try:
        pagina = request.args.get("pag")
        
        lista = listarAlimentos(pagina=pagina)
        return render_template('/Alimento/Listar.html', lista=lista)   
    except Exception, e:
        return u""+ str(e)

def listarAlimentos(pagina=1):

    p = 1
    try:
        if pagina == None:
            pagina = p
            lista = Alimento.select().order_by(Alimento.nome).paginate(pagina, 10)
            return lista
        else:
            lista = Alimento.select().order_by(Alimento.nome).paginate(pagina, 10)
            return lista
    except Exception, e:
        return e

##Alimento##
