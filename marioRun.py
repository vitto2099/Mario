import gym_super_mario_bros
from nes_py.wrappers import JoypadSpace
from gym_super_mario_bros.actions import SIMPLE_MOVEMENT
import random
import pickle
import os


class Individuo:
    def __init__(self, n_frames, cromossomo=None):
        self.n_frames = n_frames
        self.nota_avaliacao = 0
        self.geracao = 0
        if cromossomo:
            self.cromossomo = list(cromossomo)
        else:
            self.cromossomo = [random.randint(0, 6) for _ in range(n_frames)]

    def avaliacao(self):
        env = gym_super_mario_bros.make('SuperMarioBros-1-1-v0', render_mode='human', apply_api_compatibility=True)
        env = JoypadSpace(env, SIMPLE_MOVEMENT)

        env.reset()
        dist_maxima = 0
        recompensa_total = 0

        for acao in self.cromossomo:
            for _ in range(6):
                state, reward, term, trunc, info = env.step(acao)

                if info['x_pos'] > dist_maxima:
                    dist_maxima = info['x_pos']

                recompensa_total += reward
                env.render()

                if term or trunc:
                    break

            if term or trunc:
                break

        env.close()
        self.nota_avaliacao = dist_maxima + max(0, recompensa_total * 0.1)

    def mutacao(self, taxa):
        novo_cromossomo = list(self.cromossomo)
        for i in range(self.n_frames):
            if random.random() < taxa:
                novo_cromossomo[i] = random.randint(0, 6)
        return Individuo(self.n_frames, novo_cromossomo)

    def crossover(self, outro):
        ponto = random.randint(1, self.n_frames - 1)

        # Dois filhos: um com DNA do pai1+pai2, outro com pai2+pai1
        dna_filho1 = self.cromossomo[:ponto] + outro.cromossomo[ponto:]
        dna_filho2 = outro.cromossomo[:ponto] + self.cromossomo[ponto:]

        return Individuo(self.n_frames, dna_filho1), Individuo(self.n_frames, dna_filho2)


class AlgoritmoGenetico:
    def __init__(self, tamanho_populacao):
        self.tamanho_populacao = tamanho_populacao
        self.populacao = []
        self.geracao = 0
        self.melhor_solucao = None
        self.lista_solucoes = []
        self.arquivo_save = "melhor_mario.pkl"

    def salvar(self, dna):
        with open(self.arquivo_save, 'wb') as f:
            pickle.dump(dna, f)

    def carregar(self):
        if os.path.exists(self.arquivo_save):
            with open(self.arquivo_save, 'rb') as f:
                return pickle.load(f)
        return None

    def inicializa_populacao(self, n_frames):
        self.populacao = [Individuo(n_frames) for _ in range(self.tamanho_populacao)]

        dna_salvo = self.carregar()
        if dna_salvo:
            dna_ajustado = dna_salvo[:n_frames]
            while len(dna_ajustado) < n_frames:
                dna_ajustado.append(random.randint(0, 6))
            print("Memoria carregada! Mestre na populacao.")
            self.populacao[0].cromossomo = dna_ajustado

        self.melhor_solucao = self.populacao[0]

    def ordena_populacao(self):
        self.populacao = sorted(self.populacao,
                                key=lambda ind: ind.nota_avaliacao,
                                reverse=True)

    def melhor_individuo(self, individuo):
        if individuo.nota_avaliacao > self.melhor_solucao.nota_avaliacao:
            self.melhor_solucao = individuo

    def soma_avaliacoes(self):
        return sum(ind.nota_avaliacao for ind in self.populacao)

    def seleciona_pai(self, soma_avaliacao):
        # Roleta: pais com maior nota têm mais chance de ser escolhidos
        pai = -1
        valor_sorteado = random.random() * soma_avaliacao
        soma = 0
        i = 0
        while i < len(self.populacao) and soma < valor_sorteado:
            soma += self.populacao[i].nota_avaliacao
            pai += 1
            i += 1
        return pai

    def visualiza_geracao(self):
        melhor = self.populacao[0]
        print("G:%s -> Distancia: %.1f | Cromossomo: %s" % (
            melhor.geracao,
            melhor.nota_avaliacao,
            melhor.cromossomo[:10]  # exibe só os 10 primeiros genes pra não poluir
        ))

    def resolver(self, taxa_mutacao, numero_geracoes, n_frames):
        print(f"marioRun | Pop: {self.tamanho_populacao} | Frames: {n_frames}")

        self.inicializa_populacao(n_frames)

        # Avalia população inicial
        for individuo in self.populacao:
            print(f"Avaliando individuo...")
            individuo.avaliacao()

        self.ordena_populacao()
        self.melhor_solucao = self.populacao[0]
        self.lista_solucoes.append(self.melhor_solucao.nota_avaliacao)
        self.visualiza_geracao()

        for geracao in range(numero_geracoes):
            print(f"\n{'='*40}")
            print(f"  GERACAO {geracao + 1}")
            print(f"{'='*40}")

            soma_avaliacao = self.soma_avaliacoes()

            # Caso todos tenham nota 0 (geração inicial ruim), usa seleção uniforme
            if soma_avaliacao == 0:
                soma_avaliacao = 1
                for ind in self.populacao:
                    ind.nota_avaliacao = 1

            nova_populacao = []

            # Gera dois filhos por vez, igual ao da mochila
            for _ in range(0, self.tamanho_populacao, 2):
                pai1 = self.seleciona_pai(soma_avaliacao)
                pai2 = self.seleciona_pai(soma_avaliacao)

                filhos = self.populacao[pai1].crossover(self.populacao[pai2])

                filho1 = filhos[0].mutacao(taxa_mutacao)
                filho2 = filhos[1].mutacao(taxa_mutacao)
                filho1.geracao = geracao + 1
                filho2.geracao = geracao + 1

                nova_populacao.append(filho1)
                nova_populacao.append(filho2)

            # Antiga população vai para o "lixo"
            self.populacao = nova_populacao[:self.tamanho_populacao]

            for individuo in self.populacao:
                print(f"Avaliando individuo...")
                individuo.avaliacao()

            self.ordena_populacao()
            self.visualiza_geracao()

            melhor = self.populacao[0]
            self.lista_solucoes.append(melhor.nota_avaliacao)
            self.melhor_individuo(melhor)
            self.salvar(self.melhor_solucao.cromossomo)

        print("\nMelhor solucao -> G: %s | Distancia: %.1f | Cromossomo: %s" % (
            self.melhor_solucao.geracao,
            self.melhor_solucao.nota_avaliacao,
            self.melhor_solucao.cromossomo[:10]
        ))

        return self.melhor_solucao.cromossomo


if __name__ == "__main__":
    ag = AlgoritmoGenetico(tamanho_populacao=10)
    ag.resolver(
        taxa_mutacao=0.05,
        numero_geracoes=50,
        n_frames=1000
    )