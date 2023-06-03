# pylint: disable=E1101
# importamos modulo
import curses
from curses import wrapper
import time
import random
# inicializamos


# PASO 2: Creamos la pantalla de inicio con una funcion
def pantalla_inicial(stdscr):
    # limpiamos la pantalla c
    stdscr.clear()
    # elegimos donde queremos que empiece el texto, si no ponemos nada es 0, 0 por default(fila, columna) + el texto
    stdscr.addstr(
        "Bienvenido! Este es un test para mejorar tu velocidad al escribir, mucha suerte!")
    # segundo mensaje para arrancar el test con un salto de linea \n
    stdscr.addstr("\nPresiona cualquier tecla para comenzar!")
    # refrescamos la pantalla
    stdscr.refresh()
    # getkey() sabemos que es lo que escribe el usuario y poder trackear las palabras por minuto
    stdscr.getkey()


# PASO 4:Creamos una funcion para que cuando el usuario vaya escribiendo se sobreponga con el texto y cambie el color, lo hacemos con for
def sobreponer_texto(stdscr, texto, actual, ppm=0):
    stdscr.addstr(texto)
    stdscr.addstr(1, 0, f"PPM: {ppm}")

    for i, char in enumerate(actual):
        caracter_correcto = texto[i]
        color = curses.color_pair(1)
        if char != caracter_correcto:
            color = curses.color_pair(2)

        stdscr.addstr(0, i, char, color)


# Creamos una funcion para llamar al archivo texto.txt que contiene los textos que apareceran de forma random
def cargar_texto():
    with open("Textos.txt", "r") as i:
        lineas = i.readlines()
        return random.choice(lineas).strip()

# PASO 3: creamos funcion para mostrar al usuario lo que escribir y recibir lo que el escribe


def ppm_test(stdscr):
    texto_test = cargar_texto()
    # en esta list se almacena lo que el usuario va escribiendo, usamos una lista para despues poder remover caracteres
    texto_actual = []
    ppm = 0
    # trackeamos el tiempo de inicio
    tiempo_inicial = time.time()
    # nodelay()porque sino el tiempo no decrece ya que espera una key
    stdscr.nodelay(True)

    # Bucle para que el usuario escriba sobre el texto que ve y si lo hace bien que sea color verde y mal color rojo
    while True:
        # esta variable evita que el numero sea 0, si da 0 nos devuelve 1
        tiempo_transcurrido = max(time.time() - tiempo_inicial, 1)
        # ahora calculamos las palabras por minuto ej : 20 caracteres en 10 segundos. 10 / 60 = 0.16. 30 / 0.16  = 187, 5 caracteres pm / 5 = ppm
        ppm = round((len(texto_actual) / (tiempo_transcurrido / 60)) / 5)
        stdscr.clear()
        sobreponer_texto(stdscr, texto_test, texto_actual, ppm)
        stdscr.refresh()

    # metodo join() para convertir la lista en string para saber si el usuario termino de escribir todo el texto bien y luego comparamos
        if "".join(texto_actual) == texto_test:
            # nodelay(false) para quitar el delay cuando el usuario termina y asi poder preguntar si quiere jugar denuevo
            stdscr.nodelay(False)
            break

        # try except para que no tire un error al no presionar una key ya que esta el nodelay(true)
        try:
            key = stdscr.getkey()
        except:
            continue

        if texto_actual == []:
            tiempo_inicial = time.time()

        if ord(key) == 27:
            break

            # al usar curses si apretamos la tecla de borrar lo que hace es ir para atras, lo modifcamos en todas sus furmas con el siguiente if
        if key in ("KEY_BACKSPACE", "\b", "\x7f"):
            if len(texto_actual) > 0:
                texto_actual.pop()
        # evitamos que el usuario escriba mas de lo que muestra el texto, para no poner mas caracteres de los que tiene la lista
        elif len(texto_actual) < len(texto_test):
            texto_actual.append(key)


# PASO 1:creamos funcion standard output screen y agregamos las funciones necesarias y tambien le damos estilo a la terminal
def main(stdscr):
    # elegimos los colores que queremos que aparezcan en las letras y en el fondo de las letras
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    pantalla_inicial(stdscr)
    # bucle para que no termine el juego al apretar una tecla cuando se competa el test, sino que se pueda jugar de nuevo
    while True:

        ppm_test(stdscr)
        stdscr.addstr(
            2, 0, "Lograste completar el test! Presiona cualquier tecla para continuar!")
        key = stdscr.getkey()

        # ASCII esc == 27 para salir
        if ord(key) == 27:
            break


# pasamos la funcion main a la funcion wrapper para que inicialice el modulo y a la vez ejecute la funcion main
wrapper(main)
