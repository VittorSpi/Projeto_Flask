import os
import csv
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)


os.environ['FLASK_DEBUG'] = 'True'

app.debug = os.environ.get('FLASK_DEBUG') == 'True'

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/sobre')
def sobre():
    return render_template('sobre.html')


@app.route('/glossario')
def glossario():

    glossario_de_termos = []

    # abre o arquivo .csv usando o "arquivo" e não o código
    with open(
            'bd_glossario.csv',
            newline='', encoding='utf-8') as arquivo:
        reader = csv.reader(arquivo, delimiter=';')
        for l in reader:
            glossario_de_termos.append(l)

    # o glossario_de_termos vai ser chamado como "glossario" no html
    return render_template('glossario.html',
                           glossario=glossario_de_termos)


@app.route('/novo_termo')
def novo_termo():
    return render_template('adicionar_termo.html')


@app.route('/criar_termo', methods=['POST', ])
def criar_termo():
    # usa request.form para pegar o name="" que está no form do html
    termo = request.form['termo']
    definicao = request.form['definicao']

    with open(
            'bd_glossario.csv', 'a',
            newline='', encoding='utf-8') as arquivo:
        writer = csv.writer(arquivo, delimiter=';')
        # escreve termo;definicao no arquivo .csv
        writer.writerow([termo, definicao])

    return redirect(url_for('glossario'))


@app.route('/editar_termo/<int:termo_id>')
def editar_termo(termo_id):
    with open('bd_glossario.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        # o arquivo .csv vira uma lista
        linhas = list(reader)

    # verifica se o termo está dentro da lista "linhas" através do termo_id
    if termo_id < len(linhas):
        termo = linhas[termo_id][0]
        definicao = linhas[termo_id][1]
        return render_template('editar_termo.html', termo=termo, definicao=definicao, termo_id=termo_id)
    else:
        return redirect(url_for('glossario'))

@app.route('/atualizar_termo/<int:termo_id>', methods=['POST'])
def atualizar_termo(termo_id):
    novo_termo = request.form['novo_termo']
    nova_definicao = request.form['nova_definicao']

    # lê o arquivo .csv
    with open('bd_glossario.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        linhas = list(reader)

    #atualiza o termo puxando os novos valores das variáveis novo_termo/nova_definicao
    if termo_id < len(linhas):
        linhas[termo_id][0] = novo_termo
        linhas[termo_id][1] = nova_definicao

        # escreve o termo atualizado no arquivo .csv
        with open('bd_glossario.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerows(linhas)

    return redirect(url_for('glossario'))



@app.route('/excluir_termo/<int:termo_id>', methods=['POST'])
def excluir_termo(termo_id):

    with open('bd_glossario.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        linhas = list(reader)

    # estrutura do enumerate --> enumerate(indice, valor)
    for i, linha in enumerate(linhas):
        if i == termo_id:
            del linhas[i]
            break

    # atualiza a lista sem o termo excluído
    with open('bd_glossario.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(linhas)

    return redirect(url_for('glossario'))


#LISTA DE TAREFAS

@app.route('/lista')
def lista():
    lista_de_tarefas = []

    with open('bd_lista.csv', newline='', encoding='utf-8') as arquivo:
        reader = csv.reader(arquivo, delimiter=';')
        for l in reader:
            lista_de_tarefas.append(l)

    return render_template('lista.html', lista=lista_de_tarefas)

@app.route('/nova_tarefa')
def nova_tarefa():
    return render_template('adicionar_tarefa.html')

@app.route('/criar_tarefa', methods=['POST'])
def criar_tarefa():
    tarefa = request.form['tarefa']

    with open('bd_lista.csv', 'a', newline='', encoding='utf-8') as arquivo:
        writer = csv.writer(arquivo, delimiter=';')
        writer.writerow([tarefa, 'pendente'])

    return redirect(url_for('lista'))

@app.route('/editar_tarefa/<int:tarefa_id>')
def editar_tarefa(tarefa_id):
    with open('bd_lista.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        linhas = list(reader)

    if tarefa_id < len(linhas):
        tarefa = linhas[tarefa_id][0]
        return render_template('editar_tarefa.html', tarefa=tarefa, tarefa_id=tarefa_id)
    else:
        return redirect(url_for('lista'))

@app.route('/atualizar_tarefa/<int:tarefa_id>', methods=['POST'])
def atualizar_tarefa(tarefa_id):
    nova_tarefa = request.form['nova_tarefa']

    with open('bd_lista.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        linhas = list(reader)

    if tarefa_id < len(linhas):
        linhas[tarefa_id][0] = nova_tarefa

        with open('bd_lista.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerows(linhas)

    return redirect(url_for('lista'))

@app.route('/excluir_tarefa/<int:tarefa_id>', methods=['POST'])
def excluir_tarefa(tarefa_id):
    with open('bd_lista.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        linhas = list(reader)

    if tarefa_id < len(linhas):
        del linhas[tarefa_id]

        with open('bd_lista.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerows(linhas)

    return redirect(url_for('lista'))

@app.route('/marcar_completa/<int:tarefa_id>')
def marcar_completa(tarefa_id):
    with open('bd_lista.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        linhas = list(reader)

    # se tarefa_id estiver dentro dos limites, o código altera o status da tarefa para 'completa' na lista "linhas"
    if tarefa_id < len(linhas):
        linhas[tarefa_id][1] = 'completa'
        # tarefa; que se torna tarefa;completa

        with open('bd_lista.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerows(linhas)

    return redirect(url_for('lista'))

if __name__ == "__main__":
    app.run()
