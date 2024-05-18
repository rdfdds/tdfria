from flask import Flask, request, render_template
import requests, urllib
from deep_translator import GoogleTranslator

app = Flask(__name__, template_folder="templates")

id_app = "WJK6X2-LR478JVXPL"
host = "api.wolframalpha.com"
con_id = ""
s = ""

qr = []

@app.route("/")
def home():
    return render_template("home.html", data=qr)

@app.route("/", methods=["POST"])
def activerSiri():
    global con_id, host, s

    qrtemp = []

    # Obtenir la question du champ "input"
    question = request.form["question"]
    qrtemp.append(question)

    # Traduire la question en anglais
    question = GoogleTranslator(source="fr", target="en").translate(question)

    # Envoyer la demande a wolfram alpha
    if con_id:
        query = f"http://{host}/v1/conversation.jsp?appid={id_app}&conversationid={con_id}&i={urllib.parse.quote_plus(question)}"
    else:
        query = f"http://{host}/v1/conversation.jsp?appid={id_app}&i={urllib.parse.quote_plus(question)}"
    if s:
        query += f"&s={s}"
        s = ""
    reponse = requests.get(query).json()

    # Verifiez si wolfram alpha a donne une erreur
    if reponse.get('error', 0):
        qrtemp.append("Erreur")
        qr.append(qrtemp)
        return home()


    con_id = reponse["conversationID"]
    host = reponse["host"] + "/api"
    s = reponse.get("s", "")
    
    # Traduire la reponse en francais
    reponse = GoogleTranslator(source="en", target="fr").translate(reponse["result"])
    qrtemp.append(reponse)
    qr.append(qrtemp)

    return home()

if __name__ == "__main__":
    app.run()