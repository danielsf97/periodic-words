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

    (ws, ws_count) = split_word("accessibilities", elements)
    #if ws != []:
    #	i = 0
    #	while i < ws_count:
    #		ws[i] = elements[ws[i]]
    print(ws)
    print_word(ws, elements)

def print_word(result, elements):
    for el in result:
        print(elements[el], end='')
    
    print()

def split_word(word, elements):
	w_it = 0
	word_size = len(word)
	ws = []
	ws_it = 0
	ws_size = 0
	while(w_it < word_size):
		o = find_prefix(0, word[w_it:], elements)
		print("%%%%%")
		print(w_it)
		#print(elements[o])
		if o >= 118 and ws_it > 0:
			print(1)
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
			print(2)
			ws = []
			break
		else:
			print(3)
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

if __name__ == "__main__":
    omain()
