import json
import hashlib
from utils.storage import load_users, save_users

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register():
    users = load_users()
    username = input("Novo nome de usuário: ")
    if username in users:
        print("Usuário já existe.")
        return
    password = input("Senha: ")
    users[username] = {
        "password": hash_password(password),
        "progress": []
    }
    save_users(users)
    print("Usuário registrado com sucesso!")

def login():
    users = load_users()
    username = input("Usuário: ")
    password = input("Senha: ")
    if username in users and users[username]["password"] == hash_password(password):
        print(f"Bem-vindo, {username}!")
        return username
    else:
        print("Credenciais inválidas.")
        return None
