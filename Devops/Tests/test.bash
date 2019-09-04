#switch controls
while getopts ":w :p :m" o; do
    case "${o}" in
        m) 
			bash provtest/testprov.bash
            bash weighttest/testweight.bash
			;;
        p)
            bash provtest/testprov.bash
            ;;
        w)
            
            bash weighttest/testweight.bash
            ;;
        *)
            echo invalid switch
    esac
done