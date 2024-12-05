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
    opcao_selecionada = list_options.curselection()
    resposta_correta = questions[questao_index][5]
    if opcao_selecionada == resposta_correta:
        pontuacao_atual += 1
        label_correct.config(text=f"Acertou Miserável! Sua pontuação atual é de: {pontuacao_atual}")
    else:
        label_correct.config(text=f"Errou Miserável! Sua pontuação atual é de: {pontuacao_atual}")

    questao_index += 1
    gerar_questao()

def finalizar_quiz():
    label_question.config(text="CHEGOU AO FIM")
    label_correct.config(text=f"Sua pontuação final foi de: {pontuacao_atual}")


#INTERFACE GRÁFICA
root = tk.Tk()
root.title('Quiz Genial')
root.geometry('500x500')
root.resizable(False, False)

label_title = tk.Label(root, text='Quiz Genial', font=('Helvetica', 16))
label_title.pack()
label_question = tk.Label(root, text='Question')
label_question.pack(pady=10)

list_options = tk.Listbox(root)
list_options.pack()

btn_submit = tk.Button(root, text='Submit', command=verificar_resposta_correta)
btn_submit.pack()

label_correct = tk.Label(root)
label_correct.pack()


gerar_questao()
root.mainloop()



