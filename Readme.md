# 🍄 Mario 

Este projeto utiliza **Algoritmos Genéticos** para ensinar um agente a jogar Super Mario Bros de forma autônoma. Não há redes neurais aqui — apenas evolução pura através de tentativa e erro.

---

## 🕹️ Como funciona?

O algoritmo simula gerações de "Marios". Cada indivíduo tem um **DNA** (lista de comandos) e é avaliado pelo quão longe consegue chegar na fase.

### O Ciclo Evolutivo:
1.  **Geração Aleatória**: Começamos com movimentos totalmente aleatórios.
2.  **Avaliação (Fitness)**: O Mario que chegar mais longe (maior coordenada X) ganha a melhor nota.
3.  **Seleção**: Os melhores indivíduos são escolhidos para serem os "pais" da próxima geração.
4.  **Crossover**: Os DNAs dos pais são misturados para criar filhos com características de ambos.
5.  **Mutação**: Pequenas mudanças aleatórias são introduzidas para descobrir novos caminhos.

---

## 📂 Estrutura do Projeto

*   **`marioRun.py`**: O script principal que roda o jogo e o algoritmo evolutivo.
*   **`melhor_mario.pkl`**: Arquivo de "memória". Ele salva o melhor DNA encontrado para que o progresso não seja perdido ao fechar o programa.
*   **`Graficos/`**: Pasta contendo visualizações da evolução do algoritmo.

---

## 🚀 Como Rodar

### 1. Instalação
Certifique-se de ter o Python instalado e execute os comandos abaixo no terminal:

```bash
pip install gym-super-mario-bros nes-py
pip install "numpy<2.0"
```

### 2. Execução
Para ver o Mario evoluindo em tempo real:

```bash
python marioRun.py
```

---

## ⚙️ Configurações (em `marioRun.py`)

Você pode ajustar o comportamento da evolução alterando estas variáveis no código:

| Parâmetro | Valor Padrão | Descrição |
| :--- | :--- | :--- |
| `tamanho_populacao` | 10 | Quantos Marios existem por geração. |
| `numero_geracoes` | 50 | Quantas vezes o processo de evolução se repetirá. |
| `n_frames` | 1000 | Tempo máximo (em frames) que cada Mario tem para agir. |
| `taxa_mutacao` | 0.05 (5%) | Chance de um movimento ser alterado aleatoriamente. |

---

