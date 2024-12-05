from random import random
import pandas as pd
import tkinter as tk
import sqlite3
from tkinter import messagebox
import time

#CONEXÃO AO BANCO DE DADOS
conn = sqlite3.connect('quiz.db')
cursor = conn.cursor()

#TABELA QUESTIONS
cursor.execute('''
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        option1 TEXT NOT NULL,
        option2 TEXT NOT NULL,
        option3 TEXT NOT NULL,
        option4 TEXT NOT NULL,
        correct INTEGER NOT NULL
);
''')

#TABELA USERS
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        score INTEGER DEFAULT 0
);
''')

#LER CSV E INSERIR DADOS NA TABELA
dados = pd.read_csv('Docs/quiz-questions.csv')
dados.to_sql('questions', conn, if_exists='replace', index=False)

#FUNÇÕES

def random_perguntas():
    global questions
    cursor.execute("SELECT * FROM questions ORDER BY RANDOM() LIMIT 10")
    questions = cursor.fetchall()

questions = []
pontuacao_atual = 0
questao_index = 0
temporizador = 15
temporizador_ativo = True

def inicio_jogo():
    global pontuacao_atual, questao_index
    pontuacao_atual = 0
    questao_index = 0
    random_perguntas()
    label_question.pack(pady=10)
    list_options.pack()
    btn_submit.pack()
    label_correct.pack_forget()
    btn_new_game.pack_forget()
    gerar_questao()
    atualizar_temporizador()

def atualizar_temporizador():
    global temporizador, temporizador_ativo
    if temporizador > 0 and temporizador_ativo:
        label_timer.config(text=f"Segundos restantes: {temporizador}")
        label_timer.pack()
        temporizador -= 1
        root.after(1000, atualizar_temporizador)
    elif temporizador == 0:
        avancar_proxima_questao()


def gerar_questao():
    global pontuacao_atual, questao_index
    if questao_index < len(questions):
        questao = questions[questao_index]
        label_question.config(text=questao[0])
        list_options.delete(0, tk.END)
        list_options.insert(0, questao[1], questao[2], questao[3], questao[4])
    else:
        finalizar_quiz()

def avancar_proxima_questao():
    global questao_index, temporizador
    questao_index += 1
    temporizador = 15
    atualizar_temporizador()
    gerar_questao()

def verificar_resposta_correta():
    global pontuacao_atual, questao_index

    label_correct.pack()
    opcao_selecionada = list_options.curselection()

    if opcao_selecionada:
        indice_selecionado = opcao_selecionada[0]
        resposta_correta = questions[questao_index][5]
        if indice_selecionado == resposta_correta:
            pontuacao_atual += 1
            label_correct.config(text=f"Acertou Miserável! Sua pontuação atual é de: {pontuacao_atual}")
        else:
            label_correct.config(text=f"Errou Miserável! A resposta correta era {list_options.get(questions[questao_index][5])}. Sua pontuação atual é de: {pontuacao_atual}")
        avancar_proxima_questao()
    else:
        label_correct.config(text="Escolha uma opção")



def finalizar_quiz():
    global temporizador_ativo
    label_question.config(text="CHEGOU AO FIM")
    label_correct.config(text=f"Sua pontuação final foi de: {pontuacao_atual}")
    btn_submit.pack_forget()
    btn_new_game.pack()
    list_options.pack_forget()
    label_question.pack_forget()
    label_nome.pack()
    input_nome.pack()
    label_pw.pack()
    input_pw.pack()
    btn_guardar.pack()
    temporizador_ativo = False
    label_timer.pack_forget()

def guardar_dados():
    nome = input_nome.get()
    pw = input_pw.get()

    if nome and pw:
        cursor.execute("SELECT * FROM users WHERE name = ? AND password = ?", (nome, pw))
        resultado = cursor.fetchone()
        if resultado:
            cursor.execute("UPDATE users SET score = score + ? WHERE id = ?", (pontuacao_atual, resultado[0]))
            conn.commit()
            label_confirmacao.config(text="Pontuação atualizada com sucesso!", fg="green")
        else:
            try:
                cursor.execute(
                    "INSERT INTO users (name, password, score) VALUES (?, ?, ?)",
                    (nome, pw, pontuacao_atual),
                )
                conn.commit()
                label_confirmacao.config(text="Pontuação salva com sucesso!", fg="green")
            except sqlite3.IntegrityError:
                label_confirmacao.config(text="Erro: Nome já existe!", fg="red")
    else:
        label_confirmacao.config(text="Preencha todos os campos!", fg="red")

    label_confirmacao.pack()



#INTERFACE GRÁFICA
root = tk.Tk()
root.title('Quiz Genial')
root.geometry('500x500')
root.resizable(False, False)

label_title = tk.Label(root, text='Quiz Genial', font=('Helvetica', 16))
label_title.pack()
label_timer = tk.Label(root)
label_question = tk.Label(root, text='Question')
list_options = tk.Listbox(root)

btn_submit = tk.Button(root, text='Verificar', command=verificar_resposta_correta)

label_correct = tk.Label(root)


btn_new_game = tk.Button(root, text='Novo Jogo', command=inicio_jogo)
label_nome = tk.Label(root, text='Insira o seu username')
input_nome = tk.Entry(root)
label_pw = tk.Label(root, text='Insira uma password')
input_pw = tk.Entry(root, show='*')
btn_guardar = tk.Button(root, text='Guardar', command=guardar_dados)
label_confirmacao = tk.Label(root)

inicio_jogo()
root.mainloop()



