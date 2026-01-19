echo ">>> Run Directory: $1"
echo ">>> Number of CPUs: $2"

if [ -z "$2" ]
then
    echo "ERROR: Expected Two Parameters"
    echo "Example: ./data_preprocess.sh molport/ 4"
else
    echo ""
    echo ">>> get_library.py start (get minimum size fragments)"
    python preprocessing/get_library.py $1 --cpus $2
    echo ">>> get_library.py finish"
fi
