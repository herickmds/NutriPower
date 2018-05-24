from jinja2 import TemplateNotFound
from flask import Flask, render_template, request, url_for, redirect, Blueprint, abort
from NutripowerMysql import Alimento, db, Paciente, Refeicao, Dieta, Alimento_Refeicao, Refeicoes_Dieta
import json
from playhouse.shortcuts import model_to_dict

refeicao_pages = Blueprint('refeicao_pages', __name__,
                        template_folder='templates')

app = refeicao_pages

lista_alimentos_refeicao = []

##Refeicao##
@app.route('/CadastroRefeicao/', methods=["GET", "POST"])
def cadastraRefeicao():
    if request.method=="POST":
        try:
            ar = Alimento_Refeicao()
            if ar.id_alimentos_refeicao == None:
                ar.id_alimentos_refeicao = 1
            else:
                ar.id_alimentos_refeicao += ar.id_alimentos_refeicao
            for a in lista_alimentos_refeicao:
                ar.id_alimento = a.id_alimento
            ar.save()

            r = Refeicao()
            r.nome_refeicao = request.form["nome"]
            r.horario_refeicao = request.form["horario"]
            r.id_alimentos_refeicao = ar.id_alimentos_refeicao
            for a in lista_alimentos_refeicao:
                r.proteinas += "{0:.2f}".format(float(a.proteina))
                r.carboidratos += "{0:.2f}".format(float(a.carboidrato))
                r.gorduras += "{0:.2f}".format(float(a.lipidio))
            
            r.save()
            return render_template("/Refeicao/Cadastro.html", form={})
            lista_alimentos_refeicao[:] = []
        
        except Exception as e:
            return e
    else:
	        return render_template("/Refeicao/Cadastro.html", form={}, refeicao=r, lista=lista_alimentos_refeicao)

@app.route('/BuscarAlimentoRefeicao/', methods=["GET", "POST"])
def BuscarAlimentoRefeicao():
    try:   
        nome = request.args.get('busca')
        alimento = Alimento.select().where(Alimento.nome == nome).get()
        return redirect("/Refeicao/SelecionarAlimentoRefeicao/%d/" % alimento.id_alimento)
    except Exception as e:
        return u""+ str(e)

@app.route('/SelecionarAlimentoRefeicao/<id>/')
def AlimentoRefeicaoBuscado(id):
    try:
        result = Alimento.select(Alimento.nome)
        alimentos = [model_to_dict(ali)["nome"] for ali in result]
        alimento = Alimento.select().where(Alimento.id_alimento == id).get()
        lista_alimentos_refeicao.append(alimento)
        return render_template('/Refeicao/Cadastro.html', alimento=alimento, alimentos=json.dumps(alimentos))
    except Exception as e:
        return u"" +str(e)


@app.route('/ListarRefeicoes/', methods=["GET", "POST"])
def ListarRefeicao():
    try:
        pagina = request.args.get("pag")
        lista = listarRefeicoes(pagina=pagina)
        return render_template('/Refeicao/Listar.html', lista=lista)   
    except Exception, e:
        return u""+ str(e)

def listarRefeicoes(pagina=1):
    p = 1
    try:
        if pagina == None:
            pagina = p
            lista = Refeicao.select().order_by(Refeicao.nome_refeicao).paginate(pagina, 10)
            return lista
        else:
            lista = Refeicao.select().order_by(Refeicao.nome_refeicao).paginate(pagina, 10)
            return lista
    except Exception, e:
        return e
   
@app.route('/ExibirRefeicao/', methods=["GET", "POST"])
def BuscaListaRefeicoes():
    result = Refeicao.select(Refeicao.nome_refeicao)
    refeicao = [model_to_dict(p)["nome"] for p in result]
    return render_template('/Refeicao/Exibir.html', paciente=json.dumps(refeicao))

@app.route('/BuscarRefeicao/', methods=["GET"])
def buscarRefeicao():
    try:   
        nome = request.args.get('busca')
        refeicao = Refeicao.select().where(Refeicao.nome_refeicao == nome).get()
        return redirect("/Refeicao/ExibirRefeicao/%d/" % refeicao.id_refeicao)
    except Exception as e:
        return u""+ str(e)

@app.route('/Refeicao/ExibirRefeicao/<id>/')
def exibirRefeicaoBuscado(id):
    try:
        result = Refeicao.select(Refeicao.nome_refeicao)
        refeicoes = [model_to_dict(r)["nome"] for r in result]
        refeicao = Refeicao.select().where(Refeicao.id_refeicao == id).get()
        lista = Alimento_Refeicao.select().where(Alimento_Refeicao.id_alimentos_refeicao == refeicao.id_alimentos_refeicao)
        lista_alimentos = []
        for a in lista:
            lista_alimentos = Alimento.select().where(Alimento.id_alimento == a.id_alimento)

        return render_template('/Refeicao/Exibir.html', refeicao=refeicao, lista=lista_alimentos, refeicoes=json.dumps(refeicoes))
    except Exception as e:
        return u"" +str(e)


@app.route('/Refeicao/BuscarAlimentoAlterar', methods=["GET", "POST"])
def BuscarAlimentoAlterar():
    try:   
        nome = request.args.get('busca')
        alimento = Alimento.select().where(Alimento.nome== nome).get()
        task = "/Seleciona/NovoAlimento/"
        if task != None:
            return render_template('/Refeicao/Alterar.html', task=task)

        return redirect("/Refeicao/ExibirAlimentoAlterar/%d/" % alimento.id_alimento) 
        
    except Exception as e:
        return u""+ str(e)


@app.route('/Refeicao/ExibirAlimentoAlterar/<id>/')
def ExibirAlimentoAlterar(id, task):
    try:
        result = Refeicao.select(Refeicao.nome_refeicao)
        refeicoes = [model_to_dict(r)["nome"] for r in result]
        return render_template('/Refeicao/Alterar.html', refeicoes=json.dumps(refeicoes))
    except Exception as e:
        return u"" +str(e)

lista_alimentos_refeicao2 = []

@app.route('/BuscarAlimentoRefeicaoAlterar', methods=["GET", "POST"])
def BuscarAlimentoRefeicaoAlterar():
    try:   
        nome = request.args.get('busca')
        alimento = Alimento.select().where(Alimento.nome== nome).get()
        lista_alimentos_refeicao2.append(alimento)
    except Exception as e:
        return u""+ str(e)

@app.route('/AlterarRefeicao/<id>/')
def AlterarRefeicao(id):
    if request.method == 'POST':
        try:
            ar = Alimento_Refeicao()
            if ar.id_alimentos_refeicao == None:
                ar.id_alimentos_refeicao = 1
            else:
                ar.id_alimentos_refeicao += ar.id_alimentos_refeicao
            for a in lista_alimentos_refeicao:
                ar.id_alimento = a.id_alimento
            ar.save()

            result = Refeicao.select(Refeicao.nome_refeicao)
            refeicoes = [model_to_dict(x)["nome_refeicao"] for x in result]
            r = Refeicao.select().where(Refeicao.id_refeicao == id).get()
            r.nome_refeicao = request.form["nome"]
            r.horario_refeicao = request.form["horario"]
            r.id_alimentos_refeicao = ar.id_alimentos_refeicao
            for a in lista_alimentos_refeicao2:
                r.proteinas += "{0:.2f}".format(float(a.proteina))
                r.carboidratos += "{0:.2f}".format(float(a.carboidrato))
                r.gorduras += "{0:.2f}".format(float(a.lipidio))
            
            r.save()
            msg = "Refeicao alterada com sucesso!"
            return render_template('/Refeicao/Alterar.html', msg=msg ,refeicao=r, refeicoes=json.dumps(refeicoes))
            lista_alimentos_refeicao2[:] = [] 
        except Exception as e:
            return render_template("/Refeicao/Alterar.html", msg = u"" +str(e), form = request.form.to_dict())
    else:
        p = Refeicao.get(id)
        return render_template("/Refeicao/Alterar.html", form=model_to_dict(p))


@app.route('/RemoverRefeicao/', methods=["GET", "POST"])
def RemoverRefeicao():
    if request.method == 'POST':
        try:
            nome_refeicao = request.form["nome"]
            r = Refeicao.delete().where(Refeicao.nome_refeicao == nome_refeicao).get()
            Alimento_Refeicao.delete().where(Alimento_Refeicao.id_alimentos_refeicao == r.id_alimento_refeicao)
            msg = "Refeicao deletada com sucesso!"
            return render_template("/Refeicao/Exibir.html", msg=msg)
        except Exception as e:
            return e

##Refeicao##