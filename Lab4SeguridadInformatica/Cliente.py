# Felipe Vera y Marcelo Ibarra, Seguridad Informática

import socket



# Configuración del cliente
host = '127.0.0.1'
port = 12345

# Crear un socket del cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar al servidor
client_socket.connect((host, port))

###################################################################################################

# Reemplaza los numeros del mensaje recibido por letras en el abecedario dependiendo de su posición
def change_num(numero):
    alfabeto='abcdefghijklmnñopqrstuvwxyz'
    return alfabeto[numero]


######### Este es el ciclo infinito donde se pueden implementar todas las cosas del lab ###########

while True:


    # Recibir mensaje del servidor, tambien lo muestra en pantalla
    response = client_socket.recv(1024).decode()
    print(f"Respuesta del servidor: {response}")


    # Enviar mensaje al servidor, funciona igual que en codigo del server
    message = input("Mensaje al servidor: ")
    client_socket.send(message.encode())

    if message == "1":

        client_socket.recv(1024).decode()

        # Se definen los parametros necesarios para aplicar el cifrado RSA
        p= 647
        q= 569
        e= 211

        n= p*q
        fi_n= (p-1)*(q-1)

        # Envio de parametros para el servidor
        client_socket.send(str(n).encode())
        client_socket.recv(1024).decode()
        client_socket.send(str(e).encode())

        
        d= pow(e,-1,fi_n)
        mensaje_enc= []
        mensaje_des= []
        mensaje_des_str= ''

        # Ciclo para recibir el mensaje cifrado letra por letra
        largo= int(client_socket.recv(1024).decode())
        client_socket.send('oki'.encode())
        for i in range(largo):
            mensaje_enc.append(int(client_socket.recv(1024).decode()))
            client_socket.send('oki'.encode())

        # Se muestra el mensaje cifrado en pantalla
        print(mensaje_enc)


        # Descifrado del mensaje letra por letra
        for i in mensaje_enc:
            mensaje_des.append((i**d)%n)

        print(mensaje_des)

        # Se revierte la funcion change del servidor para que el mensaje cambie de numeros a letras
        for i in mensaje_des:
            mensaje_des_str= mensaje_des_str+change_num(i)
    

        # Creacion del archivo mensajeseguro.txt para almacenar el mensaje descifrado
        seguro = open("mensajeseguro.txt",'a')
        seguro.write(mensaje_des_str)
        seguro.close()

        

               


    elif message == "2":

        client_socket.recv(1024).decode()

        # Se definen los parametros necesarios para aplicar el cifrado Gamal
        p = 157
        g = 67
        a = 23
        k = (g**a)%p

        # Envio de parametros para el servidor
        client_socket.send(str(g).encode())
        client_socket.recv(1024).decode()
        client_socket.send(str(p).encode())
        client_socket.recv(1024).decode()
        client_socket.send(str(k).encode())


        # Se reciben y1 y y2 del servidor
        y1= int(client_socket.recv(1024).decode())
        client_socket.send('oki'.encode())
        
        largo= int(client_socket.recv(1024).decode())
        client_socket.send('oki'.encode())

        # Ciclo para almacenar toda las letras cifradas del mensaje correspodientes a y2
        y2=[]
        mensaje_des=[]
        mensaje_des_str=''
        
        for i in range(largo):
            y2.append(int(client_socket.recv(1024).decode()))
            client_socket.send('oki'.encode())


        print(y2)
        # Ciclo para descifrar letra por letra el mensaje cifrado
        for i in y2:
            mensaje_des.append(y1**(p-1-a)*i%p)
        print(mensaje_des)

        # Se revierte la funcion change del servidor para tranformar el mensaje de numero a letra
        for i in mensaje_des:
            mensaje_des_str= mensaje_des_str+change_num(i)

    
        # Creacion del archivo mensajeseguro.txt para almacenar el mensaje descifrado 
        seguro = open("mensajeseguro.txt",'a')
        seguro.write(mensaje_des_str)
        seguro.close()

        

##########################################################################################################
    

#Cerrar la conexión
client_socket.close()


