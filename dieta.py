from jinja2 import TemplateNotFound
from flask import Flask, render_template, request, url_for, redirect, Blueprint, abort
from NutripowerMysql import Alimento, db, Paciente, Refeicao, Dieta, Alimentos_Refeicao, Refeicoes_Dieta
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
            r = Dieta()
            nome_dieta = request.form["nome"]
            r.nome_dieta = nome_dieta
            objetivo = request.form["objetivo"]
            r.objetivo = objetivo
            r.save()
            return redirect("/Dieta/CadastroDieta/%d/" % r.id_dieta)
        
        except Exception as e:
            return e[0]
    else:
	    return render_template("/Dieta/Cadastro.html",form={},msg='cad')


@app.route('/CadastroDieta/<id_dieta>/', methods=["GET", "POST"])
def adicionaRefeicaoDieta(id_dieta):
    refeicoes=Refeicao.autocomplete()
    form=request.form.to_dict()
    dieta = Dieta.get_by_id(int(id_dieta))
    r = request.args.get('busca')
    if r:
        try:
            refeicao = Refeicao.select().where(Refeicao.nome_refeicao == r).get()
            if refeicao is not None:
                rd = Refeicoes_Dieta()
                rd.id_refeicao = refeicao.id_refeicao
                rd.id_dieta = id_dieta
                rd.save()
                return redirect('/Dieta/CadastroDieta/%s/'% id_dieta)
            else:
                msg="Alimento nao encontrado!"

        except Exception as e:
            return e
    else:
	    return render_template("/Dieta/AlterarCadastrarDieta.html", Diet=Dieta, **locals())



@app.route('/ListarDietas/')
def listar():
    try:
        pagina = request.args.get("page")
        tamanho = [t for t in Dieta.select().order_by(Dieta.nome_dieta)]
        n = len(tamanho)
        if (n%10) > 1:
            paginacoes = ((n/10) + 1)
        else:
            paginacoes = (n/10)

        if(pagina == None):
            pagina = 1
        if pagina == 0:
            pagina = 1
            lista = Dieta.listarDieta(pagina=pagina)
            return render_template('/Dieta/Listar.html', paginacoes=paginacoes, lista=lista, page=int(pagina))
        lista = Dieta.listarDieta(pagina=int(pagina))
        return render_template('/Dieta/Listar.html', paginacoes=paginacoes, lista=lista, page=int(pagina))
    except Exception, e:
        return u""+ str(e)



@app.route('/ExibirDieta/', methods=["GET", "POST"])
def BuscaListaDieta():
    dietas = Dieta.autocomplete()
    return render_template('/Dieta/Exibir.html', **locals())

@app.route('/BuscarDieta/', methods=["GET"])
def buscarDieta():
    nome = request.args.get('busca')
    dieta = Dieta.buscar(nome)
    return redirect("/Dieta/ExibirDietaBuscada/%d/" % dieta)

@app.route('/ExibirDietaBuscada/<id>/')
def exibirDietaBuscado(id):
    form = {}
    refeicoes = Refeicao.autocomplete()
    try:
        dieta = Dieta.get_by_id(id)
        return render_template('/Dieta/AlterarCadastrarDieta.html', **locals())
    except Exception as e:
        return u"" +str(e)

@app.route('/ExibirDietaAlterar/<id>/', methods=["GET", "POST"])
def alterar(id):
    try:
        form = {}
        refeicoes = Refeicao.autocomplete()
        dieta = Dieta.select().where(Dieta.id_dieta == id).get()
        rd = Refeicoes_Dieta.select().where(Refeicoes_Dieta.id_dieta == id)
        return render_template('/Dieta/AlterarCadastrarDieta.html', **locals())
    except Exception as e:
        return u"" +str(e)


@app.route('/AlterarRefeicao/<id_refeicao>/<id_alimento>/', methods=["GET", "POST"])
def alteraRefeicaoDieta(id_refeicao,id_alimento):
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


@app.route('/RemoverDieta/<id>/', methods=["GET", "POST"])
def RemoverDieta(id):
    refeicoes = Refeicao.autocomplete()
    try:
        id_diet = int(id)
      
        rd = Refeicoes_Dieta.select().where(Refeicoes_Dieta.id_dieta == id_diet).get()
        rd.delete_instance()
        d = Dieta.select().where(Dieta.id_dieta == id_diet).get()
        d.delete_instance()
        
        msg = "Refeicao deletada com sucesso!"
        return redirect('/Dieta/ListarDietas/')
    except Exception as e: 
        return u"" +str(e)


@app.route('/RemoverRefeicaoDieta/<id_dieta>/<id>/', methods=["GET", "POST"])
def RemoverRefeicaoDieta(id_dieta,id):
    refeicoes = Refeicao.autocomplete()
    try:
        rd = Refeicoes_Dieta.select().where(Refeicoes_Dieta.id_dieta == int(id_dieta) and Refeicoes_Dieta.id_refeicao == id).get()
        rd.delete_instance()
        msg = "Alimento deletado da refeicao com sucesso!"
        return redirect('/Dieta/ExibirDietaAlterar/%d/' % int(id_dieta))
    except Exception as e:
            return u"" +str(e)


##Dieta##
