# Importamos modulos necesarios
import random
import string


# Creamos funcion que contiene letras,caracteres especiales y numeros
def generador_de_contraseña(caracteres_minimos, numeros=True, caracteres_especiales=True):
    letras = string.ascii_letters + "ñÑ"
    digitos = string.digits
    especiales = string.punctuation

 # creamos un string de donde se van a seleccionar los caracteres al genera la contraseña
    caracteres = letras
    if numeros:
        caracteres += digitos
    if caracteres_especiales:
        caracteres += especiales

# variables para el bucle
    contraseña = ""
    requisitos = False
    tiene_numero = False
    tiene_especial = False

# bucle que genera un caracter random que se agrega a la contraseña hasta cumplir requisitos
    while not requisitos or len(contraseña) < caracteres_minimos:
        nuevo_caracter = random.choice(caracteres)
        contraseña += nuevo_caracter
        # aca nos fijamos si el nuevo caracter tiene numero o especiales y lo hacemos true
        if nuevo_caracter in digitos:
            tiene_numero = True
        elif nuevo_caracter in especiales:
            tiene_especial = True
        # los sumamos a requisitos
        requisitos = True
        if numeros:
            requisitos = tiene_numero
        if caracteres_especiales:
            requisitos = requisitos and tiene_especial
    return contraseña


# generamos los inputs para que el usuario escriba
# generamos un bucle para que si el usuario no ingresa un numero le vuelva a preguntar lo mismo
caracteres_minimos = None
while caracteres_minimos is None:
    try:
        caracteres_minimos = int(input("Ingrese el minimo de caracteres: "))
    except ValueError:
        print("Por favor, ingrese un número válido.")
# si el usuario ingresa algo que no sea si o no, se toma por no
tiene_numero = input("Quieres ingresar numeros?(si/no): ").lower() == "si"
tiene_especial = input(
    "Quieres ingresar caracteres especiales?(si/no): ").lower() == "si"
contraseña = generador_de_contraseña(caracteres_minimos, tiene_numero, tiene_especial)
print("La contraseña generada es: ", contraseña)
