from flask import Flask, render_template, request, url_for, redirect, session
import json
from playhouse.shortcuts import model_to_dict
from alimento import alimento_pages
from paciente import paciente_pages
from refeicao import refeicao_pages
from dieta import dieta_pages
from login import login_pages
from AvaliacaoFisica import avaliacao_pages
from flask_login import LoginManager
from inicio import inicio_pages
from Consulta import consulta_pages
import os

app = Flask(__name__)

app.secret_key = os.urandom(12)
app.register_blueprint(consulta_pages, url_prefix='/Consulta')
app.register_blueprint(avaliacao_pages, url_prefix='/AvaliacaoFisica')
app.register_blueprint(inicio_pages, url_prefix='/Inicio')
app.register_blueprint(login_pages, url_prefix='/Login')
app.register_blueprint(alimento_pages, url_prefix='/Alimento')
app.register_blueprint(paciente_pages, url_prefix='/Paciente')
app.register_blueprint(refeicao_pages, url_prefix='/Refeicao')
app.register_blueprint(dieta_pages, url_prefix='/Dieta')

@app.route("/")
def index():
    if session.get('logged_in'):
        return redirect('/Inicio/inicio/')
    else:
        return redirect('/Login/login/')
   







