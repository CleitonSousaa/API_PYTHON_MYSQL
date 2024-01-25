from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'postapp',
}

def obter_cursor():
    conn = mysql.connector.connect(**db_config)
    return conn, conn.cursor()




@app.route('/api/dados', methods=['GET'])
def obter_dados():
    _, cursor = obter_cursor()
    cursor.execute('SELECT * FROM postagens')
    dados = cursor.fetchall()
    colunas = [i[0] for i in cursor.description]
    resultado = []
    for row in dados:
        resultado.append(dict(zip(colunas, row)))
    return jsonify(resultado)


@app.route('/api/inserir_dados', methods=['POST'])
def inserir_dados():
    _, cursor = obter_cursor()
    dados_json = request.get_json()
    campos = ', '.join(dados_json.keys())
    valores = ', '.join(['%s'] * len(dados_json))
    consulta = f"INSERT INTO postagens ({campos}) VALUES ({valores})"
    cursor.execute(consulta, tuple(dados_json.values()))
    conn.commit()
    return jsonify({'mensagem': 'Dados inseridos com sucesso!'})


@app.route('/api/atualizar_dados/<int:id>', methods=['PUT'])
def atualizar_dados(id):
    conn, cursor = obter_cursor()
    dados_json = request.get_json()
    campos_para_atualizar = ', '.join([f"{campo} = %s" for campo in dados_json.keys()])
    consulta = f"UPDATE postagens SET {campos_para_atualizar} WHERE id = %s"
    cursor.execute(consulta, tuple(dados_json.values()) + (id,))
    conn.commit()
    return jsonify({'mensagem': 'Dados atualizados com sucesso!'})


@app.route('/api/excluir_dados/<int:id>', methods=['DELETE'])
def excluir_dados(id):
    conn, cursor = obter_cursor()
    consulta = "DELETE FROM postagens WHERE id = %s"
    cursor.execute(consulta, (id,))
    conn.commit()
    return jsonify({'mensagem': 'Dados excluídos com sucesso!'})

if __name__ == '__main__':
    app.run(debug=True)
