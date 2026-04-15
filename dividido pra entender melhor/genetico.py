class AlgoritmoGenetico:
    def __init__(self, tamanho_pop):
        self.tamanho_pop = tamanho_pop
        self.arquivo_save = "melhor_mario.pkl" # Nome do arquivo de salvamento

    def salvar(self, dna):
        # Salva o melhor DNA em um arquivo binário (pickle)
        with open(self.arquivo_save, 'wb') as f:
            pickle.dump(dna, f)

    def carregar(self):
        # Tenta carregar um progresso anterior se o arquivo existir
        if os.path.exists(self.arquivo_save):
            with open(self.arquivo_save, 'rb') as f:
                return pickle.load(f)
        return None

    def resolver(self, n_geracoes, n_frames, taxa_mutacao):
        # 1. Inicializa a população
        populacao = [Individuo(n_frames) for _ in range(self.tamanho_pop)]

        # 2. Carrega o "Mestre" se houver um save anterior
        dna_salvo = self.carregar()
        if dna_salvo:
            # Ajusta o tamanho caso você tenha mudado o n_frames
            dna_ajustado = dna_salvo[:n_frames]
            while len(dna_ajustado) < n_frames:
                dna_ajustado.append(random.randint(0, 6))
            populacao[0].cromossomo = dna_ajustado

        melhor_global = 0

        # Loop das Gerações
        for g in range(n_geracoes):
            # 3. Avaliação: Cada indivíduo joga uma vez
            for i, ind in enumerate(populacao):
                ind.avaliar_visual()
            
            # 4. Seleção: Ordena quem foi mais longe
            populacao.sort(key=lambda x: x.nota_avaliacao, reverse=True)
            melhor = populacao[0]

            # Salva o melhor desta geração
            self.salvar(melhor.cromossomo)

            # 5. Reprodução: Cria a próxima geração
            nova_pop = []
            # Elitismo: Mantém os dois melhores sem mudanças
            nova_pop.append(Individuo(n_frames, populacao[0].cromossomo))
            nova_pop.append(Individuo(n_frames, populacao[1].cromossomo))

            # Define quem pode ser "pai" (metade superior da população)
            elite = populacao[:max(3, self.tamanho_pop // 2)]
            
            # Preenche o resto da população com filhos (Crossover + Mutação)
            while len(nova_pop) < self.tamanho_pop:
                pai1 = random.choice(elite)
                pai2 = random.choice(elite)
                filho = pai1.crossover(pai2)
                filho.mutacao(taxa_mutacao)
                nova_pop.append(filho)

            populacao = nova_pop