from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
import bcrypt

app = Flask(__name__)
CORS(app)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5500"}})

# Configurações de conexão
db_config = {
    'host': 'mysql-d30b100-gustavocnc.d.aivencloud.com',
    'user': 'avnadmin',
    'password': 'AVNS_QqNp6z-f2Lk7STAgZLH',
    'database': 'projetofaculdade',
    'port': 17859
}

def create_connection():
    """Estabelece a conexão com o banco de dados e retorna a conexão."""
    try:
        connection = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database'],
            port=db_config['port']
        )
        if connection.is_connected():
            print("Conexão bem-sucedida ao MySQL!")
            return connection
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None

def check_password(stored_password, provided_password):
    """Verifica se a senha fornecida corresponde ao hash armazenado."""
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))

@app.route('/login', methods=['POST'])
def login():
    """Verifica as credenciais do usuário e retorna um token de autenticação ou mensagem de erro."""
    user_data = request.get_json()
    
    # Verifica se os campos obrigatórios estão presentes
    if not user_data or 'email' not in user_data or 'senha' not in user_data:
        return jsonify({"message": "Email e senha são obrigatórios"}), 400
    
    email = user_data['email']
    senha = user_data['senha']
    
    try:
        connection = create_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Usuario WHERE Email = %s", (email,))
            user = cursor.fetchone()
            
            # Adiciona mensagem de depuração
            print(f"Usuário encontrado: {user}")
            
            if user and check_password(user['Senha'], senha):
                return jsonify({"message": "Login bem-sucedido!"}), 200
            else:
                return jsonify({"message": "Credenciais inválidas"}), 401
        else:
            return jsonify({"message": "Erro ao conectar ao banco de dados"}), 500
    except Error as e:
        print(f"Erro ao verificar credenciais: {e}")
        return jsonify({"message": f"Erro ao verificar credenciais: {str(e)}"}), 500
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/register', methods=['POST'])
def register():
    """Cadastra um novo usuário no sistemas."""
    user_data = request.json
    
    # Validação de entrada
    if not user_data or not user_data.get('nome') or not user_data.get('email') or not user_data.get('senha'):
        return jsonify({"message": "Nome, email e senha são obrigatórios"}), 400
    
    nome = user_data['nome']
    email = user_data['email']
    senha = user_data['senha']
    
   
    
    try:
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            
            # Verifica se o usuário já existe
            cursor.execute("SELECT * FROM Usuario WHERE Email = %s", (email,))
            user = cursor.fetchone()
            
            if user:
                return jsonify({"message": "Usuário já existe com esse email"}), 409
            
            # Insere o novo usuário no banco de dados
            insert_query = """
                INSERT INTO Usuario (Nome, Email, Senha) 
                VALUES (%s, %s, %s)
            """
            connection.commit()
            
            return jsonify({"message": "Usuário cadastrado com sucesso!"}), 201
        else:
            return jsonify({"message": "Erro ao conectar ao banco de dados"}), 500
    except Error as e:
        print(f"Erro ao cadastrar usuário: {e}")
        return jsonify({"message": "Erro ao cadastrar usuário"}), 500
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            
@app.route('/users', methods=['GET'])
def get_users():
    """Retorna todos os usuários ou um usuário específico baseado no ID fornecido."""
    user_id = request.args.get('id')
    
    try:
        connection = create_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            
            if user_id:
                # Consulta para um usuário específico
                cursor.execute("SELECT * FROM Usuario WHERE ID = %s", (user_id,))
            else:
                # Consulta para todos os usuários
                cursor.execute("SELECT * FROM Usuario")
            
            users = cursor.fetchall()
            
            if users:
                return jsonify(users), 200
            else:
                return jsonify({"message": "Nenhum usuário encontrado"}), 404
        else:
            return jsonify({"message": "Erro ao conectar ao banco de dados"}), 500
    except Error as e:
        print(f"Erro ao consultar usuários: {e}")
        return jsonify({"message": f"Erro ao consultar usuários: {str(e)}"}), 500
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            
            
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
