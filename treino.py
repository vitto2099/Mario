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
        # Se um cromossomo for passado, usa-o (herança), senão cria um aleatório
        if cromossomo:
            self.cromossomo = list(cromossomo)
        else:
            self.cromossomo = [random.randint(0, 6) for _ in range(n_frames)]
        
    def avaliar(self):
        # Modo treino não usa render_mode='human' para ser muito mais rápido
        env = gym_super_mario_bros.make('SuperMarioBros-1-1-v0', apply_api_compatibility=True)
        env = JoypadSpace(env, SIMPLE_MOVEMENT)
        
        env.reset()
        dist_maxima = 0
        
        for acao in self.cromossomo:
            # Pulo do gato: Segura o mesmo botão por 6 frames!
            for _ in range(6): 
                state, reward, term, trunc, info = env.step(acao)
                
                if info['x_pos'] > dist_maxima:
                    dist_maxima = info['x_pos']
                
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
# CLASSE DO ALGORITMO GENÉTICO (TREINO PESADO)
# ==========================================================
class TreinadorMario:
    def __init__(self, tamanho_pop):
        self.tamanho_pop = tamanho_pop
        self.arquivo_save = "melhor_mario.pkl"
        self.arquivo_hist = "historico.pkl"

    def salvar_dados(self, melhor_ind, geracao, historico):
        # Salva o melhor DNA
        with open(self.arquivo_save, 'wb') as f:
            pickle.dump(melhor_ind.cromossomo, f)
        
        # Salva o histórico para análise posterior
        historico.append({
            'geracao': geracao, 
            'distancia': melhor_ind.nota_avaliacao, 
            'dna': melhor_ind.cromossomo[:5] # Apenas amostra
        })
        with open(self.arquivo_hist, 'wb') as f:
            pickle.dump(historico, f)

    def carregar_mestre(self):
        if os.path.exists(self.arquivo_save):
            with open(self.arquivo_save, 'rb') as f:
                return pickle.load(f)
        return None

    def iniciar_treino(self, n_geracoes, n_frames, taxa_mutacao):
        print(f"🏋️ A iniciar Treino Pesado | População: {self.tamanho_pop}")
        
        populacao = [Individuo(n_frames) for _ in range(self.tamanho_pop)]
        historico = []
        
        # Carrega progresso anterior se existir
        dna_salvo = self.carregar_mestre()
        if dna_salvo:
            print("📂 A carregar DNA salvo anteriormente...")
            populacao[0].cromossomo = dna_salvo

        for g in range(n_geracoes):
            # Fase de Avaliação
            for i, ind in enumerate(populacao):
                ind.avaliar()
                print(f"Ger {g} | Ind #{i+1}/{self.tamanho_pop} | Dist: {ind.nota_avaliacao}m", end="\r")
            
            # Ordenação: Melhor para o Pior
            populacao.sort(key=lambda x: x.nota_avaliacao, reverse=True)
            melhor_da_geracao = populacao[0]
            
            print(f"\n🏆 Geração {g} Finalizada | Recorde: {melhor_da_geracao.nota_avaliacao}m")
            
            # Persistência de dados
            self.salvar_dados(melhor_da_geracao, g, historico)

            # Evolução (Geração da próxima população)
            nova_pop = []
            
            # Elitismo: Mantém os 2 melhores sem alterações
            nova_pop.extend(populacao[:2]) 
            
            # Preenche o resto com mutações dos melhores
            while len(nova_pop) < self.tamanho_pop:
                pai = random.choice(populacao[:4]) # Sorteia entre os 4 melhores
                filho = Individuo(n_frames, pai.cromossomo)
                nova_pop.append(filho.mutacao(taxa_mutacao))
            
            populacao = nova_pop

# ==========================================================
# EXECUÇÃO DO PROCESSO
# ==========================================================
if __name__ == "__main__":
    # Configurações de Treino
    TREINADOR = TreinadorMario(tamanho_pop=10)
    TREINADOR.iniciar_treino(
        n_geracoes=100, 
        n_frames=1000, 
        taxa_mutacao=0.1
    )   