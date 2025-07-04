from funciones import *
from impresion import *
from metodos import *
import matplotlib.pyplot as plt
from tabulate import tabulate

#Parametros
print("Bienvenido al Algoritmo Genético")
print("Por favor, ingrese los parámetros del algoritmo:")
print("Los valores deben ser enteros")   
Pcruce = validar_porcentaje(input("Ingrese el porcentaje de cruce: "), "cruce")
Pmutacion = validar_porcentaje(input("Ingrese el porcentaje de mutacion: "), "mutación")
Pterminacion = validar_porcentaje(input("Ingrese el porcentaje de terminación: "), "terminación")
tamPoblacion = validar_tamano_poblacion(input("Ingrese el tamaño de la población: "))       
print("Los valores de las funciones deben ser en un formato 2x+3X o 4z+5z")
funcionFitnness = funcionesAVectores(validar_funcion(input("Ingrese la función global: ")))
funcionPesos = funcionesAVectores(validar_funcion(input("Ingrese la función fitness: ")))     
restriccion = validar_restriccion(input("Ingrese la restricción: "))
elitismo = 1   
respuesta = validar_opcion(input("Desea crear una población inicial aleatoria? (s/n): ").lower())
fenotipo = valoresMaxFenotipoBin(len(funcionFitnness))
continuar = False
if respuesta == 's':
    continuar = True
else:
    poblacionInicial = []
    ingresarPoblacionInicial(poblacionInicial, fenotipo, funcionPesos, restriccion, tamPoblacion)
while continuar:
    poblacionInicial = generarPoblacionInicial(funcionPesos, restriccion, tamPoblacion, fenotipo)
    #imprimir_tabla(poblacionInicial, funcionPesos, funcionFitnness, restriccion, 0)
    print(poblacionInicial)
    continuar = (input("Desea continuar con la evolución? (s/n): ").lower()) != 's'
iteraciones = int(input("Ingrese el número de iteraciones: "))
if iteraciones <= 0:
    print("El número de iteraciones debe ser mayor que 0")
variablesDesicion = len(poblacionInicial[0])

# Enumeración para métodos de selección
class MetodoSeleccion(Enum):
    RULETA = 1
    TORNEO = 2
    RANKING = 3

# Enumeración para métodos de cruce
class MetodoCruce(Enum):
    UN_PUNTO = 1
    DOS_PUNTOS = 2
    UNIFORME = 3

# Enumeración para métodos de mutación
class MetodoMutacion(Enum):
    BIT_FLIP = 1
    INTERCAMBIO = 2
    INVERSION = 3

 # Validación de operadores
seleccion = validar_opcion_operador(
    input("Ingrese el tipo de selección 1.ruleta, 2.torneo, 3.ranking: "),
    "selección",
    [1, 2, 3]
    )
        
cruce = validar_opcion_operador(
    input("Ingrese el tipo de cruce 1.un punto, 2.dos puntos, 3.uniforme: "),
    "cruce",
    [1, 2, 3]
    )
        
mutacion = validar_opcion_operador(
    input("Ingrese el tipo de mutación 1.bit flip, 2.intercambio, 3.inversión: "),
    "mutación",
    [1, 2, 3]
    )
        
operadores = {
        'seleccion': seleccion,
        'cruce': cruce,
        'mutacion': mutacion
    }

poblacion = np.array(poblacionInicial)

# Variables para almacenar estadísticas
historico_fitness = []
historico_factibles = []
historico_poblacion = []
historico_pesos = []

generacion = 0

# Algoritmo genético principal
while generacion < iteraciones and igualdad(poblacion, Pterminacion):
    # Evaluar población actual
    fitness, total_fitness, factibles = evaluar_poblacion(poblacion, fenotipo, funcionPesos, restriccion)
    
    # Guardar estadísticas
    historico_fitness.append(total_fitness)
    historico_factibles.append(sum(factibles))
    historico_pesos.append(funsionPesos(poblacion, funcionPesos, fenotipo))
    # Imprimir tabla detallada
    if generacion < 10 or generacion >= iteraciones - 10:
        imprimir_tabla(poblacion, fitness, factibles, generacion, operadores)
    
    # Crear nueva población
    nueva_poblacion = []
    
    # Aplicar elitismo (los mejores pasan directamente)
    if elitismo > 0:
        mejores_indices = np.argsort(fitness)[-elitismo:]
        for idx in mejores_indices:
            nueva_poblacion.append(poblacion[idx].copy())
    
    # Completar la nueva población
    while len(nueva_poblacion) < tamPoblacion:
        # Selección (usando el método seleccionado para esta generación)
        if operadores['seleccion'] == MetodoSeleccion.RULETA:
            padre1 = seleccion_ruleta(fitness, total_fitness, poblacion)
            padre2 = seleccion_ruleta(fitness, total_fitness, poblacion)
        elif operadores['seleccion'] == MetodoSeleccion.TORNEO:
            padre1 = seleccion_torneo(fitness, poblacion)
            padre2 = seleccion_torneo(fitness, poblacion)
        else:
            padre1 = seleccion_ranking(fitness, poblacion)
            padre2 = seleccion_ranking(fitness, poblacion)
        
        # Cruce (usando el método seleccionado para esta generación)
        if random.random() < Pcruce:
            if operadores['cruce'] == MetodoCruce.UN_PUNTO:
                hijo1, hijo2 = cruce_un_punto(padre1, padre2,  variablesDesicion)
            elif operadores['cruce'] == MetodoCruce.DOS_PUNTOS:
                hijo1, hijo2 = cruce_dos_puntos(padre1, padre2, variablesDesicion)
            else:
                hijo1, hijo2 = cruce_uniforme(padre1, padre2, variablesDesicion)
        else:
            hijo1, hijo2 = padre1.copy(), padre2.copy()
        
        # Mutación (usando el método seleccionado para esta generación)
        if operadores['mutacion'] == MetodoMutacion.BIT_FLIP:
            hijo1 = mutacion_bit_flip(hijo1, Pmutacion)
            hijo2 = mutacion_bit_flip(hijo2, Pmutacion)
        elif operadores['mutacion'] == MetodoMutacion.INTERCAMBIO:
            hijo1 = mutacion_intercambio(hijo1)
            hijo2 = mutacion_intercambio(hijo2)
        else:
            hijo1 = mutacion_inversion(hijo1, variablesDesicion)
            hijo2 = mutacion_inversion(hijo2, variablesDesicion)
        
        # Agregar a la nueva población (sin exceder el tamaño)
        if len(nueva_poblacion) < tamPoblacion:
            nueva_poblacion.append(hijo1)
        if len(nueva_poblacion) < tamPoblacion:
            nueva_poblacion.append(hijo2)
    generacion += 1
    # Actualizar población
    historico_poblacion.append(nueva_poblacion.copy())
    poblacion = np.array(nueva_poblacion)
    historico_pesos.append(funsionPesos(poblacion, funcionPesos, fenotipo))

imprimir_tabla_mejores_individuos(historico_poblacion, historico_pesos, historico_fitness, generacion)

# Gráficas de evolución
plt.figure(figsize=(15, 5))

# Gráfica de fitness
plt.subplot(1, 3, 1)
plt.plot(historico_fitness, marker='o')
plt.title("Evolución del Fitness Total")
plt.xlabel("Generación")
plt.ylabel("Fitness Total")
plt.grid(True)

# Gráfica de individuos factibles
plt.subplot(1, 3, 2)
plt.plot(historico_factibles, marker='o', color='orange')
plt.title("Evolución de Individuos Factibles")
plt.xlabel("Generación")
plt.ylabel("Número de Factibles")
plt.ylim(0, variablesDesicion)
plt.grid(True)

# Gráfica de operadores usados
# plt.subplot(1, 3, 3)
# operadores_seleccion = [op['seleccion'].name for op in historico_operadores]
# operadores_cruce = [op['cruce'].name for op in historico_operadores]
# operadores_mutacion = [op['mutacion'].name for op in historico_operadores]
# plt.plot(operadores_seleccion, marker='o', label='Selección')
# plt.plot(operadores_cruce, marker='s', label='Cruce')
# plt.plot(operadores_mutacion, marker='^', label='Mutación')
# plt.title("Operadores Utilizados por Generación")
# plt.xlabel("Generación")
# plt.ylabel("Tipo de Operador")
# plt.yticks([])
# plt.legend()
# plt.grid(True)

plt.tight_layout()
plt.show()

# Mostrar mejor solución encontrada
imprimir_tabla(poblacion, fitness, factibles, generacion, operadores)
# fitness_final, _, factibles_final = evaluar_poblacion(poblacion)
# mejor_idx = np.argmax(fitness_final)
# mejor_individuo = poblacion[mejor_idx]
# mejor_fitness = fitness_final[mejor_idx]
# mejor_factible = factibles_final[mejor_idx]
# mejor_peso = np.sum(mejor_individuo * funcionFitnness)

# print("\n--- Mejor Solución Encontrada ---")
# print(f"Cromosoma: {mejor_individuo.tolist()}")
# print(f"Fitness (Z): {mejor_fitness}")
# print(f"Factible: {'Sí' if mejor_factible else 'No'}")
# print(f"Peso total: {mejor_peso} (Límite: {restriccion})")
# print(f"Proyectos seleccionados: {[i+1 for i, gen in enumerate(mejor_individuo) if gen == 1]}")