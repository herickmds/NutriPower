"""Flask Login Example and instagram fallowing find"""
#!/usr/bin/python
# -*- coding: latin-1 -*-
from peewee import mysql ,CharField ,Model, MySQLDatabase, AutoField, IntegerField, DoubleField, ForeignKeyField, DateField
import peewee as pw
from jinja2 import TemplateNotFound
from flask import Flask, render_template, request, url_for, redirect, Blueprint, abort, session
from NutripowerMysql import Nutricionista
import json
from playhouse.shortcuts import model_to_dict
import os
from functools import wraps
from werkzeug.utils import secure_filename
from flask import g, request, redirect, url_for

login_pages = Blueprint('login_pages', __name__,
                        template_folder='templates')

app = login_pages


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
        	return redirect('/')
        return f(*args, **kwargs)
    return decorated_function


def processa_upload(name_do_input):
    if name_do_input not in request.files:
        return ""
    else:
        arquivo_temporario = request.files[name_do_input]
        nome_do_arquivo = secure_filename(arquivo_temporario.filename)
        caminho_do_arquivo = "static/dist/img/" + nome_do_arquivo
        arquivo_temporario.save(caminho_do_arquivo)
        url_do_arquivo = "/"+caminho_do_arquivo
        return url_do_arquivo


@app.route('/', methods=['GET', 'POST'])
def home():
	""" Session control"""
	if not session.get('logged_in'):
		return render_template('index.html')
	else:
		if request.method == 'POST':
			session['username'] = request.form['username']
			id_nut = Nutricionista.buscar(session['username'])
			user = Nutricionista.get_by_id(id_nut)
			session['senha'] = user.senha
			session['frase_secreta'] = user.frase_secreta
			session['foto'] = user.foto
			session['id'] = user.id_nutricionista
			return redirect('/Inicio/inicio/')
		return render_template('index.html', **locals())


@app.route('/login/', methods=['GET', 'POST'])
def login():
	"""Login Form"""
	if request.method == 'GET':
		return render_template('/login/login.html')
	else:
		name = request.form['username']
		passw = request.form['password']
		try:
			data = Nutricionista.filter(nome=name, senha=passw).first()
			if data is not None:
				session['logged_in'] = True
				return home()
			else:
				return 'Dont Login'
		except Exception, e:
			return e[0]

@app.route('/register/', methods=['GET', 'POST'])
def register():
	"""Register Form"""
	if request.method == 'POST':
		foto = processa_upload("foto")
		new_user = Nutricionista(foto=foto, nome=request.form['username'], senha=request.form['password'], 
		frase_secreta=request.form['frase_secreta'])
		new_user.save()
		return render_template('/login/login.html')
	return render_template('/login/register.html')

@app.route("/logout/")
def logout():
	"""Logout Form"""
	session['logged_in'] = False
	return home()



@app.route("/RecuperarSenha/", methods=['GET', 'POST'])
def RecuperarSenha():
	if request.method == 'GET':
		return render_template('/login/recuperaSenha.html')
	if request.method == 'POST':
		name = request.form['username']
		frase_secreta = request.form['frase_secreta']
	
		data = Nutricionista.filter(nome=name, frase_secreta=frase_secreta).first()
		if data is not None:
			session['logged_in'] = True
			return home()
		else:
			session['mensage'] = 'Dont Login'
			return session['mensage']


@app.route("/Perfil/", methods=['GET', 'POST'])
def Perfil():
	if request.method == 'GET':
		return render_template('/login/perfil.html')
	if request.method == 'POST':
		name = request.form['username']
		frase_secreta = request.form['frase_secreta']
	
		data = Nutricionista.filter(nome=name, frase_secreta=frase_secreta).first()
		if data is not None:
			session['logged_in'] = True
			return home()
		else:
			return 'Dont Login'



@app.route('/update/<id>/', methods=['GET', 'POST'])
def update(id):
	if request.method == 'POST':
		nut = Nutricionista.get_by_id(id)
		foto = processa_upload("foto")
		nut.foto=foto 
		nut.nome=request.form['username']
		nut.senha=request.form['password']
		nut.frase_secreta=request.form['frase_secreta']
		nut.save()
		return render_template('/login/perfil.html')
	return render_template('/login/update.html')
