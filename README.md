# MorseScript - Interpretador de mensagens em Código Morse


## Integrantes do grupo:

| ALUNO | MATRÍCULA | TURMA |
| :--- | :--- | :--- |
| Henrique Galdino Couto | 200058258 | 18h |
| Igor Thiago Lima de Santana | 190029692 | 18h |
| Rodrigo Braz Ferreira Gontijo | 190116498 | 16h |
| Thales Germano Vargas Lima | 202017147 | 18h |


## Introdução
Este projeto é um interpretador para a linguagem de domínio específico "MorseScript", desenvolvida para o trabalho final da disciplina de Compiladores.

A linguagem permite criar scripts para controlar transmissões em Código Morse, definindo velocidade, pausas e repetições nas mensagens a serem codificadas em código Morse.

### Estrutura do Código

O projeto está dividido em quatro códigos, que representam as partes de um compilador/interpretador:

* **`morsescript/lexer.py`**: O **Analisador Léxico**, responsável por transformar o código fonte em uma sequência de tokens.
* **`morsescript/parser.py`**: O **Analisador Sintático**, que recebe os tokens e constrói uma Árvore de Sintaxe Abstrata (AST) para representar a estrutura do programa.
* **`morsescript/interpreter.py`**: O **Interpretador**, que percorre a AST (usando o padrão de projeto Visitor) e executa os comandos, realizando a "transmissão" em modo texto no console.
* `morsescript/__main__.py`: Este arquivo funciona como o **ponto de entrada (Entry Point)** da aplicação quando ela é executada como um módulo (`python -m morsescript`). 

### Linguagem MorseScript

A linguagem possui os seguintes comandos:

* `TEXTO "mensagem"`: Inicia a transmissão da mensagem em Morse.
* `VELOCIDADE x`: Ajusta a velocidade em Words per Minute/WPM (Palavras Por Minuto).
* `PAUSA x`: Pausa a execução por `x` milissegundos.
* `REPITA numero [ ... ]`: Repete um bloco de comandos.
* `// comentario`: Comentários precedidos por `//` são ignorados.

### Exemplo

#### Exemplo  de código .morse
```
// Define a velocidade de transmissão em 20 palavras por minuto.
VELOCIDADE 20

// Texto contendo mensagem.
TEXTO "OLA MUNDO EM MORSE"

// Pausa por 2 segundos antes da mensagem final.
PAUSA 2000

// Mensagem final.
TEXTO "FIM"
```

#### Exemplo de saída no console
```
[CONFIG: Velocidade ajustada para 20 WPM]

Transmitindo: "OLA MUNDO EM MORSE"
--- .-.. .-   /  -- ..- -. -.. ---   /  . --   /  -- --- .-. ... . 
[TRANSMISSÃO COMPLETA]

[PAUSA: 2.00 segundos...]

Transmitindo: "FIM"
..-. .. -- 
[TRANSMISSÃO COMPLETA]
```

## Limitações


### Limitações da Linguagem (MorseScript)

As principais limitações residem na expressividade da própria linguagem, que foi mantida intencionalmente simples.

1.  **Ausência de Variáveis:** A linguagem não possui um sistema de variáveis. Todos os valores, como a duração de uma `PAUSA` ou a mensagem de um `TEXTO`, devem ser escritos diretamente no código ("hardcoded"). Isso impede o armazenamento de resultados ou a criação de scripts que se adaptam dinamicamente.

2.  **Falta de Estruturas de Controle Condicionais:** Não existe um comando como `SE` (ou `IF`). É impossível tomar decisões com base em algum estado ou condição imposta pelo usuário. Por exemplo, não é possível fazer algo como: `SE VELOCIDADE > 30 [ TEXTO "MUITO RAPIDO" ]`.

3.  **Inexistência de Abstrações do Usuário (Funções/Procedimentos):** O usuário não pode agrupar uma série de comandos em uma função ou procedimento reutilizável. Se uma mesma sequência complexa de `TEXTO` e `PAUSA` for necessária em vários pontos do script, ela deve ser copiada e colada, levando à repetição de código.

4.  **Sem Operações Aritméticas:** Os valores numéricos não podem ser resultado de expressões. Por exemplo, não é possível escrever `VELOCIDADE 20 + 5` ou `PAUSA 1000 * 3`. O valor final deve ser calculado previamente e inserido diretamente no comando.

### Limitações do Interpretador

As limitações da implementação estão relacionadas a como o código é executado e como os erros são tratados.

1.  **Tratamento de Erros Simplificado:** O tratamento de erros é rudimentar. Quando um erro léxico (caractere inválido) ou sintático (comando malformado) é encontrado, o programa simplesmente para a execução e exibe uma mensagem de erro genérica. O sistema não informa o **número da linha e da coluna** onde o erro ocorreu, o que torna a depuração de scripts mais longos um processo manual e demorado.

2.  **Interpretador Puro, Sem Otimizações:** O interpretador executa a Árvore de Sintaxe Abstrata (AST) diretamente, indo de nó a nó, sem que haja alguma otimização.

### Limitações de Interatividade

1.  **Execução Apenas via Arquivo:** O programa foi projetado para ler e executar arquivos `.morse` a partir da linha de comando. Ele não possui um modo interativo **REPL** (Read-Eval-Print Loop), que permitiria ao usuário digitar comandos um por um e ver o resultado imediato.

## Como Executar

O código foi projetado para funcionar independentemente do nome da pasta principal do projeto.


1.  Certifique-se de que você tem o Python 3 instalado.
2.  A estrutura de pastas dentro da sua pasta raiz deve ser a seguinte:
    ```
    <pasta-raiz-do-projeto>/
    ├── README.md
    ├── morsescript/
    │   └── ... (todos os arquivos .py)
    └── exemplos/
        └── demo.morse
    ```
3.  Abra um terminal e navegue para a pasta raiz do seu projeto (seja ela `trabalho-final-trabalhocomp-2025-1`, `MeuProjeto`, ou qualquer outro nome que você tenha escolhido).

    ```bash
    # Exemplo: se sua pasta se chama "MeuProjetoCompiladores"
    cd caminho/para/MeuProjetoCompiladores
    ```

4.  Uma vez dentro da pasta raiz, execute um script com o seguinte comando:

    ```bash
    python -m morsescript exemplos/NOME-DO-ARQUIVO.morse
    ```

## Referências

- https://how.dev/answers/how-to-write-a-morse-code-translator-in-python
