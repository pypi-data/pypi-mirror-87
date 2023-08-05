import requests


def buscar_avatar(usuario):
    """
    Busca o acatar de um usuário no Github
    :param usuario: str com o nome do usuario
    :return: str com o link do avatar
    """
    url = f'https://api.github.com/users/{usuario}'
    reps = requests.get(url)
    return reps.json()['avatar_url']


if __name__ == '__main__':
    print(buscar_avatar('buddygn1'))
