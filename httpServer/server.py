# importacao das bibliotecas
import socket
import os
# definicao do host e da porta do servidor
HOST = '' # ip do servidor (em branco)
PORT = 8080 # porta do servidor

okReq = "HTTP/1.1 200 OK"

badReq = "HTTP/1.1 400 Bad Request\r\n\r\n"

notFound = "HTTP/1.1 404 Not Found\r\n\r\n"

# cria o socket com IPv4 (AF_INET) usando TCP (SOCK_STREAM)
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# permite que seja possivel reusar o endereco e porta do servidor caso seja encerrado incorretamente
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# vincula o socket com a porta (faz o "bind" do IP do servidor com a porta)
listen_socket.bind((HOST, PORT))

# "escuta" pedidos na porta do socket do servidor
listen_socket.listen(1)

# imprime que o servidor esta pronto para receber conexoes
print ('Serving HTTP on port %s ...' % PORT)

message = " "

http_response = " "

filename = ""

while True:
    # aguarda por novas conexoes
    client_connection, client_address = listen_socket.accept()
    # o metodo .recv recebe os dados enviados por um cliente atraves do socket
    request = client_connection.recv(1024)
    # imprime na tela o que o cliente enviou ao servidor
    # print (request.decode('utf-8'))
    if len(request.decode('utf-8').split()) <= 3:
      requestArray = request.decode('utf-8').split()
    else:
      requestArray = request.decode('utf-8').split(' HTTP')[0].split('/')

  
    method = requestArray[0]    
    
  
    if method.strip() != 'GET':
      file = open('badRequest.html','rb') 
      http_response = file.read()
      file.close()
      message = "HTTP/1.1 400 Bad Request\r\n\r\n"

    elif requestArray[1] == '' or requestArray[1].strip() == 'HTTP/1.1' or requestArray[1].strip() == '/':
      file = open('index.html','rb') 
      http_response = file.read()
      file.close()
      message = "HTTP/1.1 200 OK\r\n\r\n"

    else:
      requestArray = requestArray[1:]

      for i in requestArray:
        if i.strip() != 'GET' and i.strip() != 'HTTP/1.1':
          filename += i+'/'

      filename = filename[:-1]  
      print(filename)
      try:
        file = open(filename,'rb') 
      
      except:
        file = open('notFound.html','rb') 
        http_response = file.read()
        file.close()
        message = "HTTP/1.1 404 Not Found\r\n\r\n"

      else:
        http_response = file.read()
        file.close()
        message = "HTTP/1.1 200 OK\r\n\r\n"

    client_connection.send(message.encode('utf-8'))
    # servidor retorna o que foi solicitado pelo cliente (neste caso a resposta e generica)
    client_connection.send(http_response)
      # encerra a conexao
    client_connection.close()

# encerra o socket do servidor
listen_socket.close()