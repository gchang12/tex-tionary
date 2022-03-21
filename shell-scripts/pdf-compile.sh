cd impatient
for i in ./*.tex; do (file=${i:2:-4}; if [[ $file != eplain && $file != config && $file != fonts && $file != macros && $file != backm && $file != fdl && $file != book ]]; then pdftex --interaction=scrollmode $i; fi); done
rm *.aux *.idx *.log
if [ ! -e output ]; then mkdir output; fi
mv *.pdf output
mv ./output/ ../pdf-output/
