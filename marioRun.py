import gym_super_mario_bros
from nes_py.wrappers import JoypadSpace
from gym_super_mario_bros.actions import SIMPLE_MOVEMENT
import random
import pickle
import os

# ==========================================================
# CLASSE DO INDIVÍDUO (MARIO)
# ==========================================================
class Individuo:
    def __init__(self, n_frames, cromossomo=None):
        self.n_frames = n_frames
        self.nota_avaliacao = 0
        if cromossomo:
            self.cromossomo = list(cromossomo)
        else:
            self.cromossomo = [random.randint(0, 6) for _ in range(n_frames)]
        
    def avaliar_visual(self):
        # 'human' ativa a janela do jogo para podermos assistir
        env = gym_super_mario_bros.make('SuperMarioBros-1-1-v0', render_mode='human', apply_api_compatibility=True)
        env = JoypadSpace(env, SIMPLE_MOVEMENT)
        
        env.reset()
        dist_maxima = 0
        
        for acao in self.cromossomo:
            # Segura o mesmo botão por 6 frames para pulos mais altos!
            for _ in range(6):
                state, reward, term, trunc, info = env.step(acao)
                
                if info['x_pos'] > dist_maxima:
                    dist_maxima = info['x_pos']
                
                env.render() # Renderiza todos os frames para o vídeo ficar suave
                
                if term or trunc:
                    break # Para o loop interno
                    
            if term or trunc:
                break # Para o loop externo
        
        env.close()
        self.nota_avaliacao = dist_maxima

    def mutacao(self, taxa):
        for i in range(self.n_frames):
            if random.random() < taxa:
                self.cromossomo[i] = random.randint(0, 6)
        return self

# ==========================================================
# CLASSE DO ALGORITMO GENÉTICO (MODO APRESENTAÇÃO)
# ==========================================================
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
        print(f"🚀 A iniciar marioRun (Modo Visual) | População: {self.tamanho_pop}")
        
        populacao = [Individuo(n_frames) for _ in range(self.tamanho_pop)]
        
        dna_salvo = self.carregar()
        if dna_salvo:
            print("📂 Memória carregada! O mestre está na população.")
            populacao[0].cromossomo = dna_salvo

        for g in range(n_geracoes):
            print(f"\n--- GERAÇÃO {g} ---")
            
            for i, ind in enumerate(populacao):
                print(f"📺 A exibir Indivíduo #{i+1}/{self.tamanho_pop}...", end=" ")
                ind.avaliar_visual()
                print(f"Distância: {ind.nota_avaliacao}m")
            
            populacao.sort(key=lambda x: x.nota_avaliacao, reverse=True)
            melhor = populacao[0]
            
            print(f"🏆 Recorde da Geração: {melhor.nota_avaliacao}m")
            self.salvar(melhor.cromossomo)
            
            # Evolução
            nova_pop = populacao[:2] # Mantém os 2 melhores
            while len(nova_pop) < self.tamanho_pop:
                pai = random.choice(populacao[:4])
                filho = Individuo(n_frames, pai.cromossomo)
                nova_pop.append(filho.mutacao(taxa_mutacao))
            
            populacao = nova_pop

# ==========================================================
# EXECUÇÃO
# ==========================================================
if __name__ == "__main__":
    # População reduzida para a apresentação não ser demasiado longa
    ag = AlgoritmoGenetico(tamanho_pop=5) 
    ag.resolver(n_geracoes=2, n_frames=4000, taxa_mutacao=0.9)