# Felipe Vera y Marcelo Ibarra, Seguridad Informática
import socket

################### Manejo TXT ############################################################

# Accede al archivo de texto inicial en modo lectura
entrada = open("mensajedeentrada.txt",'r')

# Toma el contenido del archivo de texto y lo guarda dentro de la variable mensaje
mensaje = ""
for texto in entrada:
    mensaje = mensaje+texto

###########################Funciones#####################################################

# Reemplaza los caracteres de un mensaje por numeros para almacenarlos dentro de una lista
def change(mensaje):
    alfabeto='abcdefghijklmnñopqrstuvwxyz'
    resp= []
    
    for letra in mensaje:
        for let in range(len(alfabeto)):
            if letra == alfabeto[let]:
                resp.append(let)
    return resp
            

                
    
############# Configuración del servidor ###########################################################################

# Configuración del servidor
host = '127.0.0.1'
port = 12345

# Crear un socket del servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Vincular el socket al host y puerto especificados
server_socket.bind((host, port))

# Escuchar conexiones entrantes (máximo 1 en este caso)
server_socket.listen(1)

print(f"El servidor está esperando conexiones en {host}:{port}...")

# Aceptar la conexión entrante
client_socket, client_address = server_socket.accept()
print(f"Conexión establecida con {client_address}")


# En response va lo que se le quiere enviar al cliente
response = "¿Con qué acción te gustaría trabajar?:\n1.- Encriptado RSA\n2.- Encriptado GAMAL"
# Esta es la linea de codigo que envía los mensaje, dentro del ciclo tambien está definida
client_socket.send(response.encode())
##################################################################################################################

############## Este es el ciclo infinito donde se pueden implementar todas las cosas del lab ###########

while True:
    
    # Recibir mensaje del cliente, llegan en formato de string
    message = client_socket.recv(1024).decode()
    


    if message == "1":

        # Aca el servidor recibe los parametros necesarios para cifrar el mensaje de entrada mediante RSA
        client_socket.send('oki'.encode())
        n=  int(client_socket.recv(1024).decode())
        client_socket.send('oki'.encode())
        e= int(client_socket.recv(1024).decode())

        # Se cifra el mensaje letra por letra
        mensaje_encriptado= []
        mensaje_num= change(mensaje)
        print(mensaje_num)
        for i in mensaje_num:
            mensaje_encriptado.append((i**e)%n)

        # Se Imprime el mensaje cifrado en pantallla
        print(mensaje_encriptado)

        # Envio del largo del mensaje cifrado junto con cada letra cifrada
        client_socket.send(str(len(mensaje_encriptado)).encode())
        client_socket.recv(1024).decode()
        for i in mensaje_encriptado:
            client_socket.send(str(i).encode())
            client_socket.recv(1024).decode()

        



    elif message == "2":

        # Aca el servidor recibe los parametros necesarios para cifrar el mensaje de entrada mediante Gamal
        client_socket.send('oki'.encode())
        g = int(client_socket.recv(1024).decode())
        client_socket.send('oki'.encode())
        p = int(client_socket.recv(1024).decode())
        client_socket.send('oki'.encode())
        k = int(client_socket.recv(1024).decode())

        b = 29


        # Creacion del mensaje cifrado letra por letra
        y2 = []
        mensaje_num= change(mensaje)
        print(mensaje_num)
        for i in mensaje_num:
            y2.append(i*(k**b%p))

        y1 = (g**b)%p

        
        print(y2)
        # Envio del mensaje cifrado a el cliente
        client_socket.send(str(y1).encode())
        client_socket.recv(1024).decode()
        
        client_socket.send(str(len(y2)).encode())
        client_socket.recv(1024).decode()
        for i in y2:
            client_socket.send(str(i).encode())
            client_socket.recv(1024).decode()
    
        

##########################################################################################################  



#Cerrar la conexión
client_socket.close()
server_socket.close()
