#!/usr/bin/env python
# uploads all files to device except scripts folder
import sys
import getopt
import os
import webrepl_cli

def main(argv):
   global destip
   destip = ''
   global passwd
   passwd = ''
   host = ''
   try:
      opts, args = getopt.getopt(argv,"hd:p:",["dest=","passwd="])
   except getopt.GetoptError:
      print ('upload.py -d <192.168.4.1> -p <password>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print ('upload.py -d <192.168.4.1> -p <password>')
         sys.exit()
      elif opt in ("-d", "--dest"):
         destip = arg
      elif opt in ("-p", "--passwd"):
         passwd = arg
   print ('destination is "', destip)
   print ('password is "', passwd)
if __name__ == "__main__":
	main(sys.argv[1:])
	
port = 8266
os.chdir("../")
directory = os.getcwd()
s = webrepl_cli.socket.socket()
print (destip)
ai = webrepl_cli.socket.getaddrinfo(destip, port)
addr = ai[0][4]
s.connect(addr)
#s = s.makefile("rwb")
webrepl_cli.websocket_helper.client_handshake(s)
ws = webrepl_cli.websocket(s)
ws.write(passwd.encode("utf-8") + b"\r")
ws.ioctl(9, 2)
for filename in os.listdir(directory):
    if filename.endswith(".asm") or filename.endswith(".py") or filename.startswith("_") : 
        print(os.path.join(directory, filename))
        webrepl_cli.put_file(ws, filename, filename)
        continue
    else:
        continue
s.close()
