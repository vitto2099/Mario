import gym_super_mario_bros
from nes_py.wrappers import JoypadSpace
from gym_super_mario_bros.actions import SIMPLE_MOVEMENT

# 1. Cria o ambiente
env = gym_super_mario_bros.make('SuperMarioBros-1-1-v0', render_mode='human', apply_api_compatibility=True)
env = JoypadSpace(env, SIMPLE_MOVEMENT)

done = True
for step in range(500):
    if done:
        state = env.reset()
    
    # Faz um movimento aleatório (o Mario vai ficar parecendo doido)
    state, reward, terminated, truncated, info = env.step(env.action_space.sample())
    done = terminated or truncated
    
    env.render()

env.close()