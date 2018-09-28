from subprocess import getoutput

import fileinput

def main():
    'Obtenção de elementos'
    out = getoutput("cat pw.txt | awk -F \"[ \t]+\" '{print $2}'")
    elements = out.split("\n")

    'Obtenção das palavras - ficheiros parâmetro'
    words = []
    for word in fileinput.input():
        words.append(word.strip())

if __name__ == "__main__":
    main()
