from . import home
from flask import render_template, flash, request, jsonify, make_response
from werkzeug.utils import secure_filename
from app import db
from app import UPLOAD_FOLDER
from app import ALLOWED_EXTENSIONS
from app import API_AZURE
from app import KEY

import requests
import json
import pandas as pd
import numpy as np
import os


@home.route("/", methods=["GET","POST"])
def index():
    return render_template("home.html")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def processarImagem(respostaJSON, url):
    dt = pd.DataFrame(respostaJSON['predictions'])
    dt.drop("tagId", axis=1, inplace=True)
    print()
    
    df_quadro = dt[dt.tagName == "quadro"]["probability"] 
    df_quadro_index = dt[dt.tagName == "quadro"]["probability"].index.item()
    print(dt)

    print(df_quadro_index)
    print("quadro ", df_quadro.item() * 100)
    if((df_quadro.item() * 100) < 50.0):
        retorno = {"Status":False, "Probability": 0 , "Autor": None, 
                    "Image": url,"ShowImage": True, "Message":"Essa imagem não é uma pintura"}
        return jsonify(retorno)
    dt.drop(df_quadro_index, axis=0,inplace=True)
    dt.reset_index(inplace=True)
    print(dt)
    df_return =  dt[dt.probability == dt.probability.max()] 
        
    probabilidade = round(df_return.at[0, "probability"] * 100, 2)
    autor= df_return.at[0, "tagName"]

    if(autor == "quadro" or probabilidade < 80 ):
        retorno = {"Status":False, "Probability": 0 , "Autor": autor,
                    "ShowImage": True, "Image": url, "Message":"É uma bela pintura porém não pertence à nenhum dos 3 pintores"}
        return jsonify(retorno)

    retorno = {"Status":True,"Probability": probabilidade , "Autor": autor, "Image": url, "ShowImage": True, "Message":""}

    return jsonify(retorno)



@home.route("/processarUpload", methods=["POST"])
def processarUpload():        
    APIURL = API_AZURE.format(tipo="image")
    headers = {'Content-Type': 'application/octet-stream', 'Prediction-Key': KEY}

    file = request.files['file']

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        print(os.path.join(UPLOAD_FOLDER, filename))
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        
        url_fisica = os.path.join(UPLOAD_FOLDER, filename)
        url_media = request.url_root + 'static/uploads/{0}'.format(filename)
        file = open(url_fisica, 'rb')

        resp = requests.post(url=APIURL, headers=headers, data=file)

        retornoProcessado = processarImagem(resp.json(), url_media)
        return retornoProcessado

    retorno = {
        "Status": False,
        "Probability": 0 , 
        "Autor": 0, 
        "Image": "", 
        "ShowImage": False,
        "Message":"Não foi possivel processar a imagem enviada"
    }
    return jsonify(retorno)

@home.route("/processarURL", methods=["POST"])
def processarURL():
    #https://i.pinimg.com/originals/a0/a6/cd/a0a6cd8b502b5f4191ef0a14607ac6e0.jpg
    APIURL = API_AZURE.format(tipo="url")
    headers = {'Content-Type': 'application/json', 'Prediction-Key': KEY}
    print(APIURL, headers )
    url = request.form['url']
    data = {'url': url}
    resp = requests.post(url=APIURL, headers=headers, data=json.dumps(data))

    retorno=""
    print(resp.json())
    if resp.status_code == 200:
        retornoProcessado = processarImagem(resp.json(), url)
        return retornoProcessado
    else:
        retorno = { 
            "Status": False,
            "Probability": 0 , 
            "Autor": 0, 
            "Image": url, 
            "ShowImage": False,
            "Message":"Não foi possivel processar pois a URL não é válida "
        }
        return jsonify(retorno)
    
   