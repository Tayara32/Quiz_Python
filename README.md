# Quiz Genial com Python

**Versão:** v1.0  
**Autores:** Beatriz Guerra, Pedro Pires e Tayara Cruz  
**Formador:** Nelson Santos   
**Data:** Dezembro, 2024  
**UFCD:** 5417 - Programação para a WEB - servidor (server-side)   
**Instituição:** ATEC

---
## Descrição do Projeto
Este projeto foi solicitado como uma forma prática de aplicar os conhecimentos adquiridos na unidade formativa UFCD 5417. 
O objetivo principal é compreender e fazer uso das bibliotecas `Tkinter` para criação de interfaces gráficas simples 
e intuitivas, `sqlite3` para conexão com base de dados, e o `pandas` para leituras de ficheiros `.csv`.

---
## Tecnologias Utilizadas
- Python: Linguagem de desenvolvimento
- Tkinter: Interface gráfica
- SQLite: Base de dados para armazenamento de perguntas e utilizadores
- Pandas: Manipulação de dados csv para inserção na base de dados

---
## Funcionalidades Implementadas
1. Quiz
    - Gerar perguntas através de uma função denominada `random_perguntas()` que gera 10 questões aleatórias daquelas presentes na tabela `questions` da BD, e é carregada ao iniciar o jogo.
    - Para iniciar o jogo, é chamada a função `inicio_jogo()`, que também controla a interface gráfica, alterando a visibilidade dos widgets da biblioteca `Tkinter` conforme necessário.
    - Para exibir cada pergunta e respetivas opções, é utilizada a função `gerar_questao()`, que, permite que o utilizador selecione uma opção da `ListBox`.
    - Para verificar se a opção selecionada está correta, o evento `command` no botão Verificar chama a função `verificar_resposta_correta()`. Após verificação, é atualizada a pontuação e apresentada uma mensagem apropriada, bem como a pontuação atual.
    - Após a verificação, é chamada a função `avancar_proxima_questao()`, até que as 10 questões geradas inicialmente sejam respondidas.
    - Ao finalizar as 10 questões, o quiz termina e permite que o utilizador inicie um novo jogo, com novas perguntas e/ou guarde os seus dados na base de dados.

2. Temporizador
   - 