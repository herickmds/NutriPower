from jinja2 import TemplateNotFound
from flask import Flask, render_template, request, url_for, redirect, Blueprint, abort
from NutripowerMysql import Alimento, db, Paciente, Refeicao, Dieta, Alimento_Refeicao, Refeicoes_Dieta
import json
from playhouse.shortcuts import model_to_dict

dieta_pages = Blueprint('dieta_pages', __name__,
                        template_folder='templates')

app = dieta_pages
##Dieta##
@app.route('/CadastroDieta/', methods=["GET", "POST"])
def cadastraDieta():
    if request.method=="POST":
        try:
            d = Dieta()
            d.nome_dieta = request.form["nome"]
            d.objetivo = request.form["objetivo"]
            lista_refeicoes = request.form["refeicao"]
            rd = Refeicoes_Dieta()
            if rd.id_refeicoes_deita == None:
                rd.id_refeicoes_deita = 1
            else:  
                rd.id_refeicoes_deita += 1

            caloria = ""
            proteina = ""
            gordura = ""
            carboidrato = ""

            for i in lista_refeicoes:
                rd.id_refeicao = i.id_refeicao
                r = Refeicao.get_by_id(i.id_refeicao)
                caloria += r.calorias
                proteina += r.proteinas
                gordura += r.gorduras
                carboidrato += r.carboidratos

            d.calorias = caloria
            d.proteinas = proteina
            d.carboidratos = carboidrato
            d.gorduras = gordura
           
            d.save()
            rd.save()
            return render_template("/Dieta/Cadastro.html", form={}, dieta=d)
        
        except Exception as e:
            return e
    else:
	        return render_template("/Dieta/Cadastro.html", form={}, dieta=d)


@app.route('/BuscarRefeicaoDieta/', methods=["GET", "POST"])
def BuscarRefeicaoDieta():
    try:   
        nome = request.args.get('busca')
        refeicao = Refeicao.select().where(Refeicao.nome_refeicao == nome).get()
        return redirect("/Dieta/ExibirDietaRefeicao/%d/" % refeicao.id_refeicao)
    except Exception as e:
        return u""+ str(e)


@app.route('/ExibirDietaRefeicao/<id>/')
def ExibirDietaRefeicao(id):
    try:
        result = Refeicao.select(Refeicao.nome_refeicao)
        refeicoes = [model_to_dict(r)["nome"] for r in result]
        refeicao = Refeicao.select().where(Refeicao.id_refeicao == id).get()
        return render_template('/Dieta/Cadastro.html', refeicao=refeicao, refeicoes=json.dumps(refeicoes))
    except Exception as e:
        return u"" +str(e)


@app.route('/ListarDietas/', methods=["GET", "POST"])
def ListarDieta():
    try:
        pagina = request.args.get("pag")
        
        lista = listarDietas(pagina=pagina)
        return render_template('/Dieta/Listar.html', lista=lista)   
    except Exception, e:
        return u""+ str(e)

def listarDietas(pagina=1):
    p = 1
    try:
        if pagina == None:
            pagina = p
            lista = Dieta.select().order_by(Dieta.nome_dieta).paginate(pagina, 10)
            return lista
        else:
            lista = Dieta.select().order_by(Dieta.nome_dieta).paginate(pagina, 10)
            return lista
    except Exception, e:
        return e
   
@app.route('/ExibirDieta/', methods=["GET", "POST"])
def BuscaListaDietas():
    result = Dieta.select(Dieta.nome_dieta)
    dietas = [model_to_dict(d)["nome"] for d in result]
    return render_template('/Dieta/Exibir.html', dietas=json.dumps(dietas))

@app.route('/BuscarDieta/', methods=["GET"])
def buscarDieta():
    try:   
        nome = request.args.get('busca')
        dieta = Dieta.select().where(Dieta.nome_dieta == nome).get()
        return redirect("/Dieta/ExibirDieta/%d/" % dieta.id_dieta)
    except Exception as e:
        return u""+ str(e)

@app.route('/ExibirDieta/<id>/')
def exibirDietaBuscado(id):
    try:
        result = Dieta.select(Dieta.nome_dieta)
        dietas = [model_to_dict(d)["nome"] for d in result]
        dieta = Dieta.select().where(Dieta.id_dieta == id).get()
        lista = Refeicoes_Dieta.select().where(Refeicoes_Dieta.id_refeicoes_deita == dieta.id_refeicoes_deita)
        return render_template('/Dieta/Exibir.html', lista=lista, dieta=dieta, dietas=json.dumps(dietas))
    except Exception as e:
        return u"" +str(e)

@app.route('/RemoverDieta/')
def RemoverDieta():
    try:
        nome_dieta = request.form["nome"]
        dieta = Dieta.select().where(Dieta.nome_dieta == nome_dieta).get()
        Refeicoes_Dieta.delete().where(Refeicoes_Dieta.id_refeicoes_deita == dieta.id_refeicoes_dieta).execute()
        dieta.delete()
        return render_template('/Dieta/Exibir.html', lista={}, dieta=dieta, dietas={})
    except Exception as e:
        return u"" +str(e)


##Dieta##
