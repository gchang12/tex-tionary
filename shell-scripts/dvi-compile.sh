if [ ! -e dvi-output ]; then mkdir dvi-output; fi
for i in ./input-files/*/; do cp essentials/* $i; done
cd input-files/
for i in ./*/; do ../shell-scripts/_create-dict.sh $i; done
