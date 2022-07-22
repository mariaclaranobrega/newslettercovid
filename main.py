from flask import Flask, render_template, url_for, redirect, request
from graficos import grafico_geral, bairros, casos_p_mes, obitos_idades
from leituras import df_semana_anterior, df_semana_atual, inicio, atual, obitos_fe2
from flask_apscheduler import APScheduler
import threading


app = Flask(__name__)
scheduler = APScheduler()

de_anterior = df_semana_anterior['Reported Date'].min().strftime("%d/%m/%Y")
ate_anterior = df_semana_anterior['Reported Date'].max().strftime("%d/%m/%Y")

de_atual = df_semana_atual['Reported Date'].min().strftime("%d/%m/%Y")
ate_atual = df_semana_atual['Reported Date'].max().strftime("%d/%m/%Y")


@app.route('/')
def index():

    def reloadinfos():
        grafico_geral()
        bairros()
        casos_p_mes()
        obitos_idades()
        threading.Timer(5.0, reloadinfos).start()

    reloadinfos()

    return render_template("index.html", de_anterior=de_anterior, ate_anterior=ate_anterior, de_atual=de_atual,
                           ate_atual=ate_atual, inicio=inicio, atual=atual, obitos_fe2=obitos_fe2)


if __name__ == '__main__':
    app.run(debug=True)









