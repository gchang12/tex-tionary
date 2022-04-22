from os import sep, walk, mkdir
from os.path import exists

import re

input_dir='input-files'

def list_tex_files():
    tex_files=set()

    for x,y,filelist in walk('impatient'):
        if x != 'impatient':
            # Don't want any of the files in the other directories
            continue
        for file in filelist:
            if '.tex' in file:
                # General indication that something is a TeX-file
                tex_files.add(file)
    cfg_files='config','eplain','fonts','macros'
    # These files are necessary to typeset each TeX file in this folder
    cfg_files=set(f+'.tex' for f in cfg_files)
    # Naturally, they must be excluded from the list of files to parse:
    return tex_files-cfg_files

def is_cmd_file(filename):
    with open(sep.join(['impatient',filename])) as rfile:
        if '\\begindescriptions\n' in rfile.readlines():
            # Indicator that a TeX file contains command definitions
            return True
    return False

def list_cmd_files():
    tex_files=list_tex_files()
    # Recall this is a set
    while tex_files:
        # Destructive iteration to economize on memory
        file=tex_files.pop()
        if is_cmd_file(file):
            yield file

def list_sections(filename):
    new_entry=list()
    with open(sep.join(['impatient',filename])) as rfile:
        for line in rfile.readlines():
            line=line.strip()
            # If new_entry is empty and the line does not contain the string, then the line lies outside a command definition
            if not new_entry and '\\begindesc' not in line:
                continue
            else:
                # If begindesc is in the line, then append
                # If new_entry is non-empty, then enddescr has not been reached yet; we're still inside the command definition
                new_entry.append(line)
                if '\\enddesc' in line:
                    yield new_entry
                    new_entry.clear()

def list_command_names(filename):
    """ Lists command names for a given file/section. """
    max_filename_len=16
    bad_chars='{','}','\\','.'
    # Found through experimentation
    for section in list_sections(filename):
        name=str()
        for entry in section:
            entry=entry.strip()
            if 'cts' not in entry:
                # Not a control-sequence
                if name:
                    # If cts is gathered, then stop
                    break
                else:
                    # Otherwise, keep accumulating str object
                    continue
            else:
                # General format of entry:
                # cts (cmd) [other stuff]
                entry=entry.split(' ')
                if len(entry) < 2:
                    # It's usually the second str that contains the command name
                    continue
                entry=entry[1]
                entry=re.sub(r'\W','',entry)
                # Stripping all punctuation from the entry...
                if name:
                    # Absorb more strings into name
                    if name in entry:
                        continue
                    elif entry in name:
                        continue
                    # Gotta make sure there are no names with repetitive names
                    else:
                        if len(name+entry)+1 > max_filename_len:
                            break
                        else:
                            name+='-'+entry
                elif not entry:
                    continue
                else:
                    # If entry is non-blank and name is blank:
                    # - in other words, the first instance of name generation
                    name=filename.replace('.tex','')+sep+entry
        yield name

def write_command_entry(filename):
    name_list=list_command_names(filename)
    preamble='\\input macros','','\\begindescriptions',''
    # Necessary to typeset a given command entry
    for name,section in zip(name_list,list_sections(filename)):
        # Command names and their respective entries
        folder=name.split(sep)[0]
        folder=input_dir+sep+folder
        # input-files/(section)/
        if not exists(folder):
            mkdir(folder)
        if not name:
            # To prevent TeX making ./input-files/.tex
            continue
        filename=sep.join([input_dir,name+'.tex'])
        if exists(filename):
            continue
        print(filename)
        # To show what new names are generated on subsequent runs
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
