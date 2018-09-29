#!usr/bin/python3
from subprocess import getoutput

import fileinput
import re

def main():
    'Obtenção de elementos'
    out = getoutput("cat pw.txt | awk -F \"[ \t]+\" '{print $2}'")
    elements = out.split("\n")

    'Obtenção das palavras - ficheiros parâmetro'
    #words = []
    #for word in fileinput.input():
    #    words.append(word.strip())
    print(find_prefix(0,"Boro",elements))

    print(split_word("BONO", elements))

def split_word(word, elements):
	w_it = 0
	word_size = len(word)
	ws = []
	ws_it = 0
	ws_size = 0
	while(w_it < word_size):
		o = find_prefix(0, word, elements)
		if o >= 118 and ws_it > 0:
			back = 1
			while ws_it > 0 and back == 1:
			    w_it -= len(elements[ws[ws_it]])
			    ws_it -= 1 
			    o = find_prefix(ws[ws_it] + 1, word, elements)
			    if o != 118:
			    	ws[ws_it] = o
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
			w_it += len(elements[o])
			ws_it += 1
	return (ws, ws_it)




			


def find_prefix(i, word, elements):
	size = len(elements)
	found = 0
	while i < size and not found :
		if re.match(elements[i], word): 
			#print(elements[i])
			found = 1
		else: i+=1
	return i



if __name__ == "__main__":
    main()
