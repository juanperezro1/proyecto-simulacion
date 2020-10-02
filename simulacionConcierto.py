import random
import simpy
import numpy

semilla = 40
numero_personas = 300
llegada_personas = [0,120] #Tiempo de llegada de las personas 
atencion_personas = [300, 420] #Tiempo de atención de las personas
numero_servidores = 2 #Número de servidores
 
#Variable de desempeño
cola = 0
cola_maxima = 0
espera_personas = numpy.array([])

def llegada(env, numero, contador):

    for i in range(numero):
        c = persona(env, 'Persona %02d' % i, contador)
        env.process(c)
        tiempo_llegada = random.uniform(llegada_personas[0],llegada_personas[1]) #Generar los tiempo de llegada de cada persona 
        print("Tiempo de llegada",tiempo_llegada)
        yield env.timeout(tiempo_llegada) 
        
        
def persona(env, nombre, servidor):
  
    llegada = env.now
    print('%7.2f'%(env.now)," Llega la persona ", nombre)
    global cola
    global cola_maxima 
    global espera_personas   
    
    with servidor.request() as req: #Atienede a la persona - El servidor pasa de estar descupado a ocupado durante el tiempo que se le envie
        
        cola += 1
        if cola > cola_maxima:
            cola_maxima = cola
        
        results = yield req	
        cola = cola - 1
        espera = env.now - llegada #Se calcula la espera
        espera_personas = numpy.append(espera_personas, espera)
        print('%7.2f'%(env.now), " La persona ",nombre," espera a ser atendido ",espera)
        tiempo_atencion = random.uniform(atencion_personas[0],atencion_personas[1]) #Calcular el tiempo de atención
        print("Tiempo de servicio",tiempo_atencion,"Persona", nombre)
        yield env.timeout(tiempo_atencion) #El servidor se desocupa cuando pase el tiempo de atención 
        print('%7.2f'%(env.now), " Sale la persona ",nombre)
    
print()
# Inicio de la simulación 
print('Concierto Pandémico')
print()
random.seed(semilla)
env = simpy.Environment()

# Incio del proceso y ejecución
servidor = simpy.Resource(env, capacity=numero_servidores)
env.process(llegada(env, numero_personas, servidor))
env.run()

simulacion_minutos = env.now/60
simulacion_horas = simulacion_minutos/60

print()
print("Tiempo de la simulación",simulacion_horas)
print()
print("Variables de desempleño")
print()
print("Cola máxima ",cola_maxima)
print("Tiempo promedio de espera ",'%7.2f'%(numpy.mean(espera_personas)))
