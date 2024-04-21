import socket as skt

#Conexion con el servidor intermedio
servidorAddr = "localhost"
puerto = 50001
socketCliente = skt.socket(skt.AF_INET, skt.SOCK_STREAM)

try:
    print("Solicitando conexión con el servidor intermedio")
    socketCliente.connect((servidorAddr, puerto))

except:
    print("Error de conexión, compruebe que el servidor intermedio esté encendido e intente nuevamente")
    quit()

print("Conexión establecida con el servidor intermedio en el puerto",puerto)
print("-----------------")
print("Bienvenid@ a Cachipun")

while True:
    #Menu para jugar
    print("Ingrese 1 para jugar")
    print("Ingrese 2 para salir")
    enviar = input(">>")

    while ((enviar!="1") and (enviar!="2")):
        print("Opción no válida. Intente nuevamente")
        print("-----------------")
        print("Ingrese 1 para jugar")
        print("Ingrese 2 para salir")
        enviar = input(">>")

    socketCliente.sendall(enviar.encode())
    if enviar == "1":
        print("Cargando partida")
        response = socketCliente.recv(2048).decode()
        if response == "Los servidores del juego están operativos":
            print(response)
            print("-----------------")
            #Comienza la partida
            while True:
                print("Ingrese 1 para jugar Piedra")
                print("Ingrese 2 para jugar Papel")
                print("Ingrese 3 para jugar Tijera")
                jugada = input(">>")
                while (jugada!="1") and (jugada!="2") and (jugada!="3"):
                    print("Opción no válida. Intente nuevamente")
                    print("-----------------")
                    print("Ingrese 1 para jugar Piedra")
                    print("Ingrese 2 para jugar Papel")
                    print("Ingrese 3 para jugar Tijera")
                    jugada = input(">>")
                print("-----------------")

                #Retorno de resultados del servidor intermedio
                socketCliente.sendall(jugada.encode())                
                jugo = socketCliente.recv(2048).decode()
                final = jugo.split(',')
                print(final[0])
                print(final[1])
                print(final[2])
                print("-----------------")
                
                seguimos = final[3]
                if seguimos == 'Jugador':
                    print("Felicidades, has ganado")
                    print("-----------------")
                    socketCliente.sendall("Termina".encode())
                    break
                elif seguimos == 'Bot':
                    print("Lo siento, has perdido")
                    print("-----------------")
                    socketCliente.sendall("Termina".encode())
                    break
                else:
                    socketCliente.sendall("Sigue".encode())
        elif response == "Los servidores del juego no están disponibles, intente nuevamente":
            print("Lo sentimos, los servidores del juego no están disponibles, intente nuevamente")
        else:
            print("Error de conexión, compruebe que el servidor intermedio se haya conectado al servidor Cachipun e intente nuevamente")
            quit()
    else:
        print("Gracias por jugar a Cachipun")
        break
socketCliente.close()
