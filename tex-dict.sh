cd ./dvi-output/
if [ -n "$1" ]; then 
    ls ./*/* | grep -P "$1(?=(\w|-|_)*\.dvi)";
fi;
