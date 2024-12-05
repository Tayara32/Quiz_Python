from random import random

import pandas as pd
import tkinter as tk
import sqlite3

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

cursor.execute("SELECT * FROM questions ORDER BY RANDOM() LIMIT 10")
questions = cursor.fetchall()
conn.commit()
conn.close()

#FUNÇÕES

pontuacao_atual = 0
questao_index = 0

def inicio_jogo():
    gerar_questao()
    label_question.pack(pady=10)
    list_options.pack()
    btn_submit.pack()


def gerar_questao():
    global pontuacao_atual, questao_index
    if questao_index < len(questions):
        questao = questions[questao_index]
        label_question.config(text=questao[0])
        list_options.delete(0, tk.END)
        list_options.insert(0, questao[1], questao[2], questao[3], questao[4])
    else:
        finalizar_quiz()

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
            label_correct.config(text=f"Errou Miserável! Sua pontuação atual é de: {pontuacao_atual}")
        questao_index += 1
        gerar_questao()
    else:
        label_correct.config(text="Escolha uma opção")



def finalizar_quiz():
    label_question.config(text="CHEGOU AO FIM")
    label_correct.config(text=f"Sua pontuação final foi de: {pontuacao_atual}")
    btn_submit.pack_forget()
    btn_new_game.pack()
    list_options.pack_forget()
    label_question.pack_forget()


#INTERFACE GRÁFICA
root = tk.Tk()
root.title('Quiz Genial')
root.geometry('500x500')
root.resizable(False, False)

label_title = tk.Label(root, text='Quiz Genial', font=('Helvetica', 16))
label_title.pack()
label_question = tk.Label(root, text='Question')
list_options = tk.Listbox(root)

btn_submit = tk.Button(root, text='Submit', command=verificar_resposta_correta)

label_correct = tk.Label(root)


btn_new_game = tk.Button(root, text='Novo Jogo', command=inicio_jogo)

inicio_jogo()
root.mainloop()



