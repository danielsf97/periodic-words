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

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def split_word(word, elements):
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
	size = len(elements)
	found = 0
	while i < size and not found :
		if re.match(elements[i], word, re.IGNORECASE): 
			found = 1
		else: i+=1
	return i

def gen_word(result):
    temp = []
    for el in result:
        filename = str(el+1) + '.png'
        temp.append(url_for('uploaded_file', filename =
            filename))

    return temp


@app.route('/result')
def result():
    lines = []
    elements = elems()
    with open('uploads/palavras.txt') as f:
        content = f.readlines()

    content = [x.strip() for x in content]

    for line in content:
        (ws, ws_count) = split_word(line, elements)
        lines.append(gen_word(ws))

    #return "\n".join(lines)
    return render_template("result.html", lines = lines)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files and 'word' not in request.form:
            flash('No file part')
            return redirect(request.url)
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'palavras.txt'))
                return redirect('/result')
        if 'word' in request.form:
            word = request.form['word']
            if word:
                with open('uploads/palavras.txt', 'w') as f:
                    f.write(word)
                return redirect('/result')
    return render_template("index.html")

def elems():
    'Obtenção de elementos'
    out = getoutput("cat pw.txt | awk -F \"[ \t]+\" '{print $2}'")
    elements = out.split("\n")

    return elements

if __name__ == "__main__":
    app.run(debug=True)
