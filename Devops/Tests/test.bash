#switch controls
while getopts ":w :p :m" o; do
    case "${o}" in
        m) 
			bash /home/kobi/Desktop/W3/gan_shmuel/gan_shmuel_green/Devops/Tests/provtest/testprov.bash
            bash /home/kobi/Desktop/W3/gan_shmuel/gan_shmuel_green/Devops/Tests/weighttest/testweight.bash
			;;
        p)
            bash /home/kobi/Desktop/W3/gan_shmuel/gan_shmuel_green/Devops/Tests/provtest/testprov.bash
            ;;
        w)
            
            bash /home/kobi/Desktop/W3/gan_shmuel/gan_shmuel_green/Devops/Tests/weighttest/testweight.bash
            ;;
        *)
            echo invalid switch
    esac
done