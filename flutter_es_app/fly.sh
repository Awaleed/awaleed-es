#!/bin/bash

cat << "EOF"

                         | |                              | |        
          __      __ ___ | |  ___  ___   _ __ ___    ___  | |_  ___  
          \ \ /\ / // _ \| | / __|/ _ \ | '_ ` _ \  / _ \ | __|/ _ \ 
           \ V  V /|  __/| || (__| (_) || | | | | ||  __/ | |_| (_) |
            \_/\_/  \___||_| \___|\___/ |_| |_| |_| \___|  \__|\___/ 
                                                                     
                                                                     
    ____   _       ___                             _             _  _      _ 
   |___ \ | |     / _ \                           | |           (_)| |    | |
     __) || |__  | (_) | _ __  ___  _ __    ___   | |__   _   _  _ | |  __| |
    |__ < | '_ \  > _ < | '__|/ _ \| '_ \  / _ \  | '_ \ | | | || || | / _` |
    ___) || |_) || (_) || |  |  __/| | | || (_) | | |_) || |_| || || || (_| |
   |____/ |_.__/  \___/ |_|   \___||_| |_| \___/  |_.__/  \__,_||_||_| \__,_|
                                                                             
                                                                             
                             _       _               _               
                            | |     | |             | |              
            __ _  _ __    __| |   __| |  ___  _ __  | |  ___   _   _ 
           / _` || '_ \  / _` |  / _` | / _ \| '_ \ | | / _ \ | | | |
          | (_| || | | || (_| | | (_| ||  __/| |_) || || (_) || |_| |
           \__,_||_| |_| \__,_|  \__,_| \___|| .__/ |_| \___/  \__, |
                                             | |                __/ |
                                             |_|               |___/ 

EOF
echo 'Doing a Magic (Abra Kdabra)'
sleep 8
echo 'Building'
flutter build web --web-renderer html --release && echo 'Deploying' && firebase deploy