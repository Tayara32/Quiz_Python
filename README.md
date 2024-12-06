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
O projeto está estruturado de forma a separar a lógica da base de dados da lógica do jogo, para que a manutenção e escalabilidade
do código seja facilitada.

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
   - Foi implementado um temporizador de 15 segundos para controlar o tempo que os utilizadores tem disponível para responder cada pergunta.
   - O temporizador é implementado através da função `atualizar_temporizador()`, que atualiza a interface gráfica com o tempo, em contagem decrescente, que o utilizador ainda tem disponível.
   - Quando o tempo atingido for zero a função `avancar_proxima_questao()` é chamada e automaticamente avança para a próxima questão.
   - As variáveis relacionadas ao temporizador são: `temporizador`, que determina, em segundos, o tempo para cada questão e a variável `temporizador_ativo()` controla se o temporizador esta ativo e a contar o tempo ou inativo.
   
3. Base de Dados
   - As tabelas foram criadas através de comandos `SQL` e executados através do objeto `cursor`.
   - Foram criadas duas tabelas : `questions` -> armazena as questões, opções e alternativa correta e `users` -> armazena nome, palavra-passe e suas respetivas pontuações.
   - As questões são carregadas de um arquivo `csv` para a tabela `questions` através do método `to_sql` do pandas.
   - Foi utilizado o `SQLite` que é uma base de dados que armazena os dados num único ficheiro, neste caso denominado `quiz.db`.

4. Lista de melhores Scores
   - Através da consulta dos 5 melhores utilizadores na tabela `users` na base de dados será exibido um ranking.
   - Essa consulta irá retornar  um tuplo nome e pontuação, através do método `fetchall` que será armazenado na variável `top_utilizadores`.
   - A função `exibir_melhores_utilizadores()` será chamada na função `salvar_dados()`para que o resultado seja exibido após inserção do novo utilizador à base de dados.

5. Exportação de Resultados
   - Os dados obtidos obtidos através da função `exibir_melhores_utilizadores()` são guardados num ficheiro `csv` denominado `top_scores.csv`, que é atualizado sempre que o utilizador guarda os seus dados.

---
## Conclusão
O projeto oferece uma experiência interativa e divertida e demonstra como pode ser feita a integração entre interface gráfica e base de dados. Ao utilizar bibliotecas como `Tkinter`, `sqlite3` e `pandas`, foi possível criar esse jogo de perguntas e respostas, com temporizador e que armazena os dados dos jogadores em uma base de dados. De forma que os alunos puderam melhorar as habildiades em programação Python, design de interfaces gráficas e manipulação de dados.

---