import pickle
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Configuração de estilo "Premium & Clean"
plt.style.use('dark_background')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.facecolor'] = '#0f0f0f'
plt.rcParams['figure.facecolor'] = '#0f0f0f'
plt.rcParams['grid.color'] = '#222222'
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['text.color'] = '#eeeeee'

def gerar_dashboard_clean():
    try:
        # 1. Carregar dados
        with open('historico.pkl', 'rb') as f:
            historico = pickle.load(f)
        df_hist = pd.DataFrame(historico)
        
        with open('melhor_mario.pkl', 'rb') as f:
            melhor_dna = pickle.load(f)
        
        acoes_map = {0: "Nada", 1: "Direita", 2: "Dir+Pulo", 3: "Correr", 4: "Corr+Pulo", 5: "Pulo", 6: "Esquerda"}
        acoes_cores = ['#333333', '#00ffa3', '#00d1ff', '#ffc107', '#ff1744', '#651fff', '#757575']

        # Criar figura com gridspec
        fig = plt.figure(figsize=(16, 12))
        gs = fig.add_gridspec(3, 2, height_ratios=[2, 1, 1], hspace=0.4, wspace=0.3)
        
        # --- 1. Evolução (Principal) ---
        ax1 = fig.add_subplot(gs[0, :])
        ax1.plot(df_hist['geracao'], df_hist['distancia'], color='#00ffa3', linewidth=3, label='Distância Máxima', zorder=3)
        ax1.fill_between(df_hist['geracao'], df_hist['distancia'], color='#00ffa3', alpha=0.05)
        
        if len(df_hist) >= 5:
            trend = df_hist['distancia'].rolling(window=10).mean()
            ax1.plot(df_hist['geracao'], trend, color='#ff1744', linestyle='--', alpha=0.6, label='Tendência (Média 10G)', linewidth=1.5)
        
        ax1.set_title('DESEMPENHO POR GERAÇÃO', fontsize=16, fontweight='bold', pad=20, loc='left')
        ax1.set_ylabel('Distância (pixels)', color='#888888', fontsize=12)
        ax1.set_xlabel('Geração', color='#888888', fontsize=12)
        ax1.grid(True, axis='y', linestyle='-', alpha=0.1)
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        ax1.legend(loc='upper left', frameon=False, fontsize=11)

        # Destaque para o recorde (sem caixa grande)
        max_dist = df_hist['distancia'].max()
        max_gen = df_hist.loc[df_hist['distancia'].idxmax(), 'geracao']
        ax1.scatter(max_gen, max_dist, color='#00ffa3', s=80, edgecolors='white', zorder=5)
        ax1.text(max_gen + 1, max_dist + 50, f'Recorde: {max_dist:.0f}', color='#00ffa3', fontweight='bold')

        # --- 2. Distribuição de Ações ---
        ax2 = fig.add_subplot(gs[1:, 0])
        contagem = pd.Series(melhor_dna).value_counts().sort_index()
        labels = [acoes_map.get(i, str(i)) for i in contagem.index]
        
        bars = ax2.barh(labels, contagem.values, color=acoes_cores[:len(labels)], alpha=0.8)
        ax2.set_title('PERFIL DE MOVIMENTAÇÃO (MELHOR DNA)', fontsize=14, fontweight='bold', pad=15, loc='left')
        ax2.set_xlabel('Frequência de Ações', color='#888888')
        ax2.invert_yaxis() # Melhor para leitura
        ax2.grid(True, axis='x', linestyle='--', alpha=0.1)
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        
        for bar in bars:
            width = bar.get_width()
            ax2.text(width + 5, bar.get_y() + bar.get_height()/2, f'{int(width)}', va='center', color='white', fontsize=10)

        # --- 3. Timeline de Ações (Heatmap Style) ---
        ax3 = fig.add_subplot(gs[1:, 1])
        timeline_size = 400 # Ver mais frames
        actions_chunk = melhor_dna[:timeline_size]
        
        # Criar uma matriz para o heatmap
        heatmap_data = np.zeros((7, timeline_size))
        for i, val in enumerate(actions_chunk):
            if val < 7:
                heatmap_data[val, i] = 1
        
        ax3.imshow(heatmap_data, aspect='auto', cmap='Greens', alpha=0.7, interpolation='nearest')
        ax3.set_yticks(range(7))
        ax3.set_yticklabels([acoes_map[i] for i in range(7)], fontsize=10)
        ax3.set_title(f'SEQUÊNCIA DE AÇÕES (PRIMEIROS {timeline_size} FRAMES)', fontsize=14, fontweight='bold', pad=15, loc='left')
        ax3.set_xlabel('Tempo (Frames)', color='#888888')
        
        # Adicionar o título geral com mais espaço
        plt.suptitle('ANÁLISE DE EVOLUÇÃO - SUPER MARIO BROS (AG)', fontsize=24, fontweight='bold', y=0.98, color='#00ffa3')
        
        # Salvar
        output_path = 'mario_dashboard_v2.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#0f0f0f')
        print(f"Novo dashboard salvo em: {output_path}")
        
    except Exception as e:
        print(f"Erro ao gerar dashboard: {e}")

if __name__ == "__main__":
    gerar_dashboard_clean()
