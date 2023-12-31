from pyodbc import IntegrityError, ProgrammingError

from PROYECTO.datos.conexion import Conexion
from PROYECTO.dominio.estudiante import Estudiante


class EstudianteDao:
    _INSERTAR ="INSERT INTO Estudiantes( cedula, nombre, apellido,email, carrera, activo) VALUES (?,?,?,?,?,?)"
              #"('0912568965','Luisa', 'Cruuz','lcruz@gmail.com','GIG',1 )"
    _SELECCIONAR_X_CEDULA = "select id, cedula, nombre, apellido, email, carrera, activo from Estudiantes " \
                            "where cedula = ?"

    @classmethod
    def insert_estudiante(cls, estudiante):
        #cursor= Conexion.obtenerCursor()
        respuesta={'exito':False, 'mensaje':''}
        flag_exito= False
        mensaje=''

        try:
            with Conexion.obtenerCursor() as cursor:
                datos=(estudiante.cedula, estudiante.nombre, estudiante.apellido,estudiante.email,estudiante.carrera
                       ,estudiante.activo)
                cursor.execute(cls._INSERTAR, datos)
                flag_exito= True
                mensaje = 'INGRESO EXITOSO'
        except IntegrityError as e:
            flag_exito = False
           # print('LA CEDULA QUE INGRESA YA EXISTE')
            if e.__str__().find('cedula') > 0:
                print('ESTA CEDULA YA HA SIDO INGRESADA')
                mensaje='ESTA CEDULA YA HA SIDO INGRESADA'

            elif e.__str__().find('Email') > 0:
                print('ESTA EMAIL YA HA SIDO INGRESADO')
                mensaje='ESTe EMAIL YA HA SIDO INGRESADO'
            else:
                print('ERROR  DE INTEGRIDAD')
                mensaje='ERROR  DE INTEGRIDAD'

        except ProgrammingError as e:
            flag_exito = False
            print('Los datos ingresados no son del tamaño permitido')
            mensaje='Los datos ingresados no son del tamaño permitido'
        except Exception as e:
            flag_exito = False
            print(e)

        finally:
            respuesta['exito'] = flag_exito
            respuesta['mensaje'] = mensaje
            return respuesta


    @classmethod
    def seleccionar_por_cedula(cls, estudiante):
        persona_encontrada= None
        try:
            with Conexion.obtenerCursor() as cursor:
                datos=(estudiante.cedula,)
                resultado= cursor.execute(cls._SELECCIONAR_X_CEDULA, datos)
                persona_encontrada=resultado.fetchone()
                estudiante.email= persona_encontrada[4]
                estudiante.nombre = persona_encontrada[2]
                estudiante.apellido = persona_encontrada[3]
                estudiante.carrera = persona_encontrada[5]
                estudiante.activo= persona_encontrada[6]
                estudiante.cedula = persona_encontrada[1]
                estudiante.id = persona_encontrada[0]
        except Exception as e:
            print(e)
        finally:
            return estudiante


if __name__ == '__main__':
    Estudiante1= Estudiante()
    Estudiante1.cedula='1954264919'
    Estudiante1.nombre='Juan'
    Estudiante1.apellido = 'Cruz'
    Estudiante1.email = 'jcruz@gmail.com'
    Estudiante1.carrera= 'LGI'
    Estudiante1.activo = True

    #EstudianteDao.insert_estudiante(Estudiante1)
    persona_encontrada= EstudianteDao.seleccionar_por_cedula(Estudiante1)
    print(persona_encontrada)

