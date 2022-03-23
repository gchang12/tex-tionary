if [ -n "$1" ]; then 
    ls ./dvi-output/*/* | egrep /.+/.*"$1"
fi;
