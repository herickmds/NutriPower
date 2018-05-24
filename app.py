from flask import Flask, render_template, request, url_for, redirect
from NutripowerMysql import Alimento, db, Paciente, Refeicao, Dieta, Alimento_Refeicao, Refeicoes_Dieta
import json
from playhouse.shortcuts import model_to_dict
from alimento import alimento_pages
from paciente import paciente_pages
from refeicao import refeicao_pages
from dieta import dieta_pages


app = Flask(__name__)

app.register_blueprint(alimento_pages, url_prefix='/Alimento')
app.register_blueprint(paciente_pages, url_prefix='/Paciente')
app.register_blueprint(refeicao_pages, url_prefix='/Refeicao')
app.register_blueprint(dieta_pages, url_prefix='/Dieta')

@app.route("/")
def index():
    return render_template('index.html')










