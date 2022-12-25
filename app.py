from flask import Flask, render_template, request
from flask_mysqldb import MySQL


app = Flask(__name__)

#CONEXION A LA BASE DE DATOS
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'udenar'
app.config['MYSQL_PORT'] = 3306
mysql = MySQL(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin/estudiantes')
def estudiantes():
    return render_template('estudiantes.html')


@app.route('/admin/estudiantes/nuevo', methods=['POST']) # Funcion sirve para la creacion de estudiantes (CREATE)
def nuevo_estudiante():
    
    codigo = request.form["codigo"]
    nombres = request.form["nombres"]
    apellidos = request.form["apellidos"]
    correo = request.form["correo"]
    telefono = request.form["telefono"]
    
    datos = dict()
    try:
        sql = f"""
                INSERT INTO estudiante (codigo, nombres, apellidos, correo, telefono)
                VALUES ({codigo}, '{nombres}', '{apellidos}', '{correo}', '{telefono}')
            """
        cursor = mysql.connection.cursor()
        cursor.execute(sql)
        filas = cursor.rowcount
        mysql.connection.commit()
        cursor.close()
        
        if filas != 1:
            datos["error"] = "Numero de filas afectadas no es correcto"
        else:
            datos["exito"] = "El estudiante se agregó correctamente"
    
    except:
        datos["error"] = "Error al insertar los datos del estudiante."
    
    return inscritos(datos)


@app.route('/admin/inscritos') # Funcion sirve para la leer todos los datos en la tabla estudiantes (READ)
def inscritos(datos= dict()):
    
    try:
        sql = f"""
                SELECT codigo, nombres, apellidos, correo, telefono
                FROM estudiante
            """
        cursor = mysql.connection.cursor()
        cursor.execute(sql)
        resultado = cursor.fetchall()
        datos["estudiantes"] = resultado
        cursor.close()
        
    except:
        datos["error"] = "Error al consultar los estudiantes"

    return render_template('inscritos.html', modelo = datos) # Cada vez que hay una seleccion de estudiante en un dicrionario es porque esos datos se pasaran a un html mediante un modelo para mostrarlo en pantalla


# ACTUALIZACION DE DATOS

@app.route('/admin/estudiantes/editar/<id>') # Funcion sirve para leer UN ESTUDIANTE de la tabla estudiantes (READ)
def editar(id: str):
    datos = dict()
    try:
        if id == None or len(id) == 0:
            raise Exception("Id invalido")
    
        # Consultar la informacion del estudiante con el codigo id
        sql = f"""
            SELECT codigo, nombres, apellidos, correo, telefono
            FROM estudiante
            WHERE codigo = '{id}'
            """
        # Abrir el cursor a la base de datos
        cursor = mysql.connection.cursor()
        cursor.execute(sql)
        # Cargar la informacion del estudiante en el dictionary
        registro = cursor.fetchone()
        datos["estudiantes"] = registro
        cursor.close()
        # Mostrar la plantilla
        return render_template('estudiante_editar.html', modelo = datos) # Cada vez que hay una seleccion de estudiante en un dicrionario es porque esos datos se pasaran a un html mediante un modelo para mostrarlo en pantalla
    except Exception as ex:
        datos["error"] = str(ex)
        return inscritos(datos)


@app.route('/admin/estudiantes/actualizar', methods = ['POST']) # Funcion recoge los datos de <estudiante_editar.html> y lo actualiza (UPDATE)
def actualizar():
    
    codigo = request.form["codigo"]
    nombres = request.form["nombres"]
    apellidos = request.form["apellidos"]
    correo = request.form["correo"]
    telefono = request.form["telefono"]
    
    datos= dict()
    try:
        sql = f"""
            UPDATE estudiante
            SET nombres = '{nombres}',
                apellidos = '{apellidos}',
                correo = '{correo}',
                telefono = '{telefono}'
                WHERE codigo = '{codigo}'
            """
        cursor = mysql.connection.cursor()
        cursor.execute(sql)
        filas = cursor.rowcount
        mysql.connection.commit()
        cursor.close()
        
        if filas != 1:
            datos["error"] = "Numero de filas afectadas no es correcto"
        else:
            datos["exito"] = "Los datos del estudiante se actualizaron exitosamente"
    
    except:
        datos["error"] = "Error al actualizar los datos del estudiante."
    
    return inscritos(datos)

@app.route('/admin/estudiantes/eliminar/<id>')
def eliminar(id: str):
    if id == None or len(id) == 0:
        raise Exception("Id invalido")
    
    datos= dict()
    try:
        sql = f"""
            DELETE
            FROM estudiante
            WHERE codigo = '{id}'
            """
        cursor = mysql.connection.cursor()
        cursor.execute(sql)
        filas = cursor.rowcount
        mysql.connection.commit()
        cursor.close()
        
        if filas != 1:
            datos["error"] = "Numero de filas afectadas no es correcto"
        
    except:
        datos["error"] = "Error al eliminar los datos del estudiante"
        
    return inscritos(datos)
        
# ===============================================================================
        

@app.route('/admin/materias')
def materias(datos = dict()):
    
    try:
        sql= f"""
            SELECT id, nombre, creditos
            FROM materia
        """
        cursor = mysql.connection.cursor()
        cursor.execute(sql)
        resultado = cursor.fetchall()
        datos["materias"] = resultado
        cursor.close()
    except:
        datos["error"] = "Error al consultar las materias en la base de datos"
        
    return render_template('materias.html', modelo = datos)       
        

@app.route('/admin/materia/nueva', methods=['POST'])
def crear_materia():
    
    id = request.form["id"]
    nombre = request.form["nombre"]
    creditos = request.form["creditos"]
    
    datos= dict()
    try:
        sql= f"""
            INSERT INTO materia (id, nombre, creditos)
            VALUES ({id}, '{nombre}', {creditos})
        """
        cursor = mysql.connection.cursor()
        cursor.execute(sql)
        filas = cursor.rowcount
        mysql.connection.commit()
        cursor.close()
        
        if filas != 1:
            datos["error"] = "Numero de filas afectadas no es correcto"
            
        else:
            datos["exito"] = "Se ha registrado la materia exitosamente"
    except:
        datos["error"] = "Error al registrar la materia"
    
    return materias(datos)
        
# UPDATE MATERIAS
@app.route('/admin/materias/editar/<id>')
def editar_materias(id: str):
    
    datos= dict()
    try:
        if id == None or len(id) == 0:
            raise Exception("Id invalido")
        
        sql = f"""
            SELECT id, nombre, creditos
            FROM materia
            WHERE id = '{id}'
        """
        cursor = mysql.connection.cursor()
        cursor.execute(sql)
        resultado = cursor.fetchone()
        datos["materias"] = resultado
        cursor.close()
        return render_template('materia_editar.html', modelo = datos)
    except:
        datos["error"] = "Error al consultar la materia en la base de datos"
        return materias(datos)
    
        
@app.route('/admin/materias/actualizar', methods = ['POST'])
def materia_actualizar():
    
    id = request.form["id"]
    nombre = request.form["nombre"]
    creditos = request.form["creditos"]
    
    datos = dict()
    try:
        sql = f"""
            UPDATE materia
            SET nombre = '{nombre}',
                creditos = '{creditos}'
                WHERE id = '{id}'
        """
        cursor = mysql.connection.cursor()
        cursor.execute(sql)
        filas = cursor.rowcount
        mysql.connection.commit()
        cursor.close()
        
        if filas != 1:
            datos["error"] = "Numero de filas afectadas no es correcto"
        else:
            datos["exito"] = "Se ha realido la actualizacion exitosamente"
    
    except:
        datos["error"] = "Error al actualizar la materia en la base de datos"
        
    return materias(datos)

@app.route('/admin/materias/eliminar/<id>')
def materia_eliminar(id: str):
    
    if id == None or len(id) == 0:
        raise Exception("Id invalido")
    
    datos = dict()
    try:
        sql = f"""
            DELETE
            FROM materia
            WHERE id = '{id}'
        """
        cursor = mysql.connection.cursor()
        cursor.execute(sql)
        borrada = cursor.rowcount
        mysql.connection.commit()
        cursor.close()
        
        if borrada != 1:
            datos["error"] = "Numero de filas afectadas no es correcto"
        else:
            datos["exito"] = "La materia se ha eliminado exitosamente"
    except:
        datos["error"] = "Error al eliminar la materia en la base de datos"
        
    return materias(datos)
        
# ===============================================================================

@app.route('/admin/matriculas')
def matricula():
    return render_template('matriculas.html')

@app.route('/admin/matriculas/buscar', methods=['POST'])
def matricula_buscar(codigo = None, datos=dict()):
    
    if codigo is None:
        codigo = request.form["codigo"]
    
    # Consulta datos de estudiante
    try:
        sql = f"""
            SELECT codigo, nombres, apellidos, correo, telefono
            FROM estudiante
            WHERE codigo = '{codigo}'
        """
        cursor = mysql.connection.cursor()
        cursor.execute(sql)
        estudiante = cursor.fetchone()
        datos["estudiante"] = estudiante
        cursor.close()
        
    # Consulta datos de materias
        sql = f"""
            SELECT ma.id, ma.nombre, ma.creditos
            FROM matricula m
            JOIN materia ma
            on (m.id_materia = ma.id)
            WHERE m.codigo_estudiante = '{codigo}'
        """
        cursor = mysql.connection.cursor()
        cursor.execute(sql)
        materias_ma = cursor.fetchall()
        print(materias_ma)
        datos["materias_matriculadas"] = materias_ma
        cursor.close()
        
        # Consulta de todas las materias disponibles
        sql = f"""
            SELECT id, nombre, creditos
            FROM materia
            """
        cursor = mysql.connection.cursor()
        cursor.execute(sql)
        materias = cursor.fetchall()
        datos["materias"] = materias
        cursor.close()

    except:
        datos["error"] = "El estudiante no se encuentra en la base de datos"
        
    return render_template('matriculas.html', modelo = datos)
    
@app.route('/admin/matriculas/agregar', methods = ['POST'])
def agregar_matricula():
    
    codigo = request.form["codigo"]
    materia = request.form["materia"]
    
    datos = dict()
    try:
            
        sql = f"""
            INSERT INTO matricula (codigo_estudiante, id_materia)
            VALUES ('{codigo}', {materia})
        """
        cursor = mysql.connection.cursor()
        cursor.execute(sql)
        filas = cursor.rowcount
        mysql.connection.commit()
        cursor.close()
        
        if filas != 1:
            datos["error"] = "Numero de filas afectadas no es correcto"
        else:
            datos["exito"] = "Se a matricula satisfactoriamente"
    except Exception as e:
        datos["error"] = "Error al intentar matricular la materia"
        print (e)
        
    return matricula_buscar(codigo, datos)

@app.route('/admin/matriculas/eliminar/<codigo_est>/<id_materia>')
def eliminar_matricula(codigo_est, id_materia):
    
    datos = dict()
    
    try:

        if codigo_est == None or len(codigo_est) == 0:
            raise Exception("El id de la materia no se reconoce")
        
        sql = f"""
            DELETE
            FROM matricula
            WHERE codigo_estudiante = '{codigo_est}'
            AND id_materia = {id_materia}
        """
        cursor = mysql.connection.cursor()
        cursor.execute(sql)
        eliminacion = cursor.rowcount
        mysql.connection.commit()
        cursor.close()
        
        if eliminacion != 1:
            datos["error"] = "Numero de filas afectadas no es correcto"
        else:
            datos["exito"] = "Se ha eliminado la materia matriculada satisfactoriamente"
    except Exception as e:
        datos["error"] = "No se ha podido eliminar la matricula"

    return matricula_buscar(codigo_est, datos)


app.run(debug=True)