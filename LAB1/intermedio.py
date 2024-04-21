import socket as skt

"""
def resultado(jugada, contra):
    jugada = Jugada que realiza el cliente
    contra = Jugada que realiza el servidor cachipun
    Return = Retorna si el jugador gana, pierde o empata
"""
def resultado(jugada, contra):
    if jugada == contra:
        return "Empate"
    elif jugada == "1" and contra == "2":
        return "Pierdes"
    elif jugada == "1" and contra == "3":
        return "Ganas"
    elif jugada == "2" and contra == "1":
        return "Ganas"
    elif jugada == "2" and contra == "3":
        return "Pierdes"
    elif jugada == "3" and contra == "1":
        return "Pierdes"
    elif jugada == "3" and contra == "2":
        return "Ganas"

"""
def bot_jugo(numero):
    numero = Numero que retorno el servidor cachipun
    return: Retorna Piedra, Papel o Tijera dependiendo de la respuesta
"""
def bot_jugo(numero):
    if numero == '1':
        return "Piedra"
    elif numero == '2':
        return "Papel"
    elif numero == '3':
        return "Tijera"

#Conexion con el cliente
puerto = 50001

serverSocket = skt.socket(skt.AF_INET, skt.SOCK_STREAM)

serverSocket.bind(('', puerto))

serverSocket.listen(1)

#Conexion con el servidor cachipun
direccionServidor = "localhost"
puerto2 = 50002

cachipunSocket = skt.socket(skt.AF_INET, skt.SOCK_DGRAM)
print("Servidor intermedio iniciado, esperando solicitud de conexión del cliente")
print("El servidor se ejecuta en el puerto", puerto)

clienteSocket, clienteDireccion = serverSocket.accept()
print("Conexion establecida con el cliente en el puerto", puerto)

while True:
    jugador = 0
    bot = 0
    seguimos = 'Nadie'
    mensaje = clienteSocket.recv(2048).decode()
    if mensaje == "1":
        print("Intentando conexión con servidor Cachipun")
        empezar = "EMPEZAR"
        try:
            cachipunSocket.sendto(empezar.encode(), (direccionServidor, puerto2))
            mgs, addr = cachipunSocket.recvfrom(2048)
        except:
            print("Error de conexión, compruebe que el servidor Cachipun esté encendido e intente nuevamente")
            quit()

        print("Conexión establecida con el servidor Cachipun en el puerto", puerto2)
        print("Consultando disponibilidad del servidor Cachipun para jugar")
        #El servidor cachipun esta disponible
        if str(mgs) == "b'OK'":
            respuesta = "Los servidores del juego están operativos"
            print(respuesta)
            mgs, addr = cachipunSocket.recvfrom(2048)
            nuevo_puerto = int(str(mgs)[2:7])
            print("La partida se ejecutará en el puerto", nuevo_puerto)
            clienteSocket.sendall(respuesta.encode())
            #Comienza juego con el cliente y el servidor
            while True:
                jugada = clienteSocket.recv(2048).decode()
                cachipunSocket.sendto("JUGADA".encode(), (direccionServidor, nuevo_puerto))
                mgs, addr = cachipunSocket.recvfrom(2048)
                print("El bot jugó "+bot_jugo(str(mgs)[2]))
                res = resultado(jugada, str(mgs)[2])
                if res == "Ganas":
                    jugador += 1
                elif res == "Pierdes":
                    bot += 1
                marcador = "Jugador: "+str(jugador)+"; Bot: "+str(bot)
                if jugador == 3:
                    seguimos = 'Jugador'
                elif bot == 3:
                    seguimos = 'Bot'
                jugo = "El bot jugó "+bot_jugo(str(mgs)[2])
                final = jugo+","+res+","+marcador+","+str(seguimos)
                clienteSocket.send(final.encode())
                fin = clienteSocket.recv(2048).decode()
                if fin == "Termina":
                    cachipunSocket.sendto("TJUGADA".encode(), (direccionServidor, nuevo_puerto))
                    break
        #El servidor no esta disponible
        else:
            print("Los servidores del juego no están disponibles, intente nuevamente")
            clienteSocket.sendall("Los servidores del juego no están disponibles, intente nuevamente".encode())
    else:
        termino = "TERMINO"
        cachipunSocket.sendto(termino.encode(), (direccionServidor, puerto2))
        break
print("Servidor apagado")
cachipunSocket.close()
clienteSocket.close()