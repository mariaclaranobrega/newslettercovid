from email.mime.image import MIMEImage
from main import df_semana_anterior, df_semana_atual, inicio, atual, obitos_fe2, grafico_geral, bairros, casos_p_mes, \
    obitos_idades, ate_atual, de_atual, de_anterior, ate_anterior, app
from graficos import grafico_geral, bairros, casos_p_mes, obitos_idades
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import schedule
import time


def enviar():
    grafico_geral()
    bairros()
    obitos_idades()
    casos_p_mes()

    estilo = """
        .um {{max-width:37.5rem;margin:auto;display: flex; flex-direction:column; justify-content:center; align-items: center;padding:1rem;margin: auto;border:0.125rem solid grey;border-radius:0.625rem;box-shadow: 0.313rem 0.313rem #DCDCDC}}
        .dois {{max-width:7rem;}}
        .tres {{font-size: 1.5rem;font-family: 'Oswald', sans-serif;}}
        .quatro {{max-width:100%;}}
        .cinco {{font-size: 0.8rem;display:flex;flex-direction:row;justify-content:space-around}}
        .seis {{display:flex;flex-direction:row;align-items:center}}
        .sete {{width: 3rem; height: 1.5rem;background-color:darkgray}}
        .oito {{padding-left:0.5rem;font-family: 'Cormorant SC', serif}}
        .nove {{display:flex;flex-direction:row;align-items:center}}
        .dez {{width: 3rem; height: 1.5rem;background-color:red}}
        .onze {{padding-left:0.5rem;font-family: 'Cormorant SC', serif;}}
        .doze {{font-family: 'Inter', sans-serif;text-align: center;font-size:0.9rem}}
        .treze {{padding-top: 1rem}}
        .catorze {{font-size: 1.3rem;text-align: center;font-family: 'Oswald', sans-serif;}}
        .quinze {{font-family: 'Inter', sans-serif;text-align: center;font-size:0.9rem}}
        .dezesseis {{display:flex;flex-direction:row;justify-content:center; align-items:center;padding-top: 2rem}}
        .dezessete {{font-size: 1.5rem;text-align: center;font-family: 'Oswald', sans-serif;}}
        .dezoito {{font-size: 0.8rem;font-family: 'Inter', sans-serif;text-align: center}}
        .dezenove {{max-width:50%;}}
        .vinte {{padding-top: 2rem; padding-bottom:2rem}}
        .vinteum {{font-family: 'Inter', sans-serif;text-align: center;font-size: 0.8rem}}
        .vintedois {{font-family: 'Inter', sans-serif;text-align: center;font-size: 0.5rem;color:grey}}
        """

    message_html = f'''
    <!doctype html>
    <html lang="pt-PT">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport"
              content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
        <link href="https://fonts.googleapis.com/css2?family=Beau+Rivage&family=Oswald&display=swap" rel="stylesheet">
        <link href="https://fonts.googleapis.com/css2?family=Cormorant+SC:wght@700&display=swap" rel="stylesheet">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300&display=swap" rel="stylesheet">
        <style type="text/css"> {estilo} </style>
        <title>COVID-19</title>
    </head>
    <body>
    
    
    <div class="um">
    
        <img class="dois" src="cid:image1" alt="Logo-Covid">
    
        <div>
            <p class="tres">RESUMO DE INFORMAÇÕES</p>
        </div>
    
        <div>
            <img class="quatro" src="cid:image2" alt="Informacoes Gerais">
            <div class="cinco">
                <div class="seis">
                    <div class="sete"></div>
                    <p class="oito">Casos em cinza: De {de_anterior} até {ate_anterior}</p>
                </div>
                <div class="nove">
                    <div class="dez"></div>
                    <p class="onze">Casos em vermelho: De {de_atual} até {ate_atual}</p>
                </div>
            </div>
            <p class="doze">Atualizações sobre os números de casos, óbitos, pacientes hospitalizados e entubados na última semana. Nas barras de cor cinza é possível ver o apanhado geral do número de casos, óbitos, hospitalizações e óbitos da semana passada, enquanto que nas barras de cor vermelha pode-se analisar estes mesmos dados durante esta semana.Importante ressaltar que a doença pode ser prevenida por meio da utlização de máscaras, lavagem das mãos e evitando aglomerações.</p>
        </div>
    
        <div class="treze">
            <p class="catorze">BAIRROS COM MAIOR ÍNDICE DE CONTAMINAÇÃO ATIVA</p>
            <img class="quatro" src="cid:image3" alt="Bairros mais contaminados">
            <p class="quinze">No gráfico acima temos o ranking dos bairros que atualmente apresentam os maiores índices de contaminação ativa. Mantenha-se atento às nossas atualizações, e caso seu bairro esteja nesta listagem, reforçarmos a importante de redobrar os cuidados preventivos para diminuir o risco de possíveis contaminações.</p>
        </div>
    
        <div class="dezesseis">
            <div>
                <p class="dezessete">ÓBITOS POR FAIXA ETÁRIA</p>
                <p class="dezoito">Segundo dados coletados entre {inicio} e {atual}, a faixa etária com maior número de casos fatais é de {list(obitos_fe2.keys())[0]}, e a faixa etária com menor número de letalidade é {list(obitos_fe2.keys())[-1]}. Entretanto, todas os cidadãos devem continuar a fazer sua parte para impedir um aumento na circulação do vírus SARS-CoV-2 nos espaços públicos e privados.</p>
            </div>
            <img class="dezenove" src="cid:image4" alt="Idades de maior risco">
        </div>
    
        <div class="vinte">
            <p class="vinteum">Abaixo temos a evolução do COVID-19 entre {inicio} e {atual}, de acordo com os casos reportados neste período. Contamos com a colaboração da população para que a curva de casos seja decrescente.</p>
            <img class="quatro" src="cid:image5" alt="Evolução dos casos">
        </div>
    
        <p class="vintedois">Todos os dados foram reunidos pelo Toronto Public Health (TPH) e estão à domínio público, podendo ser encontrados em https://www.kaggle.com/datasets/divyansh22/toronto-covid19-cases?resource=download.</p>
    
    </div>
    
    </body>
    </html>
    '''

    host = 'smtp.gmail.com'
    port = 587
    user = 'EMAIL_REMETENTE@gmail.com'
    password = 'SUA_SENHA_DE_APP'
    server = smtplib.SMTP(host, port)

    server.ehlo()
    server.starttls()
    server.login(user, password)

    email_msg = MIMEMultipart()
    # Lista de destinatários
    destinatarios = ['email1@gmail.com', 'email2@gmail.com', 'email3@gmail.com']
    email_msg['From'] = user
    # Transformar a lista de destinatários em uma str divididindo os emails por vírgulas.
    email_msg['To'] = str(destinatarios).replace('[','').replace(']','').replace("'",'').replace(" ",'')
    email_msg['Subject'] = 'Newsletter COVID'

    # Logo COVID
    covidlogo = open('static/images/covid_logo_pequena.png', 'rb')
    covid_logoImage = MIMEImage(covidlogo.read())
    covidlogo.close()
    covid_logoImage.add_header('Content-ID', '<image1>')
    email_msg.attach(covid_logoImage)

    # geral
    geral = open('static/images/geral.png', 'rb')
    geralImage = MIMEImage(geral.read())
    geral.close()
    geralImage.add_header('Content-ID', '<image2>')
    email_msg.attach(geralImage)

    # bairros
    bairro = open('static/images/bairros.png', 'rb')
    bairrosImage = MIMEImage(bairro.read())
    bairro.close()
    bairrosImage.add_header('Content-ID', '<image3>')
    email_msg.attach(bairrosImage)

    # obito
    obito = open('static/images/idades_obitos.png', 'rb')
    obitosImage = MIMEImage(obito.read())
    obito.close()
    obitosImage.add_header('Content-ID', '<image4>')
    email_msg.attach(obitosImage)

    # registro mes
    mes = open('static/images/registos_mes.png', 'rb')
    mesImage = MIMEImage(mes.read())
    mes.close()
    mesImage.add_header('Content-ID', '<image5>')
    email_msg.attach(mesImage)
    email_msg.attach(MIMEText(message_html, 'html'))

    # Receberá email_msg['To'] um por um
    multidest = MIMEMultipart()
    loop = 1
    while loop <= len(destinatarios):
        # Abrir e fechar o terminal a cada envio, para driblar o problema com o servidor do SMTP
        server.quit()

        server = smtplib.SMTP(host, port)
        server.ehlo()
        server.starttls()
        server.login(user, password)
        # Iniciar sempre com essa variável limpa
        multidest.__delitem__('To')
        # Se a lista do email_msg['To'] tiver mais de 1 elemento:
        if (email_msg['To'].find(',')) != -1:
            # Salvar na variável transitória o email (até a vírgula)
            multidest['To'] = email_msg['To'][0:(email_msg['To'].find(','))+1]
        # Se não houver vírgula, significa que só há 1 elemento:
        else:
            # Salvar o elemento inteiro
            multidest['To'] = email_msg['To'][0:]
        # Enviar para este elemento
        server.sendmail(email_msg['From'], f"<{multidest['To']}>", email_msg.as_string())
        print("Email enviado para ", multidest['To'])
        # Apagar este email da listagem do email_msg['To']
        att = str(email_msg['To'].split(',')[1:]).replace('[','').replace(']','').replace("'",'').replace(" ",'')
        # Limpar variável
        email_msg.__delitem__('To')
        # Adicionar os emails restantes na lista
        email_msg['To'] = att
        print("Seguintes: ",email_msg['To'],"\n")

        loop += 1
        time.sleep(2)

    server.quit()


if __name__ == '__main__':
    enviar()

