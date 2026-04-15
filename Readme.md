# Mario 

Treina um agente autônomo para jogar Super Mario Bros usando **Algoritmos Genéticos**. Sem rede neural, sem aprendizado supervisionado — apenas evolução pura.

---

## Como o Jogo Roda

O Super Mario Bros é executado por um **emulador de NES em Python** via `nes-py`. Não é uma simulação simplificada — é o jogo real rodando frame a frame dentro do processo Python.

```
Python Script
    └── gym-super-mario-bros   ← Interface OpenAI Gym
            └── nes-py          ← Emulador NES completo
                    └── ROM SMB ← O jogo de fato
```

A cada chamada de `env.step(ação)`, o emulador avança **1 frame (1/60s)**. O código repete cada ação por 6 frames consecutivos — o equivalente a segurar o botão por ~100ms, tempo necessário para pulos e corridas terem efeito físico real no jogo.

Em modo visual (`marioRun.py`), uma janela SDL/pyglet abre e exibe o jogo em tempo real. Em modo treino (`treino.py`), tudo roda sem interface gráfica, muito mais rápido.

---

## Como o Algoritmo Genético Funciona

### 1. Representação — O Cromossomo

Cada "Mario" é uma lista de inteiros (0–6), onde cada número é um botão do controle:

| Valor | Ação         |
|-------|--------------|
| 0     | Nenhum (NOOP) |
| 1     | Andar → direita |
| 2     | Andar + Pular |
| 3     | Correr (B) |
| 4     | Correr + Pular |
| 5     | Pular no lugar |
| 6     | Andar ← esquerda |

Um cromossomo de 1000 genes = ~100 segundos de jogo.

### 2. Fitness — Como Medir o Desempenho

```python
nota_avaliacao = dist_maxima + max(0, recompensa_total * 0.1)
```

- **dist_maxima**: posição horizontal mais longe que o Mario chegou
- **recompensa_total × 0.1**: bônus por trajetórias sustentadas, penaliza mortes

### 3. Seleção — Quem Sobrevive

- Os **2 melhores** da geração passam intactos (elitismo)
- O restante é gerado por **crossover + mutação** entre o top 1/3

### 4. Crossover — Combinando DNAs

```
Pai 1: [1, 2, 1, 4, 0, 3, 2, 5]
Pai 2: [3, 3, 4, 1, 2, 0, 1, 4]
Ponto: ─────────────┤
Filho: [1, 2, 1, 4, 2, 0, 1, 4]  ← melhor dos dois
```

Um ponto de corte aleatório divide os cromossomos, e o filho herda a primeira metade de um pai e a segunda metade do outro.

### 5. Mutação — Introduzindo Variação

Cada gene tem 5% de chance de ser substituído por um valor aleatório. Taxa baixa = preserva bons genes, mas mantém exploração.

> ⚠️ Uma taxa de mutação alta (ex: 90%) destrói o DNA a cada geração — o algoritmo nunca converge.

### 6. Persistência — Memória Entre Execuções

O melhor DNA encontrado é salvo automaticamente em `melhor_mario.pkl`. Ao reiniciar o treino, ele é recarregado e inserido na população inicial — o progresso nunca se perde.

```
treino.py  ──salva──►  melhor_mario.pkl  ◄──lê──  marioRun.py
```

---

## Estrutura do Projeto

```
mario-ag/
├── treino.py           # Treino headless (sem janela)
├── marioRun.py         # Apresentação visual (janela do jogo aberta)
├── melhor_mario.pkl    # DNA do melhor Mario (gerado automaticamente)
└── historico.pkl       # Histórico de distâncias por geração
```

---

## Como Usar

### Instalação:
No PowerShell (Padrão do VS Code) 
```bash
use: Get-Content comandos.txt | iex
```

```bash
pip install gym-super-mario-bros nes-py
pip install "numpy<2.0"
```

### Treinar (rápido, sem interface)

```bash
python treino.py
```

Roda 100 gerações com população de 10. Salva progresso automaticamente. Pode ser interrompido e retomado.

### Assistir o Melhor Mario

```bash
python marioRun.py
```

Carrega o melhor DNA do treino e abre a janela do jogo. Roda 2 gerações com população de 5.

---

## ⚙️ Parâmetros

| Parâmetro       | treino.py | marioRun.py | Descrição |
|----------------|-----------|-------------|-----------|
| `tamanho_pop`  | 10        | 5           | Indivíduos por geração |
| `n_geracoes`   | 100       | 2           | Gerações totais |
| `n_frames`     | 1000      | 1000        | Ações por cromossomo |
| `taxa_mutacao` | 0.05      | 0.05        | Prob. de mutar cada gene |

---

## O que Esperar

- **Geração 0**: Mario aleatório, morre rapidamente
- **Gerações 5–10**: Começa a andar para a direita consistentemente
- **Gerações 20+**: Aprende a pular obstáculos básicos
- **Gerações 50+**: Trajetórias mais longas e confiáveis

O progresso não é linear — pode estagnar por algumas gerações e melhorar subitamente quando uma boa combinação de genes surge por crossover.

---

## Notas Técnicas

- Em servidores Linux sem GUI, `marioRun.py` requer um display virtual: `Xvfb :99 -screen 0 1024x768x24 & DISPLAY=:99 python marioRun.py`
- `treino.py` funciona em qualquer ambiente, incluindo servidores sem display
- Os dois scripts compartilham o mesmo arquivo `.pkl` e podem ser alternados livremente