import os
from flask import Flask, flash, send_from_directory, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from subprocess import getoutput
import fileinput
import re

UPLOAD_FOLDER = os.getcwd() + '/uploads'
ALLOWED_EXTENSIONS = set(['txt'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "secret"


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Efetua upload de um dado ficheiro"""
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

def allowed_file(filename):
    """Verifica se um ficheiro preenche os requisitos necessários"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def split_word(word, elements):
	"""Devolve os se possível os simbolos quimicos que formam uma dada palavra"""
	w_it = 0
	word_size = len(word)
	ws = []
	ws_it = 0
	ws_size = 0
	while(w_it < word_size):
		o = find_prefix(0, word[w_it:], elements)
		if o >= 118 and ws_it > 0:
			back = 1
			while ws_it > 0 and back == 1:
			    ws_it -= 1
			    w_it -= len(elements[ws[ws_it]]) 
			    o = find_prefix(ws[ws_it] + 1, word[w_it:], elements)
			    ws.pop()
			    if o != 118:
			    	ws.append(o)
			    	w_it += len(elements[o])
			    	ws_it += 1
			    	back = 0
			if (ws_it <= 0):
				ws = []
				break
		elif o >= 118 and ws_it <= 0:
			ws = []
			break
		else:
			ws.append(o)
			w_it += len(elements[o])
			ws_it += 1
	return (ws, ws_it)

def find_prefix(i, word, elements):
	"""Encontra um possível símbolo químico como prefixo da palavra pretendida """
	size = len(elements)
	found = 0
	while i < size and not found :
		if re.match(elements[i], word, re.IGNORECASE): 
			found = 1
		else: i+=1
	return i

def gen_word(result, elements):
    """Para uma dada palavra, obtém as imagens dos respetivos simbolos quimicos"""
    temp = []
    for el in result:
        filename = str(el+1) + '.png'
        temp.append((url_for('uploaded_file', filename =
            filename),elements[el]))

    return temp


@app.route('/result')
def result():
    """Gera a página com o resultado"""
    lines = []

    (siglas, elements) = elems()
    
    with open('uploads/palavras.txt') as fl:
        fc = fl.readlines()

    fc = [l.strip() for l in fc]

    for word in fc:
        (ws, ws_count) = split_word(word, siglas)
        lines.append((word, gen_word(ws, elements)))
        

    return render_template("result.html", lines = lines)


@app.route('/', methods=['GET', 'POST'])
def index():
    """Gera a página inicial, onde se pode fornecer um ficheiro, ou uma única palavra"""    
    if request.method == 'POST':
        if 'fileButton' in request.form:
            if 'file' not in request.files:
                flash('No selected file!')
                return redirect(url_for('index'))
            elif not allowed_file(request.files['file'].filename):
                flash('Invalid file! Allowed file types: .txt')
                return redirect(url_for('index'))
            else:
                file = request.files['file']
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'palavras.txt'))
                return redirect('/result')
        elif 'wordButton' in request.form:
            if 'word' in request.form and request.form['word'] != "":
                word = request.form['word']
                with open('uploads/palavras.txt', 'w') as f:
                    f.write(word)
                return redirect('/result')
            else:
                flash('No word was provided!')
                return redirect(url_for('index'))

    return render_template("index.html")

def elems():
    """Obtenção de elementos"""
    out = getoutput("cat uploads/pw.txt | awk -F \"[ \t]+\" '{print $2}'")
    siglas = out.split("\n")
    out = getoutput("cat uploads/pw.txt | awk -F \"[ \t]+\" '{print $3}'")
    elements = out.split("\n")

    return (siglas, elements)

if __name__ == "__main__":
    app.run(debug = True)
