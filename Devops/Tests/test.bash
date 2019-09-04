SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P)"

#create logs folder.
mkdir "$SCRIPTPATH"/weighttest/endtoend/logs
mkdir "$SCRIPTPATH"/provtest/endtoend/logs
#switch controls
while getopts ":w :p :m" o; do
    case "${o}" in
        m) 
            
			bash "$SCRIPTPATH"/provtest/testprovmaster.bash
            bash "$SCRIPTPATH"/weighttest/testweightmaster.bash
			;;
        p)
            bash "$SCRIPTPATH"/provtest/testprov.bash
            ;;
        w)
            
            bash "$SCRIPTPATH"/weighttest/testweight.bash
            ;;
        *)
            echo invalid switch
    esac
done