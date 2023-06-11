from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# MYSQL CONNECTION
app.config['MYSQL_HOST'] = 'sql10.freesqldatabase.com'
app.config['MYSQL_USER'] = 'sql10625106'
app.config['MYSQL_PASSWORD'] = '8uUhtdb2hC'
app.config['MYSQL_DB'] = 'sql10625106'
mysql = MySQL(app)


# SETTINGS
app.secret_key = 'mysecret_key'

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM STG_PEDIDOS')
    data = cur.fetchall()
    cur.close()
    print(data)
    return render_template('index.html', pedidos=data)

@app.route('/add_pedido', methods=['POST'])
def add_pedido():
    if request.method == 'POST':
        pedido = request.form['pedido']
        producto = request.form['producto']
        camion = request.form['camion']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO STG_PEDIDOS (pedido, producto, camion) VALUES (%s, %s, %s)', (pedido, producto, camion))
        mysql.connection.commit()
        cur.close()
        flash('Pedido Agregado Successfully')
        return redirect(url_for('index'))
    else:
        return 'Invalid request'

@app.route('/edit/<int:id>')
def edit_pedido(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM STG_PEDIDOS WHERE id = %s', (id,))
    data = cur.fetchone()
    cur.close()
    if data:
        pedido = {
            'id': data[0],
            'pedido': data[1],
            'producto': data[2],
            'camion': data[3]
        }
        return render_template('edit_pedido.html', pedido=pedido)
    else:
        flash('Pedido no encontrado')
        return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['POST'])
def update_pedido(id):
    if request.method == 'POST':
        pedido = request.form['pedido']
        producto = request.form['producto']
        camion = request.form['camion']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE STG_PEDIDOS
            SET pedido = %s,
                producto = %s,
                camion = %s
            WHERE id = %s
        """, (pedido, producto, camion, id))
        mysql.connection.commit()
        cur.close()
        flash('Pedido Actualizado')
        return redirect(url_for('index'))

@app.route('/delete/<string:id>')
def delete_pedido(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM STG_PEDIDOS WHERE id = %s', (id,))
    mysql.connection.commit()
    cur.close()
    flash('Pedido removido correctamente')
    return redirect(url_for('index'))

@app.route('/approve/', methods=['POST'])
def approve_pedidos():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO STG_PEDIDOS_FINAL (pedido, producto, camion)
            SELECT pedido, producto, camion
            FROM STG_PEDIDOS
        """)
        mysql.connection.commit()
        cur.close()
        flash('Se liberaron todos los pedidos')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port=3003, debug=True)
