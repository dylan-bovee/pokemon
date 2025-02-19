import requests

def get_base_experience(pokemon_name):
    """Récupère l'expérience de base d'un Pokémon depuis la PokéAPI"""
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data["base_experience"]
    else:
        print(f"Erreur : Impossible de récupérer les données pour {pokemon_name}")
        return None

def calculate_exp_gained(defeated_pokemon, defeated_level):

    base_exp = get_base_experience(defeated_pokemon)
    
    if base_exp is None:
        return 0  # Erreur dans la récupération de l'EXP de base

    exp_gained = (base_exp * defeated_level) / 7  # Formule classique de Pokémon


    return int(exp_gained)  # On retourne un entier

# Exemple d'utilisation
pokemon_vaincu = ""
niveau_vaincu = 1

exp_gagnee = calculate_exp_gained(pokemon_vaincu, niveau_vaincu)
print(f"EXP gagnée : {exp_gagnee}")
