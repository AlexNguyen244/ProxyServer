
# Authors: Alex Nguyen (912141552), Michelle Karnadjaja (917297605)

from timeit import default_timer as timer
from socket import *
import sys

start = timer()
if len(sys.argv) <= 1:
    print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address of the Proxy Server]')
    sys.exit(2)
 
# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
# Fill in start.
server_ip = sys.argv[1]
server_port = 8080
tcpSerSock.bind((server_ip, server_port))
print("socket binded to {}:{}".format(server_ip, server_port))
tcpSerSock.listen(1)
print("socket is listening")

# Client Server
tcpCliServer = socket(AF_INET, SOCK_STREAM)
tcpCliServer.connect((gethostname(), server_port))
# Fill in end.

while 1:
    # Start receiving data from the client
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)
    # Fill in start.
    server_message = bytes("GET http://www.facebook.com HTTP/1.1", "utf-8") #HTTP request
    tcpCliSock.send(server_message)
    message = tcpCliServer.recv(1024).decode("utf-8") # client's message
    # Fill in end.
    print("message:", message)
    # Extract the filename from the given message
    split_message = message.split()[1]
    print("split message:", split_message)
    filename = message.split()[1].partition("//")[2] # HTTP request
    print("filename:", filename)
    fileExist = "false"
    filetouse = "/" + filename
    print("filetouse:", filetouse)
    try:
        # Check whether the file exist in the cache
        f = open(filetouse[1:], "r")
        outputdata = f.readlines()
        fileExist = "true"
        # ProxyServer finds a cache hit and generates a response message
        tcpCliSock.send(bytes("HTTP/1.1 200 OK\r\n\r\n", "utf-8"))
        tcpCliSock.send(bytes("Content-Type:text/html\r\n\r\n", "utf-8"))
        # Fill in start.
        print("File found in cache")
        for i in range(0, len(outputdata)):
            tcpCliSock.send(bytes(outputdata[i], "utf-8"))
        # Fill in end.
        print('Read from cache')
        end = timer()
        print("Time:", end - start)
        tcpCliSock.close()
        break
    #Error handling for file not found in cache
    except IOError:
        if fileExist == "false":
            # Create a socket on the proxyserver
            # Fill in start.
            print("File not found in cache")
            c = socket(AF_INET, SOCK_STREAM)
            # Fill in end.
            hostn = filename.replace("www.","",1)
            print("hostn:", hostn)

            try:
                # Connect to the socket to port 80
                # Fill in start.
                c.connect((hostn, 80))
                print("Connected to", hostn, gethostbyname(hostn))
                # Fill in end.
                # Create a temporary file on this socket and ask port 80 for file requested by the client
                #fileobj = c.makefile('r', 0)
                #fileobj.write("GET   "+"http://"   +   filename   +   " HTTP/1.0\n\n") # This was implemented above instead
                # Read the response into buffer
                # Fill in start.
                c.sendall(server_message)
                buffer = c.recv(20480)
                print(buffer)
                # Fill in end.
                # Create a new file in the cache for the requested file. 
                # Also send the response in the buffer to client socket and the corresponding file in the cache
                tmpFile = open("./" + filename,"wb")
                # Fill in start.
                tmpFile.write(buffer)
                tcpCliSock.sendall(buffer)
                print("Data has been written")
                # Fill in end.
                end = timer()
                print("Time:", end - start)
                tcpCliSock.close()
                break
            except:
                print("Illegal request") 
                end = timer()
                print("Time:", end - start)
                tcpCliSock.close()
                break     
        else:
            # HTTP response message for file not found
            # Fill in start.
            tcpSerSock.send(bytes("HTTP/1.1 404 Not Found\r\n\r\n", "utf-8"))
            tcpCliSock.send(bytes("Content-Type:text/html\r\n\r\n", "utf-8"))
            end = timer()
            print("Time:", end - start)
            break
            # Fill in end.
# Close the client and the server sockets
    # Fill in start.
tcpSerSock.close()
    # Fill in end.