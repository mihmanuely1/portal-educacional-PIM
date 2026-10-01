from utils.storage import load_users, save_users

def show_courses(username):
    users = load_users()
    print("\n--- Cursos disponíveis ---")
    print("1. Introdução à Lógica")
    print("2. Programação com Python")
    print("3. Segurança Digital")
    print("0. Sair")
    choice = input("Escolha um curso: ")
    if choice != '0':
        users[username]["progress"].append(choice)
        save_users(users)
        print("Curso acessado! Progresso salvo.")
