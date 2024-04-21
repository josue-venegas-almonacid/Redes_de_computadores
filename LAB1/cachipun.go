package main

import (
	"fmt"
	"math/rand"
	"net"
	"strconv"
	"strings"
	"time"
)

//func Use(): Funcion que utiliza variables para no generar error de uso
func Use(vals ...interface{}) {
	for _, val := range vals {
		_ = val
	}
}

func main() {
	//Conexion con el servidor intermedio
	r := rand.New(rand.NewSource(time.Now().UnixNano()))
	PUERTO := ":50002"
	BUFFER := 1024
	fmt.Println("Servidor Cachipun iniciado, esperando mensajes de servidor intermedio")
	fmt.Println("El servidor se ejecuta en el puerto", PUERTO[1:])
	fmt.Println("-----------------")
	s, err := net.ResolveUDPAddr("udp4", PUERTO)
	if err != nil {
		fmt.Println(err)
		return
	}
	conexion, err := net.ListenUDP("udp4", s)
	if err != nil {
		fmt.Println(err)
		return
	}
	defer conexion.Close()
	buffer := make([]byte, BUFFER)
	var jugada int
	var partida int
	var nuevo_puerto int
	//Recibe respuestas de parte del servidor intermedio
	for {
		n, addr, err := conexion.ReadFromUDP(buffer)
		fmt.Println("El cliente envió ->", string(buffer[0:n]))
		if strings.TrimSpace(string(buffer[0:n])) == "TERMINO" {
			fmt.Println("Servidor apagado")
			return
		}
		ok := []byte("OK")
		partida = r.Intn(10)
		//El servidor no esta disponible para jugar
		if partida == 9 {
			SALIR := []byte("SALIR")
			_, err = conexion.WriteToUDP(SALIR, addr)
			if err != nil {
				fmt.Println(err)
				return
			}
		//El servidor comienza a jugar
		} else {
			_, err = conexion.WriteToUDP(ok, addr)
			if err != nil {
				fmt.Println(err)
				return
			}
			//Abre el nuevo puerto de juego
			nuevo_puerto = r.Intn(52000-50003) + 50003
			_, err = conexion.WriteToUDP([]byte(strconv.Itoa(nuevo_puerto)), addr)
			NEW_PUERTO := ":" + strconv.Itoa(nuevo_puerto)
			s, err := net.ResolveUDPAddr("udp4", NEW_PUERTO)
			if err != nil {
				fmt.Println(err)
				return
			}
			conexion, err := net.ListenUDP("udp4", s)
			if err != nil {
				fmt.Println(err)
				return
			}
			defer conexion.Close()
			fmt.Println("La partida se ejecutará en el puerto", strconv.Itoa(nuevo_puerto))
			fmt.Println("-----------------")
			for {
				//Servidor hace sus jugadas para enviarlas al servidor intermedio
				n, addr, err := conexion.ReadFromUDP(buffer)
				Use(addr, err)
				fmt.Println("El cliente envió ->", string(buffer[0:n]))
				if strings.TrimSpace(string(buffer[0:n])) == "TJUGADA" {
					break
				}
				jugada = r.Intn(3) + 1
				_, err = conexion.WriteToUDP([]byte(strconv.Itoa(jugada)), addr)
				fmt.Println("El servidor enviará ->", strconv.Itoa(jugada))
				fmt.Println("-----------------")
			}
		}
	}
}
