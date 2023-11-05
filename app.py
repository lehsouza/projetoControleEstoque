from flask import Flask, render_template, request, redirect, flash
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '1234'
app.config['MYSQL_DATABASE_DB'] = 'estoquedb'
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'

mysql.init_app(app)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'senha_secreta'

@app.route('/')
def main():
     return render_template('index.html')

@app.route('/', methods=['POST'])
def cadastrar():
    nomeProduto = request.form.get('nome')
    fabricante = request.form.get('fabricante')
    quantidade = request.form.get('quantidade')

    if nomeProduto and fabricante and quantidade:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('insert into produto(Codigo, Nome, Quantidade, Fornecedor) VALUES (null,%s, %s, %s)', (nomeProduto, quantidade, fabricante))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Cadastro realizado com sucesso!', 'sucesso')
        return redirect('/')
    else:
        flash('Erro - Informações preenchidas incorretamente.', 'error')
        return redirect('/')
    
@app.route('/listar', methods=['GET'])
def listar():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('select Codigo, Nome, Fornecedor, Quantidade from produto')
    lista = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return render_template('lista.html', listas=lista)

@app.route('/deletar/<int:Codigo>', methods = ['GET'])
def deletar(Codigo):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM produto WHERE codigo=%s', (Codigo))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/listar')

if __name__ == "__main__":
    app.run(debug=True)