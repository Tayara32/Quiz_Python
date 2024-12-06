import sqlite3
import pandas as pd

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

questions = []

def random_perguntas():
    global questions
    cursor.execute("SELECT * FROM questions ORDER BY RANDOM() LIMIT 10")
    questions = cursor.fetchall()

def top_scores():
    cursor.execute("SELECT name, score FROM users ORDER BY score DESC LIMIT 5")
    top_utilizadores = cursor.fetchall()
    df = pd.DataFrame(top_utilizadores, columns=['name', 'score'])
    df.to_csv('top_scores.csv', index=False)
    return top_utilizadores
