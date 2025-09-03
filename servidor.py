import socket
import sys
import threading
import random
import time 
HOST = "localhost"  # Direccion ip del host (En este caso la wifi)
PORT = 65432  # Puerto al que se conectará el cliente
buffer_size = 1024
tablero=[]
global n
n = 0
global contador_jugadas
contador_jugadas=0
#global contador_jugadas
contador_jugadas = 0 #Se utiliza para contar las casillas que son acertadas por el usuario
#global controlador
controlador = 1

def servirPorSiempre(socketTcp, listaconexiones):
    try:
        while True:
            client_conn, client_addr = socketTcp.accept()
            print("Usuario Conectado: ", client_addr)
            listaconexiones.append(client_conn)
            thread_read = threading.Thread(target=recibir_datos, args=[client_conn, client_addr])
            thread_read.start()
            gestion_conexiones(listaConexiones)
    except Exception as e:
        print(e)

def gestion_conexiones(listaconexiones):
    for conn in listaconexiones:
        if conn.fileno() == -1:
            listaconexiones.remove(conn)
    print("hilos activos:", threading.active_count())
    print("enum", threading.enumerate())
    print("conexiones: ", len(listaconexiones))
    print(listaconexiones)


def recibir_datos(conn, addr):
    global contador_jugadas
    #global controlador
    try:
        cur_thread = threading.current_thread() #Se obtiene el hilo actual que se está ejecutando
        if(len(listaConexiones)==1):
            conn.sendall(b'1')
            crearTablero(tablero,conn)
        else:
            conn.sendall(b'0')
            while True:
                print("N es esto: ",n)
                if n==0:
                    time.sleep(3)
                else:
                    conn.sendall(str(n).encode('utf-8'))
                    break
        print("Tablero actual")
        print(n)
        mostrarTablero(tablero) #Se usa para mostrar el tablero 0's son casillas vacias y 1's son las minas
        while True:
            """data = conn.recv(1024)
            response = bytes("{}: {}".format(cur_thread.name, data), 'ascii')"""
            print("Recibiendo datos del jugador {} en el {}".format(addr, cur_thread.name))
            coordenadas = conn.recv(buffer_size) #Se reciben las coordenadas del cliente en formato (**,**)
            print(coordenadas) 
            filas = int(coordenadas[1:3])-1 
            print(filas)
            columnas = int(coordenadas[4:6])-1
            print(columnas)
            if filas >= n or columnas >= n: #Excepcion fuera de rango
                print("Fuera de rango")
                conn.sendall(b'3') #Se envia respuesta al cliente de código 3
                print("Tablero actual")
                mostrarTablero(tablero)  
            else:
                condicion = tablero[filas][columnas] 
                if condicion != 1 and condicion!=2:  #Se verifica que la casilla no tenga minas
                    print("Casilla válida")
                    tablero[filas][columnas] = 2 #Se coloca la jugada en la casilla
                    contador_jugadas = contador_jugadas + 1 #Se incrementa el contador de las jugadas
                    condicion_gane = (n*n)-m #Se necesita cumplir la condicion para ganar
                    if contador_jugadas == condicion_gane:  #Se verifica el número de jugadas
                        conn.sendall(b'1')   #Si gana, se envía el código 1 al usuario
                        conn.close()
                        break #En caso de ganar se sale del ciclo del juego y acaba
                    conn.sendall(b'2') #En dado caso de que todavía no gane se sigue en el juego y se envia el codigo 2
                elif condicion == 1: #Condicion para cuando se encuentra una mina
                    print("Se ha encontrado una mina")
                    conn.sendall(b'4') #Se envía el codigo 4 para el usuario
                    conn.close()
                    break #Se sale del ciclo del juego
                elif condicion == 2: #Condicion para cuando la casilla ya se ha elegido
                    print("Casilla ya elegida")
                    conn.sendall(b'5')
                print("Tablero actual")
                mostrarTablero(tablero) 
    except Exception as e:
        print(e)
    finally:
        conn.close()


def mostrarTablero(tablero): #Funcion para mostrar el tablero
    for filaT in tablero:
        for v in filaT:
            print(v, end=" ")
        print()

def crearTablero(tablero,conn):
    print("Esperando dificultad")
    global n
    global m
    dificultad = conn.recv(buffer_size) #Se recibe la dificultad
    dificultad = dificultad.lower() #Como la dificultad es una cadena, se convierten a minúsculas para las condiciones siguientes
    if dificultad==b'principiante': #Condiciones para crear el tablero
        print("Eligio principiante")
        n = 9 #Longitud del tablero
        m = 10 #Minas a poner
        conn.sendall(str(n).encode('utf-8')) #Servidor envía la longitud del tablero al cliente
    elif dificultad==b'avanzado':
        print("Eligio avanzado")
        n = 16
        m = 40
        conn.sendall(str(n).encode('utf-8'))
    elif dificultad==b'prueba' : #Tablero para pruebas, mas pequeño
        print("Entro a la prueba")
        n = 3
        m = 4
        conn.sendall(str(n).encode('utf-8'))
    print("Creando tablero...")
    #tablero = [] #Se empieza a crear el tablero
    for i in range(n):
        tablero.append([])
        for j in range(n):
            tablero[i].append(0) #Se rellena con 0's
    print("Poniendo minas...")
    i = 1
    while i <= m: #Se ponen las minas
        rand1 = random.randint(0,n-1) #Se crean posciciones de manera aleatoria
        rand2 = random.randint(0,n-1)
        if tablero[rand1][rand2] == 0: #Se pueden repetir, por lo que debemos confirmar que la casilla esté vacía
            tablero[rand1][rand2] = 1
        else :
            minascontrolador = 1
            while minascontrolador: #En caso de repetirse, iterar hasta obtener una casilla vacía
                rand1 = random.randint(0,n-1)
                rand2 = random.randint(0,n-1)
                if tablero[rand1][rand2] == 1:
                    minascontrolador = 1
                else:
                    tablero[rand1][rand2] = 1
                    minascontrolador = 0
        i = i + 1


listaConexiones = []
host, port, numConn = sys.argv[1:4]

if len(sys.argv) != 4:
    print("usage:", sys.argv[0], "<host> <port> <num_connections>")
    sys.exit(1)

serveraddr = (host, int(port))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
    TCPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #Sirve para establecer opciones en un socket existente, permite reultilizacion de direccion del socket
    TCPServerSocket.bind(serveraddr)
    TCPServerSocket.listen(int(numConn))
    print("El servidor para el juego del Buscaminas está disponible para partidas: ")
    servirPorSiempre(TCPServerSocket, listaConexiones)
