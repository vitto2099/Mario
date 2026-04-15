class Individuo:
    def __init__(self, n_frames, cromossomo=None):
        self.n_frames = n_frames # Quantidade de ações que o Mario vai tomar
        self.nota_avaliacao = 0  # O quão bem ele foi (fitness)
        if cromossomo:
            self.cromossomo = list(cromossomo)
        else:
            # Se não houver DNA, cria um aleatório (movimentos de 0 a 6)
            self.cromossomo = [random.randint(0, 6) for _ in range(n_frames)]

    def avaliar_visual(self):
        # Cria o ambiente do Mario
        env = gym_super_mario_bros.make('SuperMarioBros-1-1-v0', render_mode='human', apply_api_compatibility=True)
        env = JoypadSpace(env, SIMPLE_MOVEMENT) # Limita os movimentos para facilitar
        env.reset()
        
        dist_maxima = 0
        recompensa_total = 0

        for acao in self.cromossomo:
            # Repete a mesma ação por 6 frames para o movimento ser perceptível
            for _ in range(6):
                state, reward, term, trunc, info = env.step(acao)
                
                # Acompanha a maior distância alcançada à direita (x_pos)
                if info['x_pos'] > dist_maxima:
                    dist_maxima = info['x_pos']

                recompensa_total += reward
                env.render() # Mostra o jogo na tela

                if term or trunc: break
            if term or trunc: break

        env.close()
        # A pontuação final foca na distância percorrida + um bônus de recompensa do jogo
        self.nota_avaliacao = dist_maxima + max(0, recompensa_total * 0.1)

    def mutacao(self, taxa):
        # Pequena chance de mudar um movimento aleatório no DNA
        for i in range(self.n_frames):
            if random.random() < taxa:
                self.cromossomo[i] = random.randint(0, 6)
        return self

    def crossover(self, outro):
        # Mistura o DNA de dois pais para criar um filho
        ponto = random.randint(1, self.n_frames - 1)
        dna_filho = self.cromossomo[:ponto] + outro.cromossomo[ponto:]
        return Individuo(self.n_frames, dna_filho)