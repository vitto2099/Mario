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

    def avaliar_visual(self):
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
        for i in range(self.n_frames):
            if random.random() < taxa:
                self.cromossomo[i] = random.randint(0, 6)
        return self

    def crossover(self, outro):
        ponto = random.randint(1, self.n_frames - 1)
        dna_filho = self.cromossomo[:ponto] + outro.cromossomo[ponto:]
        return Individuo(self.n_frames, dna_filho)


class AlgoritmoGenetico:
    def __init__(self, tamanho_pop):
        self.tamanho_pop = tamanho_pop
        self.arquivo_save = "melhor_mario.pkl"

    def salvar(self, dna):
        with open(self.arquivo_save, 'wb') as f:
            pickle.dump(dna, f)

    def carregar(self):
        if os.path.exists(self.arquivo_save):
            with open(self.arquivo_save, 'rb') as f:
                return pickle.load(f)
        return None

    def resolver(self, n_geracoes, n_frames, taxa_mutacao):
        print(f"marioRun (Modo Visual) | Pop: {self.tamanho_pop} | Frames: {n_frames}")

        populacao = [Individuo(n_frames) for _ in range(self.tamanho_pop)]

        dna_salvo = self.carregar()
        if dna_salvo:
            dna_ajustado = dna_salvo[:n_frames]
            while len(dna_ajustado) < n_frames:
                dna_ajustado.append(random.randint(0, 6))
            print("Memoria carregada! Mestre na populacao.")
            populacao[0].cromossomo = dna_ajustado

        melhor_global = 0

        for g in range(n_geracoes):
            print(f"\n{'='*40}")
            print(f"  GERACAO {g}")
            print(f"{'='*40}")

            for i, ind in enumerate(populacao):
                print(f"Exibindo Individuo {i+1}/{self.tamanho_pop}...")
                ind.avaliar_visual()
                print(f"   Distancia: {ind.nota_avaliacao:.1f}m")

            populacao.sort(key=lambda x: x.nota_avaliacao, reverse=True)
            melhor = populacao[0]

            if melhor.nota_avaliacao > melhor_global:
                melhor_global = melhor.nota_avaliacao
                print(f"\nNOVO RECORDE: {melhor_global:.1f}m!")
            print(f"Recorde da Geracao {g}: {melhor.nota_avaliacao:.1f}m | Global: {melhor_global:.1f}m")

            self.salvar(melhor.cromossomo)

            nova_pop = []
            nova_pop.append(Individuo(n_frames, populacao[0].cromossomo))
            nova_pop.append(Individuo(n_frames, populacao[1].cromossomo))

            elite = populacao[:max(3, self.tamanho_pop // 2)]
            while len(nova_pop) < self.tamanho_pop:
                pai1 = random.choice(elite)
                pai2 = random.choice(elite)
                filho = pai1.crossover(pai2)
                filho.mutacao(taxa_mutacao)
                nova_pop.append(filho)

            populacao = nova_pop


if __name__ == "__main__":
    ag = AlgoritmoGenetico(tamanho_pop=10)
    ag.resolver(
        n_geracoes=50,
        n_frames=1000,
        taxa_mutacao=0.05
    )