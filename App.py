from flask import Flask, render_template, request, url_for, redirect, flash
from flask_mysqldb import MySQL

app= Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'bdprueba'
mysql = MySQL(app)

app.secret_key = 'mysecretkey'
@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM alumnos')
    data = cur.fetchall()
    print(data)
    return render_template('index.html', alumno = data)

@app.route('/agregar_alumno', methods=['POST'] )
def agregar_alumno():
    if request.method == 'POST':
        nombre= request.form['nombre']
        apellido= request.form['apellido']
        fecha_nacimiento= request.form['fecha_nacimiento']
        sexo= request.form['sexo']
        cur= mysql.connection.cursor()
        cur.execute('INSERT INTO alumnos (nombre, apellido, fecha_nacimiento, sexo) VALUES (%s, %s, %s, %s)',
        (nombre,apellido,fecha_nacimiento,sexo))
        mysql.connection.commit()
        flash('Alumno agregado')
        return redirect(url_for('Index'))

@app.route('/agregar_curso', methods=['POST'] )
def agregar_curso():
    if request.method == 'POST':
        nombre= request.form['nombre']
        descripcion= request.form['descripcion']
        cur= mysql.connection.cursor()
        cur.execute('INSERT INTO cursos (nombre_curso, descripcion) VALUES (%s, %s)',
        (nombre,descripcion))
        mysql.connection.commit()
        flash('Curso agregado')
        return redirect(url_for('Index'))

@app.route('/edit/<id>')
def get_alumno(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM alumnos WHERE id = %s', (id))
    data= cur.fetchall()
    return render_template('edit-alumno.html', alumno = data[0])

def delete_alumno(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM alumnos WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Alumno borrado')
    return redirect(url_for('Index'))

@app.route('/update/<id>', methods = ['POST'])
def update_alumno(id):
    if request.method == 'POST':

        nombre= request.form['nombre']
        apellido= request.form['apellido']
        fecha_nacimiento= request.form['fecha_nacimiento']
        sexo= request.form['sexo']
        cur = mysql.connection.cursor()
        cur.execute("""        
            UPDATE alumnos
            SET nombre = %s,
                apellido = %s,
                fecha_nacimiento= %s,
                sexo = %s
            WHERE id = %s
        """, (nombre,apellido,fecha_nacimiento,sexo,id))
        mysql.connection.commit()
        flash('Datos del alumno modificados')
        return redirect(url_for('Index'))
        

"""
   POR COMPLETAR 

@app.route('/notas', methods=['GET', 'POST'])
def ingresar_notas():
    if request.method == 'POST':

        id_curso = int(request.form['curso'])
        nota1 = float(request.form['nota1'])
        nota2 = float(request.form['nota2'])
        nota3 = float(request.form['nota3'])


        promedio = (nota1 + nota2 + (nota3)*2) / 4

       
        cur = mysql.connection.cursor()
        
        cur.execute("INSERT INTO notas (id_alumno, id_curso, nota1, nota2, nota3, promediofinal) VALUES (?, ?, ?, ?, ?, ?)",
                    (id_alumno, id_curso, nota1, nota2, nota3, promedio))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('Index', id=id_alumno))

    else:
        
        cur = mysql.connection.cursor()
        cursos = cur.execute("SELECT * FROM cursos").fetchall()
        cur.close()

        return render_template('ingresar-notas.html', cursos=cursos)
    """
if __name__ == '__main__':
    app.run(port= 3000, debug = True)
