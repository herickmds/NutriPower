from flask import Flask, render_template, request, url_for, redirect
from NutripowerMysql import Paciente, db

db.connect()


app = Flask(__name__)


@app.route('/<task>', methods=["GET", "POST"])
def index(task=''):
        return render_template('index.html', task=task)
    


def cadastrar():
	if request.method=="POST":
		try:
			if request.form['usuario'] == "":
				raise Exception(u"usuario não informado!")	
			if request.form['email'] == "":
				raise Exception(u"email não informado!")
			p = Paciente
			p.usuario = request.form['usuario'] 
			p.email = request.form['email']
			p.nome_completo = request.form['nome_completo']
			p.senha = request.form['senha']
			p.biografia = request.form['biografia']
			p.foto_url = processa_upload("foto_url")
			p.save()
			return redirect("/")
		except Exception as error:
			return render_template("cadastrar.html", msg_error = error,	form = request.form.to_dict())
	else:
		return render_template("cadastrar.html", form={})

db.close()