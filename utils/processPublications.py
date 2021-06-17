import sys
import os
import re
from pathlib import Path
from unidecode import unidecode

p_type = 2

def main():
    filepath = sys.argv[1]
    if not os.path.isfile(filepath):
        print("File path {} does not exist. Exiting...").format(filepath)
        sys.exit()

    
    with open(filepath) as fp:
        for line in fp:
            m = re.search('^(.+)\(([0-9]+)\).? \[(.+).?\]\(\<(.+)\>\).? \*(.+)\*.?', line)

            if m is not None:
                authors = m.group(1).split("; ")
                authors = list(map(str.strip, authors)) # remove trailing spaces
                print(authors)
                year = m.group(2)
                print(year)
                title = m.group(3)
                print(title)
                link = m.group(4)
                print(link)
                journal = m.group(5)
                print(journal)
                print("")

                generateMD(authors, year, title, link, journal, sys.argv[2])


def generateMD(authors, year, title, link, journal, dest_path):
    #Create_markdown
    c = '---\n'
    c+= 'title: "'+title+'"\n'
    c+= 'authors:\n'
    for auth in authors:
        c+='- '+auth+'\n'
    c+='date: "'+year+'-01-01T00:00:00Z"\n' #Fecha de publicación?
    c+='doi: ""\n'
    c+='publishDate: "'+year+'-01-01T00:00:00Z"\n'
    c+='publication_types: ["'+str(p_type)+'"]\n'
    #journal
    c+='publication: "In *'+journal+'*"\n'
    c+='tags:\n- Source Themes\nfeatured: false\n'
    #Link
    c+='links:\n- name: Link\n  url: '+link +'\n'
    c+='---'
    #se escribe content en el archivo
    filename=year+re.sub('[^a-zA-Z]+','',unidecode(authors[0])+journal)+'.md'
    #md_file = open(os.path.join(dest_path, filename), "w")
    #md_file.write(c)
    #md_file.close()
    with open(os.path.join(dest_path, filename), 'x') as temp_file:
        temp_file.write(c)
    #resetear la variable para el próximo fichero
    c=''

if __name__ == '__main__':
    main()