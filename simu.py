from random import randint


class Horario:

    def __str__(self):
        return self.dia + " " + self.turno

    def __init__(self, dia, tur):
        self.dia = dia
        self.turno = tur


class Profesor:

    def dar_horario(self, cuando, turno):
        self.horarios.append( Horario(cuando, turno) )
        self.horarios_originales.append( Horario(cuando, turno) )

    def horarios_disponibles(self):
        return len(self.horarios)

    def reservar_horario(self):
        # Saco el horario de las posibles
        ran = None
        
        if len(self.horarios) > 0:
            ran = self.horarios.pop( randint( 0, len(self.horarios)-1 ) )
        
        return ran
        
    def restablecer(self):
        self.horarios.clear()
        self.horarios = [k for k in self.horarios_originales]

    def __str__(self):
        return self.nombre

    def __init__(self, nombre):
        self.nombre = nombre
        self.horarios = [ ]
        self.horarios_originales = [  ]
        
        #self.horario_materia = {}
        
#===============================================

class Solucion:
    # Conjunto de materia, profesor y horario

    def __init__(self, materia, profesor=None, horario=None):
        self.materia = materia
        self.profesor = profesor
        self.horario = horario
        
        if profesor == None:
            self.profesor = self.materia.dame_profesor()
            if self.profesor != None:
                self.horario = self.profesor.reservar_horario()
                #self.profesor = None if self.horario==None

        
        
    def __str__(self):
        return ' '.join(["Materia:", self.materia.nombre, "Profesor:", str(self.profesor), "Dia", str(self.horario)])
        
    def __repr__(self):
        return self.__str__()


class Materia:

    # Busco un profesor, si no hay la materia queda sin darse.
    # Si encuentra un profesor y el profesor no tiene horarios disponibles busca a otro.
    def dame_profesor(self):
        ok = True
        
        while( len(self.profesores) > 0 ):
            ran = randint(0, len(self.profesores)-1 )
            pro = self.profesores[ran]
            if pro.horarios_disponibles() <= 0:
                del self.profesores[ran]
            else:
                return pro
            
        return None

        
    def restablecer(self):
        self.profesores = [k for k in self.profesores_iniciales]
        
        return self


    def dar_profesores(self, profes=[]):
        for k in profes:
            self.profesores.append(k)
            self.profesores_iniciales.append(k)
        
    def dar_profesor(self, prof):
        self.profesores.append(prof)
        self.profesores_iniciales.append(prof)


    def __init__(self, nombre):
        self.profesores = [] # Quien puede darla
        self.profesores_iniciales = []
        
        self.nombre = nombre



def generar_randoms(veces):
    ret = []
    # cuidado con esto, no repetir materias ni profesores!!.
    mats = [ analisis, simulacion, circuitos, programacion, ingles, metodos, control, redes, operativos, seguridad ]
    profes = [otaduy, graciana, roberto, federico, gaston, fernando, ezequiel, pablo, fagalde]
    
    for vec in range(veces):
        solu = []
        #pmats = [h.restablecer() for h in mats] # Restablezco las materias (profesores nuevamente disponibles).
        for h in mats:
            h.restablecer()
        
        for pp in profes:
            pp = pp.restablecer() # Para una nueva solucion necesito restablecer el horario de mis profesores.
    
        for mat in mats:
            solu.append( Solucion( mat ) )
            
        ret.append(solu) # Agrego la solucion al conjunto de soluciones
    
    
    return ret
    
def reproducir(a,b):
    #a es solucion 1
    #b es solucion 2
    
    #IDEA: tomo la primera mitad de la solucion de A y la segunda mitad de B.
    #Las uno.
    #Si el horario de un profesor se repite en 2 materias se cambia el profesor por el de la otra solucion.
    #Si una solucion no tiene profesor para una materia lo intercambia con el de la otra.
    
    la = int(len(a)/2)
    lb = int(len(b)/2)
    
    c = a[0:la]+b[1+lb:]
    repetidos = {}
    
    for idp in range(len(c)):
        val = c[idp]
        
        if val == None:
            if idp <= la:
                c[idp] = b[idp]
            else:
                c[idp] = a[idp+1]
        
    
    for idx in range(len(c)):
        val = c[idx]
        if len(repetidos.setdefault( val.horario, [] )) > 0 and val.profesor in repetidos[val.horario]:
            if idx <= la:
                c[idx] = b[idx]
            else:
                c[idx] = a[idx+1]
        elif val.profesor != None:
            repetidos[val.horario].append(val.profesor)
            
    return c
    
    
    
    
def fitness(solucion):
    tot = 0
    for k in solucion:
        if k.profesor: # Se le asigno alguien ( la materia se dicta )
            tot += 1
            
    return tot
    # Cantidad de materias dadas. Probar materias+variedad de profesores?


# Funcion de comparacion para saber a quien selecciono
def compa(a):
    return fitness(a)
    
    
    
#=========================
# CARGA DE DATOS
#=========================
    
gaston = Profesor("Gaston")
fernando = Profesor("Fernando")
roberto = Profesor("Roberto")
ezequiel = Profesor("Ezequiel")
otaduy = Profesor("Otaduy")
graciana = Profesor("Graciana")
federico = Profesor("Federico")
pablo = Profesor("Pablo")
fagalde = Profesor("Fagalde")


# Aca van todos los profesores
def cargar_profesores():
    gaston.dar_horario( "lunes", "maniana" )
    #gaston.dar_horario( "martes", "maniana" )
    #gaston.dar_horario("jueves", "noche")
    gaston.dar_horario("sabado", "maniana")
    
    #fernando.dar_horario( "martes", "maniana" )
    fernando.dar_horario( "jueves", "maniana" )
    fernando.dar_horario( "viernes", "tarde" )
    
    #roberto.dar_horario( "lunes", "noche" )
    roberto.dar_horario("martes", "noche")
    #roberto.dar_horario("sabado", "maniana")
    
    ezequiel.dar_horario("miercoles", "noche")
    #ezequiel.dar_horario("lunes", "tarde")

    otaduy.dar_horario("jueves", "noche")
    #otaduy.dar_horario("jueves", "maniana")
    
    graciana.dar_horario("lunes", "maniana")
    #graciana.dar_horario("lunes", "noche")
    #graciana.dar_horario("martes", "maniana")
    #graciana.dar_horario("martes", "noche")
    graciana.dar_horario("sabado", "maniana")
    
    #federico.dar_horario("lunes", "noche")
    federico.dar_horario("martes", "maniana")
    #federico.dar_horario( "miercoles", "tarde" )
    #federico.dar_horario("jueves", "noche")
    federico.dar_horario("sabado", "maniana")
    
    fagalde.dar_horario( "sabado", "tarde" )
    #fagalde.dar_horario("miercoles", "noche" )
    fagalde.dar_horario("miercoles", "maniana" )
    #fagalde.dar_horario("lunes", "maniana" )
    
    pablo.dar_horario("lunes", "noche")
    #pablo.dar_horario("jueves", "tarde")
  
  
#===============================================
    
analisis = Materia("Analisis")
simulacion = Materia("Simulacion")
circuitos = Materia("Circuitos")
programacion = Materia("Programacion")
ingles = Materia("Ingles")
metodos = Materia("Metodos")
control = Materia("Control")
seguridad = Materia("Seguridad")
operativos = Materia("Operativos")
redes = Materia("Redes")

#===============================================
# aca van todas las materias
def cargar_materias():
    analisis.dar_profesores( [gaston, ezequiel, graciana] )
    simulacion.dar_profesores( [fernando, gaston, ezequiel] )
    circuitos.dar_profesores( [roberto, federico] )
    programacion.dar_profesores( [fernando, otaduy, pablo] )
    ingles.dar_profesores( [ezequiel, federico] )
    metodos.dar_profesores( [roberto, gaston, graciana] )
    control.dar_profesores( [federico, pablo, gaston] )
    redes.dar_profesores( [pablo, fagalde] )
    operativos.dar_profesores( [fagalde, roberto] )
    seguridad.dar_profesores( [fagalde, graciana] )
    

#===============================================
#===============================================

def main():
    cargar_profesores()
    cargar_materias()
    
    # estos randoms estan ya filtrados, no deberian existir repetidos ni cosas raras.
    # probablemente necesite menos iteraciones?
    arranque = generar_randoms(500) # todas las soluciones
    
    # 100 rondas
    for rondas in range(100):
        # ordeno mi poblacion por fitness
        arranque = sorted(arranque, key=compa, reverse=True) #arranque.sort( key=compa )
        # creo un grupo nuevo en base a los anteriores
        # quizas es mejor hacer mas hijos de los mismos que todos de distintos.
        extras = [ reproducir(arranque[x], arranque[x+1]) for x in range(100) ]
        # siguen a la siguiente ronda 400 seleccionados y 100 nuevos.
        arranque = arranque[:400] + extras
        # incluir mutacion?...
        pass
    
    # Reordeno la ultima ronda
    arranque = sorted(arranque, key=compa) #arranque.sort( key=compa )
    # Obtengo el mejor
    arranque = [ arranque[0] for x in sorted(arranque, key=compa, reverse=True) ]
    
    print( arranque[0] )
    
    
    
    totm = 0
    for cosa in arranque[0]:
        if cosa.profesor != None:
            totm+=1
        else:
            print(cosa.materia.nombre)
    
    print("Total materias:", totm)



main()

