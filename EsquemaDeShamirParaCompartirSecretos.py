import random
from sympy import nextprime, mod_inverse

def generar_polinomio(secret, grado_polinomio):
    # Genera un polinomio aleatorio de grado grado_polinomio-1, con el coeficiente principal igual al secreto
    coeficientes = [random.randint(0, 100) for _ in range(grado_polinomio)]
    coeficientes[0] = secret
    return coeficientes

def dividir_secreto(secret, num_partes, grado_polinomio):
    # Divide el secreto num_partes utilizando el esquema de Shamir
    if num_partes < grado_polinomio:
        raise ValueError("El número de partes debe ser al menos igual al grado del polinomio.")

    partes = []
    coeficientes = generar_polinomio(secret, grado_polinomio)
    for i in range(1, num_partes + 1):
        x = i
        y = evaluar_polinomio(coeficientes, x)
        partes.append((x, y))
    return partes

def evaluar_polinomio(coeficientes, x):
    # Evalúa el polinomio representado por los coeficientes en el punto x
    y = sum(coef * (x ** i) for i, coef in enumerate(coeficientes))
    return y

def recuperar_secreto(partes, punto_a_determinar):
    # Reconstruye el secreto utilizando la interpolación de Lagrange
    secreto = 0
    max_y = max(partes, key=lambda x: int(x[1]))[1]
    p = nextprime(max_y)  # Actualizamos p para que sea el primo más cercano o mayor que el valor máximo de y en las partes
    for i in range(len(partes)):
        x_i, y_i = partes[i]
        term = y_i
        for j in range(len(partes)):
            if i != j:
                x_j, _ = partes[j]
                term = term * (punto_a_determinar - x_j) * mod_inverse(x_i - x_j, p)
        secreto += term
    return int(secreto) % p

# Parámetros del esquema de Shamir
secreto = 532
num_partes = 7
grado_polinomio = 5

# Compartir el secreto
partes = dividir_secreto(secreto, num_partes, grado_polinomio)
print("Partes generadas:", partes)

# Reconstruir el secreto
secreto_reconstruido = recuperar_secreto(partes, 0)
print("El secreto reconstruido es:", secreto_reconstruido)