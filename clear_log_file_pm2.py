import os

print('INFO: -------------------CLEANING NGINX LOGS-------------------')
os.system('pm2 flush')
print('INFO: -------------------CLEANING NGINX LOGS DONE!.-------------------')



*/3 * * * * python3 /home/ec2-user/Desktop/golomt/golomtbank-statement-records/golomt_v2.py
