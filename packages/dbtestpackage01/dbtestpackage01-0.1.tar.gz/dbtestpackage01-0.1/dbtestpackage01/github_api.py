import requests


def buscar_avatar(usuario):
    """Pega a url do avatar de usuário na API do Github"""
    url = f'https://api.github.com/users/{usuario}'
    resp = requests.get(url)
    return resp.json()['avatar_url']


if __name__ == '__main__':
    print(buscar_avatar('boybluepiano'))
