import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from leituras import casos, mortes, hospitalizados, entubados, dez_bairros, casos_por_mes, obitos_fe


mpl.rc('font', family='sans-serif')


def grafico_geral():
    labels = ['Casos', 'Óbitos', 'Hospitalizações', 'Entubação']
    anterior = [casos[0], mortes[0], hospitalizados[0], entubados[0]]
    atual = [casos[1], mortes[1], hospitalizados[1], entubados[1]]

    x = np.arange(len(labels))  # the label locations
    width = 0.3  # the width of the bars

    fig, ax = plt.subplots(figsize=(6, 4))
    rects1 = ax.bar(x - width / 2, anterior, width, color='darkgray')
    rects2 = ax.bar(x + width / 2, atual, width, color='red')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_xticks(x, labels)
    plt.yticks([])
    ax.legend([])
    ax.get_legend().remove()

    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)

    fig.tight_layout()

    # Eliminar todas as bordas
    plt.box(False)
    plt.savefig('static/images/geral.png', bbox_inches='tight')

    return plt.savefig('static/images/geral.png', bbox_inches='tight')


def bairros():
    plt.subplots(figsize=(8, 4))
    desc = plt.barh(list(dez_bairros.keys()), list(dez_bairros.values()),
                    color=('#b10000', '#d80000', '#ff0000', '#ff2727', '#ff3b3b'))
    plt.bar_label(desc, padding=2)
    plt.box()
    plt.xticks([])
    plt.savefig('static/images/bairros.png', bbox_inches='tight')
    return plt.savefig('static/images/bairros.png', bbox_inches='tight')


def casos_p_mes():
    names = list(casos_por_mes.keys())
    values = list(casos_por_mes.values())

    fig, axs = plt.subplots(figsize=(9, 3))
    axs.plot(names, values, color='red', linewidth=3)
    plt.box(False)
    plt.savefig('static/images/registos_mes.png', bbox_inches='tight')
    return plt.savefig('static/images/registos_mes.png', bbox_inches='tight')


def obitos_idades():
    labels = list(obitos_fe.keys())[:6]
    sizes = list(obitos_fe.values())[:6]

    fig1, ax1 = plt.subplots(figsize=(6, 5))
    ax1.pie(sizes, labels=labels, startangle=0, labeldistance = 1.1,
            explode=[0, 0, 0, 0.05, 0.07, .3], wedgeprops = {"ec": "k"},
            colors=['#3b3b3b', '#4f4f4f', '#6c6c6c', '#a7a7a7', '#cecece', 'white'])
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.savefig('static/images/idades_obitos.png', bbox_inches='tight')
    return plt.savefig('static/images/idades_obitos.png', bbox_inches='tight')


