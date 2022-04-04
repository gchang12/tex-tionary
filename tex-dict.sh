if [ -n "$1" ]; then 
    ls ./dvi-output/*/* | grep -P "$1(?=(\w|-|_)*\.dvi)";
fi;
