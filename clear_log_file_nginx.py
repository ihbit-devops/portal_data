import os

print('INFO: -------------------CLEANING NGINX LOGS-------------------')
os.system('sudo rm -f /var/log/nginx/*')
os.system('sudo nginx -s reload')
print('INFO: -------------------CLEANING NGINX LOGS DONE!.-------------------')
