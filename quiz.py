import pandas as pd
import tkinter as tk
import sqlite3

conn = sqlite3.connect('quiz.db')
cursor = conn.cursor()

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

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        score INTEGER DEFAULT 0
);
''')


dados = pd.read_csv('Docs/quiz-questions.csv')
dados.to_sql('questions', conn, if_exists='replace', index=False)

conn.commit()
conn.close()

#INTERFACE GRÁFICA
root = tk.Tk()
root.title('Quiz Genial')
root.geometry('500x500')
root.resizable(False, False)

label_title = tk.Label(root, text='Quiz Genial', font=('Helvetica', 16))
label_title.pack()
label_question = tk.Label(root, text='Question')
label_question.pack()

root.mainloop()



