# Webhook
Docker Hub Webhook for automation.


# usage:
## 1. generate secret token using openssl
openssl rand -hex 10                              
0e051c7f820b604df180
## 2. setup env 
secret, token, cmd, chat_id = os.getenv("secret"), os.getenv("token"), os.getenv("cmd"), os.getenv("chat_id")
## 3. setup webhook
http://ip/?secret=0e051c7f820b604df180
## 4. run
usermod -aG docker nobody
pip install tornado
python server.py

# one key install
sh -c "$(wget -O- https://raw.githubusercontent.com/tgbot-collection/Webhook/master/install.sh)"