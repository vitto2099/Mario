import pickle

try:
    with open('historico.pkl', 'rb') as f:
        data = pickle.load(f)
    print(f"Total entries: {len(data)}")
    for i in range(min(3, len(data))):
        print(f"Entry {i}: {data[i]}")
except Exception as e:
    print(f"Error: {e}")
