from os import sep, walk, mkdir
from os.path import exists

import re

input_dir='input-files'

def list_tex_files():
    tex_files=set()

    for x,y,filelist in walk('impatient'):
        if x != 'impatient':
            continue
        for file in filelist:
            if '.tex' in file:
                tex_files.add(file)
    cfg_files='config','eplain','fonts','macros'
    cfg_files=set(f+'.tex' for f in cfg_files)
    return tex_files-cfg_files

def is_cmd_file(filename):
    with open(sep.join(['impatient',filename])) as rfile:
        if '\\begindescriptions\n' in rfile.readlines():
            return True
    return False

def list_cmd_files():
    tex_files=list_tex_files()
    while tex_files:
        file=tex_files.pop()
        if is_cmd_file(file):
            yield file

def list_sections(filename):
    new_entry=list()
    with open(sep.join(['impatient',filename])) as rfile:
        for line in rfile.readlines():
            line=line.strip()
            if not new_entry and line != '\\begindesc':
                continue
            else:
                new_entry.append(line)
                if line == '\\enddesc':
                    yield new_entry
                    new_entry.clear()

def list_command_names(filename):
    max_filename_len=16
    bad_chars='{','}','\\','.'
    for section in list_sections(filename):
        name=str()
        for entry in section:
            entry=entry.strip()
            if 'cts' not in entry:
                if name:
                    break
                else:
                    continue
            else:
                if '@' in entry:
                    continue
                entry=entry.split(' ')[1]
                entry=re.sub(r'\W','',entry)
                if name:
                    if name in entry:
                        continue
                    elif entry in name:
                        continue
                    else:
                        if len(name+entry)+1 > max_filename_len:
                            break
                        else:
                            name+='-'+entry
                else:
                    name=filename.replace('.tex','')+sep+entry
 #       for c in bad_chars:
#            name=name.replace(c,'')
        yield name

def write_command_entry(filename):
    name_list=list_command_names(filename)
    preamble='\\input macros','','\\begindescriptions',''
    for name,section in zip(name_list,list_sections(filename)):
        folder=name.split(sep)[0]
        folder=input_dir+sep+folder
        if not exists(folder):
            mkdir(folder)
        if not name:
            continue
        filename=sep.join([input_dir,name+'.tex'])
        with open(filename,'w') as wfile:
            for p in preamble:
                wfile.write(p+'\n')
            for line in section:
                wfile.write(line+'\n')
            wfile.write('\n\\enddescriptions\n\\end')

def write_all():
    if not exists(input_dir):
        mkdir(input_dir)
    for file in list_cmd_files():
        write_command_entry(file)

if __name__ == '__main__':
    write_all()
