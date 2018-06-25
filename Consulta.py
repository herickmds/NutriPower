from jinja2 import TemplateNotFound
from flask import Flask, render_template, request, url_for, redirect, Blueprint, abort, session
from NutripowerMysql import Avaliacao_Fisica, db, Paciente, Consulta, Nutricionista, Dieta
import json
from playhouse.shortcuts import model_to_dict
import math

consulta_pages = Blueprint('consulta_pages', __name__,
                        template_folder='templates')

app = consulta_pages

#avaliacaofisica#

@app.route('/CadastroConsulta/<id_avaliacao>/', methods=["GET", "POST"])
def CadastroConsulta(id_avaliacao):
    form=request.form.to_dict()
    nome = session['username']

    nutricionista = Nutricionista.buscar(nome)
    af = Avaliacao_Fisica.get_by_id(id_avaliacao)
    c = Consulta()
    c.id_paciente = af.id_paciente
    c.id_avaliacao = id_avaliacao
 
    c.id_nutricionista = nutricionista
    c.objetivo = af.objetivo
    c.data = af.data
    
    dietas = Dieta.autocomplete()
    nome = request.args.get('busca')
    if nome:
        dieta = Dieta.buscar(nome)
        c.id_dieta = dieta
        return render_template("/Consulta/Cadastro.html", msg='ok', salvar="", **locals())
    
    
    if request.method=="POST":
        c.proxima_consulta = request.form['proxima_consulta']    
        c.save()
        return render_template("/Consulta/Cadastro.html",msg='ok', salvar="ok", **locals())


    return render_template("/Consulta/Cadastro.html", msg="", salvar="", **locals())



@app.route('/ListarConsulta/', methods=["GET","POST"])
def ListarAvaliacao():
    try:
        pagina = request.args.get("page")
        tamanho = [t for t in Consulta.select().order_by(Consulta.id_paciente)]
        n = len(tamanho)
        if (n%10) > 1:
            paginacoes = ((n/10) + 1)
        else:
            paginacoes = (n/10)

        if(pagina == None):
            pagina = 1
        if pagina == 0:
            pagina = 1
            lista = Consulta.listarConsulta(pagina=pagina)
            return render_template('/Consulta/Listar.html', paginacoes=paginacoes, lista=lista, page=int(pagina))
        lista = Consulta.listarConsulta(pagina=int(pagina))
        return render_template('/Consulta/Listar.html', paginacoes=paginacoes, lista=lista, page=int(pagina))
    except Exception, e:
        return u""+ str(e)


@app.route('/Remover/<id>/', methods=["GET","POST"])
def Remover(id):
    try:
        Consulta.delete_by_id(id)
        return redirect('/Consulta/ListarConsulta/')
    except Exception, e:
        return u""+ str(e)




@app.route('/Exibir/<id_consulta>/', methods=["GET", "POST"])
def Exibir(id_consulta):
    form=request.form.to_dict()
    nome = session['username']

    nutricionista = Nutricionista.buscar(nome)
    c = Consulta.select().where(Consulta.id_consulta == id_consulta).get()
    
    if request.method=="POST":
        c.proxima_consulta = request.form['proxima_consulta']    
        c.save()
        return render_template("/Consulta/Cadastro.html", msg="ok", salvar="ok", **locals())


    return render_template("/Consulta/Cadastro.html", msg="ok", exibir="ok", **locals())



  
#avaliacaofisica#
