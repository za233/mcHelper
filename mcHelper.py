import socket
from threading import Thread
import optparse
import binascii
import time
global last
global bufs
last=""
bufs=""
def hexdump(src,length=16):
	result=[]
	digits=4 if isinstance(src,unicode) else 2
	for i in xrange(0,len(src),length):
		s=src[i:i+length]
		hexa=b' '.join(["%0*X"%(digits,ord(x)) for x in s])
		text=b' '.join([x if 0x20<=ord(x)<0x7F else b'.' for x in s])
		result.append(b"%04X  %-*s  %s" % (i,length*(digits+1),hexa,text))
	print b'\n'.join(result)
def sendkill(to,buf):
	a=0
	while a<=100:
		time.sleep(0.2)
		a=a+1
		to.send(buf)
def PacketID(buf):
	return ord(buf[0])
def transport (froms,to,handle=1):
	global bufs
	global last
	conf=0
	while True:
		try:
			buf=froms.recv(4096)
			to.send(buf)
			if handle==1 and len(buf)>0:
				if len(buf)>=5 and ord(buf[3])==47 and ord(buf[4])==111:
					print ("GET REQUEST!")
					if conf==0:
						print ("Process OPEN!")
						conf=1
					elif conf==1:
						print ("Process CLOSE!")
						conf=0
				if PacketID(buf)==6:
					if conf==1:
						print ("GOT!")
						hexdump(buf)
						th=Thread(target=sendkill,args=(to,buf))
						th.start()
					continue
		except Exception,e:
			print e
			break
			pass
def main ():
    parser=optparse.OptionParser("transport -t <target host ip> -p <target port> -b <local port to bind>")
    parser.add_option("-t",dest="targets",type="string",help="Target Host IP")
    parser.add_option("-p",dest="tport",type="string",help="Target Port")
    parser.add_option("-b",dest="lport",type="string",help="Local Port To Bind")
    (options,args)=parser.parse_args()
    if options.targets==None or options.tport==None or options.lport==None:
        print ("Bad Args!")
        exit(0)
    targets=options.targets
    tport=int(options.tport)
    lport=int(options.lport)
    sock=socket.socket()
    try:
        sock.bind(("127.0.0.1",lport))
        sock.listen(10)
    except:
        print ("Error!")
        pass
    while True:
        (ac,addr)=sock.accept()
        print ("get a connect!")
        try:
            links=socket.socket()
            links.connect((targets,tport))
        except:
            print ("connect error!")
            continue
        th1=Thread(target=transport,args=(ac,links,1))
        th2=Thread(target=transport,args=(links,ac,0))
        th1.start()
        th2.start()
if __name__=="__main__":
    main()
            
            
            
            
            
            
            
            
            
            
