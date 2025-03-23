from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mysqldb import MySQL
import bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
CORS(app)  # Permite requisições do frontend

# Configuração do MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Welcome@ads'
app.config['MYSQL_DB'] = 'cad_veiculos'
app.config['JWT_SECRET_KEY'] = 'chave_secreta'

mysql = MySQL(app)
jwt = JWTManager(app)

# Rota para obter usuários
@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, Modelo, Número Chassi, Fabricante, Cor, Número Placa, Número Motor, Pesso Liquido, Pesso Bruto, Número de Cavalos, Tipo de Combustivel, Números de Cilindros FROM veiculos")
    users = cur.fetchall()
    cur.close()
    
    return jsonify([{"id": u[0], "Modelo": u[1], "Número Chassi": u[2], "Fabricante": u[3], "Número Placa": u[4], "Número Motor": u[5], "Pesso Liquido": u[6], "Pesso Bruto": u[7], "Número de Cavalos": u[8], "Tipo de Combustivel": u[9], "Números de Cilindros": u[10]} for u in users])

# Rota para cadastro de usuários
@app.route('/registro', methods=['POST'])
def register():
    data = request.get_json()
    id_veiculo = data['ID']
    modelo = data['Modelo']
    num_chassi = data['Número Chassi']
    fabricante = data['Fabricante']
    cor = data['Cor']
    num_placa = data['Número Placa']
    num_motor = data['Número Motor']
    pesso_liquido = data['Pesso Liquido']
    pesso_bruto = data['Pesso Bruto']
    cavalos = data['Número de Cavalos']
    tipo_combustivel = data['Tipo de Combustivel']
    cilidros = data['Números de Cilindros']

    #senha = bcrypt.hashpw(data['senha'].encode('utf-8'), bcrypt.gensalt())

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO (ID, Modelo, Número Chassi, Fabricante, Cor, Número Placa, Número Motor, Pesso Liquido, Pesso Bruto, Número de Cavalos, Tipo de Combustivel, Números de Cilindros) VALUES (%s, %s, %s, %s, %s)", (id_veiculo, modelo, num_chassi, fabricante, cor, num_placa, num_motor, pesso_liquido, pesso_bruto, cavalos, tipo_combustivel, cilidros  ))
    mysql.connection.commit()
    cur.close()

    return jsonify({"mensagem": "Veiculo cadastrado com sucesso!"})

# Rota de login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    senha = data['senha'].encode('utf-8')

    cur = mysql.connection.cursor()
    cur.execute("SELECT id, nome, senha FROM usuarios WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()

    if user and bcrypt.checkpw(senha, user[2].encode('utf-8')):
        token = create_access_token(identity={"id": user[0], "nome": user[1]})
        return jsonify({"token": token})
    return jsonify({"erro": "Credenciais inválidas"}), 401

# Rota protegida para testar autenticação
@app.route('/perfil', methods=['GET'])
@jwt_required()
def perfil():
    usuario = get_jwt_identity()
    return jsonify({"mensagem": f"Bem-vindo, {usuario['nome']}!"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
