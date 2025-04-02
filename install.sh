#!/bin/bash

 echo -e "\e[31m
       _  _           ____      _ 
      | || |         |___ \    | |
   ___| || |_ ___ _ __ __) | __| |
  / __|__   _/ __| '__|__ < / _\` |
  \__ \  | || (__| |  ___) | (_| |
  |___/  |_| \___|_| |____/ \__,_|
                                  
	

\e[0m"  

echo "installation..."
pip install -r requirements.txt
mkdir modules
echo "enter your api_id"
read api_id
echo "enter your hash_id"
read hash_id
cat > config.ini <<EOF

[userbot]
API_ID=$api_id 
API_HASH=$hash_id

EOF

echo  -e "\e[31mдля запуска используйте python3 s4cr3d.py\e[0m"


