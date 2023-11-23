import logging
import traceback
import flask
from replit import db

app = flask.Flask(__name__, template_folder='templates')

@app.errorhandler(500)
def internal_server_error(e: str):
    return flask.jsonify(error=str(e)), 500

def get_contatos():
    return db.get('contatos', {})

@app.route('/', methods=['GET', 'POST'])
def cadastroContatos():
    try:
        contatos = get_contatos()
        if flask.request.method == "POST":
            email = flask.request.form['email']
            contatos[email] = {
                'nome': flask.request.form['nome'],
                'telefone': flask.request.form['telefone'],
                'assunto': flask.request.form['assunto'],
                'mensagem': flask.request.form['mensagem'],
                'preferencia_email': 'Email' in flask.request.form.getlist('preferencia'),
                'preferencia_telefone': 'Telefone' in flask.request.form.getlist('preferencia')
            }
            db['contatos'] = contatos
        return flask.render_template('contatos.html', contatos=contatos)
    except Exception as e:
        logging.exception('Falha ao acessar o banco de dados')
        flask.abort(500, description=str(e) + ': ' + traceback.format_exc())

@app.route('/excluirContato', methods=['POST'])
def excluirContato():
    try:
        email = flask.request.form['email']
        contatos = get_contatos()
        if email in contatos:
            del contatos[email]
            db['contatos'] = contatos
        return flask.redirect('/')
    except Exception as e:
        logging.exception('Falha ao excluir contato')
        flask.abort(500, description=str(e) + ': ' + traceback.format_exc())

@app.route('/limparBanco', methods=['POST'])
def limparBanco():
    try:
        del db["contatos"]
        return flask.redirect('/')
    except Exception as e:
        logging.exception(e)
        return flask.render_template('contatos.html')

app.run('0.0.0.0')
