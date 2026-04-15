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
        if cromossomo:
            self.cromossomo = list(cromossomo)
        else:
            self.cromossomo = [random.randint(0, 6) for _ in range(n_frames)]

    def avaliar(self):
        env = gym_super_mario_bros.make('SuperMarioBros-1-1-v0', apply_api_compatibility=True)
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

                if term or trunc:
                    break

            if term or trunc:
                break

        env.close()
        self.nota_avaliacao = dist_maxima + max(0, recompensa_total * 0.1)

    def mutacao(self, taxa):
        for i in range(self.n_frames):
            if random.random() < taxa:
                self.cromossomo[i] = random.randint(0, 6)
        return self

    def crossover(self, outro):
        ponto = random.randint(1, self.n_frames - 1)
        dna_filho = self.cromossomo[:ponto] + outro.cromossomo[ponto:]
        return Individuo(self.n_frames, dna_filho)


class TreinadorMario:
    def __init__(self, tamanho_pop):
        self.tamanho_pop = tamanho_pop
        self.arquivo_save = "melhor_mario.pkl"
        self.arquivo_hist = "historico.pkl"

    def salvar_dados(self, melhor_ind, geracao, historico):
        with open(self.arquivo_save, 'wb') as f:
            pickle.dump(melhor_ind.cromossomo, f)

        historico.append({
            'geracao': geracao,
            'distancia': melhor_ind.nota_avaliacao,
            'dna': melhor_ind.cromossomo[:5]
        })
        with open(self.arquivo_hist, 'wb') as f:
            pickle.dump(historico, f)

    def carregar_mestre(self):
        if os.path.exists(self.arquivo_save):
            with open(self.arquivo_save, 'rb') as f:
                return pickle.load(f)
        return None

    def carregar_historico(self):
        if os.path.exists(self.arquivo_hist):
            with open(self.arquivo_hist, 'rb') as f:
                return pickle.load(f)
        return []

    def iniciar_treino(self, n_geracoes, n_frames, taxa_mutacao):
        print(f"Iniciando Treino | Populacao: {self.tamanho_pop} | Frames: {n_frames}")

        populacao = [Individuo(n_frames) for _ in range(self.tamanho_pop)]

        historico = self.carregar_historico()
        geracao_offset = historico[-1]['geracao'] + 1 if historico else 0

        dna_salvo = self.carregar_mestre()
        if dna_salvo:
            print("DNA anterior carregado - inserindo na populacao inicial...")
            populacao[0].cromossomo = list(dna_salvo)
            copia = Individuo(n_frames, dna_salvo)
            copia.mutacao(taxa_mutacao * 0.5)
            populacao[1].cromossomo = copia.cromossomo

        melhor_global = 0

        for g in range(n_geracoes):
            geracao_real = g + geracao_offset

            for i, ind in enumerate(populacao):
                ind.avaliar()
                print(f"  Ger {geracao_real} | Ind {i+1}/{self.tamanho_pop} | Dist: {ind.nota_avaliacao:.1f}", end="\r")

            populacao.sort(key=lambda x: x.nota_avaliacao, reverse=True)
            melhor = populacao[0]

            if melhor.nota_avaliacao > melhor_global:
                melhor_global = melhor.nota_avaliacao
                print(f"\nNOVO RECORDE GLOBAL: {melhor_global:.1f}m na geracao {geracao_real}!")
            else:
                print(f"\nGeracao {geracao_real} | Melhor: {melhor.nota_avaliacao:.1f}m | Recorde: {melhor_global:.1f}m")

            self.salvar_dados(melhor, geracao_real, historico)

            nova_pop = []
            nova_pop.append(Individuo(n_frames, populacao[0].cromossomo))
            nova_pop.append(Individuo(n_frames, populacao[1].cromossomo))

            elite = populacao[:max(4, self.tamanho_pop // 3)]
            while len(nova_pop) < self.tamanho_pop:
                pai1 = random.choice(elite)
                pai2 = random.choice(elite)
                filho = pai1.crossover(pai2)
                filho.mutacao(taxa_mutacao)
                nova_pop.append(filho)

            populacao = nova_pop


if __name__ == "__main__":
    TREINADOR = TreinadorMario(tamanho_pop=10)
    TREINADOR.iniciar_treino(
        n_geracoes=100,
        n_frames=1000,
        taxa_mutacao=0.05
    )