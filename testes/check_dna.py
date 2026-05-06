import pickle

try:
    with open('melhor_mario.pkl', 'rb') as f:
        data = pickle.load(f)
    print(f"DNA length: {len(data)}")
    print(f"DNA sample: {data[:20]}")
except Exception as e:
    print(f"Error: {e}")
