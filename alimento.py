from jinja2 import TemplateNotFound
from flask import Flask, render_template, request, url_for, redirect, Blueprint, abort
from NutripowerMysql import Alimento, db, Paciente, Refeicao, Dieta, Alimentos_Refeicao, Refeicoes_Dieta
import json
from playhouse.shortcuts import model_to_dict

alimento_pages = Blueprint('simple_page', __name__,
                        template_folder='templates')

app = alimento_pages
##Alimento##
@app.route('/ExibirAlimento/<id>/')
def exibirBuscado(id):
    alimentos = Alimento.autocomplete()
    try:
        alimento = Alimento.select().where(Alimento.id_alimento == id).get()
        return render_template('/Alimento/Exibir.html', **locals())
    except Exception as e:
        return u"" +str(e)

@app.route('/ExibirAlimento/', methods=["GET", "POST"])
def exibirListar():
    alimentos = Alimento.autocomplete()
    return render_template('Alimento/Exibir.html', **locals())
    
@app.route('/BuscarAlimento/', methods=["GET"])
def buscar():
    try:   
        nome = request.args.get('busca')
        alimento = Alimento.buscar(nome)
        return redirect("/Alimento/ExibirAlimento/%d/" % alimento)
    except Exception as e:
        return u""+ str(e)

@app.route('/ListarAlimento/')
def listar():
    try:
        pagina = request.args.get("page")
        tamanho = [t for t in Alimento.select().order_by(Alimento.nome)]
        n = len(tamanho)
        if (n%10) > 1:
            paginacoes = ((n/10) + 1)
        else:
            paginacoes = (n/10)

        if(pagina == None):
            pagina = 1
        if pagina == 0:
            pagina = 1
            lista = Alimento.listar(pagina=pagina)
            return render_template('/Alimento/Listar.html', paginacoes=paginacoes, lista=lista, page=int(pagina))
        lista = Alimento.listar(pagina=int(pagina))
        return render_template('/Alimento/Listar.html', paginacoes=paginacoes, lista=lista, page=int(pagina))
    except Exception, e:
        return u""+ str(e)
        
##Alimento##
