from utils.storage import load_users
from statistics import mean, median, mode

def show_stats():
    users = load_users()
    times = [len(data.get("progress", [])) for data in users.values()]
    if not times:
        print("Nenhum dado para análise.")
        return

    print("Estatísticas de acesso:")
    print(f"- Média de acessos: {mean(times)}")
    print(f"- Mediana de acessos: {median(times)}")
    try:
        print(f"- Moda de acessos: {mode(times)}")
    except:
        print("- Moda de acessos: múltiplos valores.")
