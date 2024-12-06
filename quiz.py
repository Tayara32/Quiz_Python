import pandas as pd
import tkinter as tk
import sqlite3
import db


pontuacao_atual = 0
questao_index = 0
temporizador = 15
temporizador_ativo = True

def inicio_jogo():
    global pontuacao_atual, questao_index, temporizador_ativo
    db.random_perguntas()
    pontuacao_atual = 0
    questao_index = 0
    label_question.pack(pady=10)
    list_options.pack()
    btn_submit.pack(pady=10)
    label_correct.pack_forget()
    btn_new_game.pack_forget()
    temporizador_ativo = True
    gerar_questao()
    atualizar_temporizador()
    label_melhores.pack_forget()
    lista_melhores.pack_forget()
    label_confirmacao.pack_forget()
    label_nome.pack_forget()
    label_pw.pack_forget()
    input_nome.pack_forget()
    input_pw.pack_forget()
    btn_guardar.pack_forget()


def atualizar_temporizador():
    global temporizador, temporizador_ativo

    if temporizador == 0:
        avancar_proxima_questao()

    if temporizador_ativo:
        label_timer.config(text=f"Segundos restantes: {temporizador}", font='Helvetica, 12')
        label_timer.pack()
        root.after(1000, atualizar_temporizador)
        temporizador -= 1


def gerar_questao():
    global pontuacao_atual, questao_index
    if questao_index < len(db.questions):
        questao = db.questions[questao_index]
        label_question.config(text=questao[0])
        list_options.delete(0, tk.END)
        list_options.insert(0, questao[1], questao[2], questao[3], questao[4])
    else:
        finalizar_quiz()

def avancar_proxima_questao():
    global questao_index, temporizador
    questao_index += 1
    temporizador = 15
    gerar_questao()

def verificar_resposta_correta():
    global pontuacao_atual, questao_index

    label_correct.pack()
    opcao_selecionada = list_options.curselection()

    if opcao_selecionada:
        indice_selecionado = opcao_selecionada[0]
        resposta_correta = db.questions[questao_index][5]
        if indice_selecionado == resposta_correta:
            pontuacao_atual += 1
            label_correct.config(text=f"Correto!\n A sua pontuação atual é de: {pontuacao_atual}", fg='green', font=('Helvetica', 10, 'bold'))
        else:
            label_correct.config(text=f"Errado! A resposta correta era {list_options.get(db.questions[questao_index][5])}.\n A sua pontuação atual é de: {pontuacao_atual}", fg='red', font=('Helvetica', 10, 'bold'))
        avancar_proxima_questao()
    else:
        label_correct.config(text="Escolha uma opção")


def finalizar_quiz():
    global temporizador_ativo
    label_question.config(text="CHEGOU AO FIM")
    label_correct.config(text=f"Sua pontuação final foi de: {pontuacao_atual}")
    btn_submit.pack_forget()
    btn_new_game.pack(pady=10)
    list_options.pack_forget()
    label_question.pack_forget()
    label_nome.pack()
    input_nome.pack(ipady=5, ipadx=5)
    label_pw.pack(pady=(10,0))
    input_pw.pack(ipady=5, ipadx=5)
    btn_guardar.pack(pady=10)
    temporizador_ativo = False
    label_timer.pack_forget()

def guardar_dados():
    nome = input_nome.get()
    pw = input_pw.get()

    if nome and pw:
        db.cursor.execute("SELECT * FROM users WHERE name = ? AND password = ?", (nome, pw))
        resultado = db.cursor.fetchone()
        if resultado:
            db.cursor.execute("UPDATE users SET score = score + ? WHERE id = ?", (pontuacao_atual, resultado[0]))
            db.conn.commit()
            label_confirmacao.config(text="Pontuação atualizada com sucesso!", fg="green")
        else:
            try:
                db.cursor.execute(
                    "INSERT INTO users (name, password, score) VALUES (?, ?, ?)",
                    (nome, pw, pontuacao_atual),
                )
                db.conn.commit()
                label_confirmacao.config(text="Pontuação salva com sucesso!", fg="green")
            except sqlite3.IntegrityError:
                label_confirmacao.config(text="Erro: Nome já existe!", fg="red")
    else:
        label_confirmacao.config(text="Preencha todos os campos!", fg="red")

    label_nome.pack_forget()
    input_nome.pack_forget()
    label_pw.pack_forget()
    input_pw.pack_forget()
    btn_guardar.pack_forget()
    label_confirmacao.pack()
    exibir_melhores_scores()

def exibir_melhores_scores():
    top_utilizadores = db.top_scores()
    label_melhores.config(text="TOP 5 Melhores Scores:")
    lista_melhores.delete(0, tk.END)
    for i, utilizador in enumerate(top_utilizadores, start=1):
        lista_melhores.insert(tk.END, f"{i}. {utilizador[0]} - {utilizador[1]} pontos")
    label_melhores.pack()
    lista_melhores.pack()


#INTERFACE GRÁFICA
root = tk.Tk()
root.configure(background='alice blue')
root.title('Quiz Genial')
root.geometry('600x400')
root.resizable(False, False)

label_title = tk.Label(root, text='Quiz Genial', font=('Helvetica', 20, 'bold'), fg='SlateBlue2', bg='alice blue')
label_title.pack(pady=5)
label_timer = tk.Label(root, bg='alice blue')
label_question = tk.Label(root, text='Question', bg='alice blue', font='Helvetica, 12')
list_options = tk.Listbox(root, bg='floral white', justify='center', font='Helvetica, 12', height=4, width=24)

btn_submit = tk.Button(root, text='Verificar', command=verificar_resposta_correta, background='SlateBlue2', fg='white', font=('Helvetica', 12, 'bold'))

label_correct = tk.Label(root, bg='alice blue')


btn_new_game = tk.Button(root, text='Novo Jogo', command=inicio_jogo, background='SlateBlue2', fg='white', font=('Helvetica', 12, 'bold'))
label_nome = tk.Label(root, text='Insira o seu username', bg='alice blue', font='Helvetica, 10')
input_nome = tk.Entry(root)
label_pw = tk.Label(root, text='Insira uma password', bg='alice blue', font='Helvetica, 10')
input_pw = tk.Entry(root, show='*')
btn_guardar = tk.Button(root, text='Guardar', command=guardar_dados, background='SlateBlue2', fg='white', font=('Helvetica', 12, 'bold'))
label_confirmacao = tk.Label(root, bg='alice blue', font='Helvetica, 10')

label_melhores = tk.Label(root, text="TOP 5 Usuários:", font=("Helvetica", 12, 'bold'), bg='alice blue')
lista_melhores = tk.Listbox(root, bg='floral white', justify='center', font='Helvetica, 12', height=4, width=24)

inicio_jogo()
root.mainloop()