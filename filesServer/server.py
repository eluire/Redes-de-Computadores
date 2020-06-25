# importacao das bibliotecas
from socket import * # sockets

# definicao das variaveis
serverName = '' # ip do servidor (em branco)
serverPort = 61000 # porta a se conectar
serverSocket = socket(AF_INET,SOCK_STREAM) # criacao do socket TCP
serverSocket.bind((serverName,serverPort)) # bind do ip do servidor com a porta
serverSocket.listen(1) # socket pronto para 'ouvir' conexoes
print ('Servidor TCP esperando conexoes na porta %d ...' % (serverPort))
while 1:
  connectionSocket, addr = serverSocket.accept() # aceita as conexoes dos clientes
  sentence = connectionSocket.recv(1024) # recebe dados do cliente
  sentence = sentence.decode('utf-8')
  if sentence == 'obter arquivo.txt':
    file = open('./arquivo.txt')
    response = file.read()
    print ('Cliente %s enviou: %s, resposta %s' % (addr, sentence, response))
    connectionSocket.send(response.encode('utf-8')) # envia para o cliente o texto transformado
    connectionSocket.close() # encerra o socket com o cliente
  else:
    response = "Comando inválido"
    print ('Cliente %s enviou: %s, resposta %s' % (addr, sentence, response))
    connectionSocket.send(response.encode('utf-8')) # envia para o cliente o texto transformado
    connectionSocket.close() # encerra o socket com o cliente

serverSocket.close() # encerra o socket do servidor