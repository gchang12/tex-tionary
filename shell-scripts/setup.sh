cd ..
if [ ! -d "impatient" ]; then (unzip impatient.zip); fi
if [ ! -d "input-files" ]; then (python3 macro_finder.py); fi
cp edits/loop.tex input-files/genops/loop.tex
cp edits/acute-b-bar.tex input-files/math/acute-b-bar.tex
if [ ! -d "essentials" ]; then (mkdir essentials); fi
cp impatient/{eplain,fonts,config}.tex essentials/
cp edits/macros.tex essentials/
cd shell-scripts

# Unmute to compile .dvi
#chmod 700 dvi-compile.sh _create-dict.sh; cd ..; ./shell-scripts/dvi-compile.sh

# Unmute to compile .pdf
#chmod 700 pdf-compile.sh; cd ..; ./shell-scripts/pdf-compile.sh
