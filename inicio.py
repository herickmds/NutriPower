from jinja2 import TemplateNotFound
from flask import Flask, render_template, request, url_for, redirect, Blueprint, abort, session
import json
from playhouse.shortcuts import model_to_dict
import os
from werkzeug.utils import secure_filename

inicio_pages = Blueprint('inicio_pages', __name__,
                        template_folder='templates')

app = inicio_pages

@app.route('/inicio/', methods=['GET', 'POST'])
def upload_file():
    lista_img = files_path("C:\NutriPower\static\dist\imagens")
    return render_template("inicio.html" , imagens=lista_img)

def files_path(path):
    lista = []
    for p, _, files in os.walk(os.path.abspath(path)):
        for file in files:
            lista.append(file)
    return lista
