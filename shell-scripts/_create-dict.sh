cd $1
for i in ./*.tex; do (file=${i:2:-4}; if [[ $file != book && $file != eplain && $file != config && $file != fonts && $file != macros ]]; then etex $i; fi); done
rm *.aux *.idx *.log
for i in {eplain,config,fonts,macros}; do rm $i.tex; done
output_dir=../../dvi-output/${1:2:-1}
if [ ! -e $output_dir ]; then mkdir $output_dir; fi
mv *.dvi $output_dir
