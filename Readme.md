    🍄 MarioRUN — Evolução com Algoritmo Genético

    Este projeto utiliza Algoritmos Genéticos para ensinar o Mario a atravessar o nível 1-1 do Super Mario Bros original.

    A ideia é simples: o Mario aprende sozinho, por tentativa e erro, quais sequências de botões fazem ele ir mais longe.

    📋 Sumário
    📝 Sobre o Projeto
    🛠️ Tecnologias Utilizadas
    ⚙️ Como Instalar
    🚀 Como Rodar
    🧠 Gerenciamento de Memória
    🏗️ Estrutura do Código
    📝 Sobre o Projeto

    O Mario começa sem saber absolutamente nada (movimentos aleatórios). A cada geração, acontece:

    🎮 Treino
    20 indivíduos são testados simultaneamente
    Execução em background (sem janela) → muito mais rápido
    📏 Avaliação (Fitness)
    Baseado na posição horizontal (x_pos)
    Quem vai mais longe vence
    🧬 Evolução
    Os melhores indivíduos:
    fazem crossover (mistura de DNA)
    sofrem mutação (pequenas mudanças aleatórias)
    👀 Visualização
    O melhor Mario da geração é exibido na tela
    Com os gráficos clássicos do NES
    🛠️ Tecnologias Utilizadas
    🐍 Python 3.11+
    🎮 Gym Super Mario Bros — emulador e ambiente
    🕹️ Nes-py — controle do NES
    💾 Pickle — salvar/carregar o “cérebro”
    ⚙️ Como Instalar

    Abra o terminal (PowerShell ou CMD) e roda:

    pip install gym-super-mario-bros nes-py
    pip install "numpy<2.0"

    ⚠️ Importante: usar NumPy < 2.0 pra evitar conflito com o Gym

    🚀 Como Rodar

    Certifique-se que o arquivo principal se chama:

    marioRUN.py

    Depois execute:

    python marioRUN.py
    python treino.py


    🧠 Gerenciamento de Memória

    O projeto salva o progresso automaticamente pra não perder o aprendizado.

    💾 Salvar e Carregar

    O melhor indivíduo é salvo em:

    melhor_mario.pkl
    Quando o programa inicia:
    Se o arquivo existir → continua aprendendo de onde parou
    Se não → começa do zero
    🔄 Resetar (Apagar Memória)

    Se quiser zerar tudo:

    rm melhor_mario.pkl

    Ou simplesmente deletar o arquivo manualmente.

    🏗️ Estrutura do Código

    O projeto é dividido em duas partes principais:

    🧍 Classe Individuo

    Responsável pelo comportamento de cada Mario:

    treino()
    Executa a simulação
    mostrar=False → roda sem abrir janela (modo rápido)
    crossover()
    Mistura o DNA de dois indivíduos
    mutacao()
    Aplica mudanças aleatórias
    🧠 Classe AlgoritmoGenetico

    Responsável pela lógica da evolução:

    Gerencia a população
    Ordena os melhores indivíduos
    Salva e carrega os arquivos .pkl
    ⚠️ Nota Técnica
    O projeto usa o ambiente v0
    Isso garante os sprites originais do NES
    Melhor para visualização da evolução