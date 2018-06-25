from jinja2 import TemplateNotFound
from flask import Flask, render_template, request, url_for, redirect, Blueprint, abort
from NutripowerMysql import Alimento, db, Paciente, Refeicao, Dieta, Alimentos_Refeicao, Refeicoes_Dieta
import json
from playhouse.shortcuts import model_to_dict

refeicao_pages = Blueprint('refeicao_pages', __name__,
                        template_folder='templates')

app = refeicao_pages

lista_alimentos = []
##Refeicao##
@app.route('/CadastroRefeicao/', methods=["GET", "POST"])
def cadastraRefeicao():
    if request.method=="POST":
        try:
            r = Refeicao()
            nome_refeicao = request.form["nome"]
            r.nome_refeicao = nome_refeicao
            horario_refeicao = request.form["horario"]
            r.horario_refeicao = horario_refeicao
            r.save()
            return redirect("/Refeicao/CadastroRefeicao/%d/" % r.id_refeicao)
        
        except Exception as e:
            return e[0]
    else:
	    return render_template("/Refeicao/Cadastro.html",form={},msg='cad')


@app.route('/CadastroRefeicao/<id_refeicao>/', methods=["GET", "POST"])
def adicionaAlimentoRefeicao(id_refeicao):
    alimentos=Alimento.autocomplete()
    form=request.form.to_dict()
    refeicao = Refeicao.get_by_id(int(id_refeicao))
    a = request.args.get('busca')
    if a:
        try:
            alimento = Alimento.select().where(Alimento.nome == a).get()
            if alimento is not None:
                porcao = request.args.get('porcao')
                ar = Alimentos_Refeicao()
                ar.id_refeicao = refeicao.id_refeicao
                ar.id_alimento =  alimento.id_alimento
                ar.porcao = porcao
                ar.save()
                return redirect('/Refeicao/CadastroRefeicao/%s/'% id_refeicao)
            else:
                msg="Alimento nao encontrado!"
        
        except Exception as e:
            return e
    else:
	    return render_template("/Refeicao/CadastrarAlterar.html", Ref=Refeicao, **locals())


@app.route('/ListarRefeicoes/')
def listar():
    try:
        pagina = request.args.get("page")
        tamanho = [t for t in Refeicao.select().order_by(Refeicao.nome_refeicao)]
        n = len(tamanho)
        if (n%10) > 1:
            paginacoes = ((n/10) + 1)
        else:
            paginacoes = (n/10)

        if(pagina == None):
            pagina = 1
        if pagina == 0:
            pagina = 1
            lista = Refeicao.listarRefeicao(pagina=pagina)
            return render_template('/Refeicao/Listar.html', paginacoes=paginacoes, lista=lista, page=int(pagina))
        lista = Refeicao.listarRefeicao(pagina=int(pagina))
        return render_template('/Refeicao/Listar.html', paginacoes=paginacoes, lista=lista, page=int(pagina))
    except Exception, e:
        return u""+ str(e)



@app.route('/ExibirRefeicao/', methods=["GET", "POST"])
def BuscaListaRefeicoes():
    refeicoes = Refeicao.autocomplete()
    return render_template('/Refeicao/Exibir.html', **locals())

@app.route('/BuscarRefeicao/', methods=["GET"])
def buscarRefeicao():
    nome = request.args.get('busca')
    refeicao = Refeicao.buscar(nome)
    return redirect("/Refeicao/ExibirRefeicao/%d/" % refeicao)

@app.route('/ExibirRefeicao/<id>/')
def exibirRefeicaoBuscado(id):
    form = {}
    alimentos=Alimento.autocomplete()
    refeicoes = Refeicao.autocomplete()
    try:
        refeicao = Refeicao.select().where(Refeicao.id_refeicao == id).get()
        return render_template('/Refeicao/CadastrarAlterar.html', **locals())
    except Exception as e:
        return u"" +str(e)


@app.route('/AlterarRefeicao/')
def AlterarRefeicao():
    try:
        refeicoes = Refeicao.autocomplete()
        nome = request.args.get('busca')
        if nome:
            refeicao = Refeicao.buscar(nome)
            return redirect("/Refeicao/ExibirRefeicaoAlterar/%d/" % refeicao)
        else:
            return render_template('/Refeicao/BuscaRefeicaoAlterar.html', **locals())
    except Exception as e:
        return u"" +str(e)


@app.route('/ExibirRefeicaoAlterar/<id>/', methods=["GET", "POST"])
def alterar(id):
    try:
        form = {}
        alimentos=Alimento.autocomplete()
        refeicoes = Refeicao.autocomplete()
        refeicao = Refeicao.select().where(Refeicao.id_refeicao == id).get()
        ar = Alimentos_Refeicao.select().where(Alimentos_Refeicao.id_refeicao == id)
        return render_template('/Refeicao/CadastrarAlterar.html', **locals())
    except Exception as e:
        return u"" +str(e)


@app.route('/AlterarRefeicao/<id_refeicao>/<id_alimento>/', methods=["GET", "POST"])
def alteraAlimentoRefeicao(id_refeicao,id_alimento):
    nome = request.args.get('busca')
    id_Ali = Alimento.buscar(nome)
    try:
        alimentos=Alimento.autocomplete()
        ar = Alimentos_Refeicao.select().where(Alimentos_Refeicao.id_refeicao == id_refeicao and Alimentos_Refeicao.id_alimento == id_alimento)
        ar.id_alimento = id_Ali
        ar.porcao = request.form['porcao']
        ar.save()
        r = Refeicao.get_by_id(id_refeicao)
        r.nome_refeicao = request.form['nome']
        r.horario_refeicao = request.form['horario']
        r.save()
        form=request.form.to_dict()
        return render_template('/Refeicao/CadastrarAlterar.html', **locals())
    except Exception as e:
        return u"" +str(e)


@app.route('/RemoverRefeicao/<id>/', methods=["GET", "POST"])
def RemoverRefeicao(id):
    refeicoes = Refeicao.autocomplete()
    try:
        id_ref = int(id)
        Refeicao.delete_by_id(id_ref)
        ar = Alimentos_Refeicao.select().where(Alimentos_Refeicao.id_refeicao == int(id_ref) and Alimentos_Refeicao.id_alimento == id).get()
        ar.delete_instance()
        
        msg = "Refeicao deletada com sucesso!"
        return redirect('/Refeicao/ListarRefeicoes/')
    except Exception as e: 
        return u"" +str(e)


@app.route('/RemoverAlimentoRefeicao/<id_refeicao>/<id>/', methods=["GET", "POST"])
def RemoverAlimentoRefeicao(id_refeicao,id):
    refeicoes = Refeicao.autocomplete()
    try:
        ar = Alimentos_Refeicao.select().where(Alimentos_Refeicao.id_refeicao == int(id_refeicao) and Alimentos_Refeicao.id_alimento == id).get()
        ar.delete_instance()
        msg = "Alimento deletado da refeicao com sucesso!"
        return redirect('/Refeicao/ExibirRefeicaoAlterar/%d/' % int(id_refeicao))
    except Exception as e:
            return u"" +str(e)


##Refeicao##