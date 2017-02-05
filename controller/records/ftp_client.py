import ftplib
import os, sys 

#--------------------------------------------------------
#sudo python ftp_client xxx.xml 192.168.1.134 2121
username = "user"
password = "12345"
#filename = sys.argv[1]
#server = sys.argv[2]
#port = sys.argv[3]
#-------------------
ftp = ftplib.FTP()
#-------------------------------------------------------- 
def upload(ftp, filepath, remote_dir):
    ext = os.path.splitext(filepath)[1]
    if remote_dir == True:
          ftp.cwd("/cheikh")
    if ext in (".txt", ".xml", ".html"):
        ftp.storlines("STOR " +os.path.basename(filepath), open(filepath))
    else:
        ftp.storbinary("STOR "+os.path.basename(filepath), open(filepath, "rb"), 1024)
 
def connectToFTPServer(serv_addr, port, user, psswd):
	ftp.connect(serv_addr, port) 
	ftp.login(user, psswd)
	return ftp

#----------------TESTS------------------------------------------ 
'''ftp.connect(server, port)
ftp.login(username, password)
upload(ftp, filename, False)'''
