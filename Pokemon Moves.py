import requests

def get_pokemon_move(moves):
    url = f"https://pokeapi.co/api/v2/move/{moves.lower()}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        # Vérification si c'est une attaque de la génération 1
        if data.get("generation", {}).get("name") == "generation-i":
            # Vérification du type de dégâts (physique ou spécial uniquement)
            damage_class = data.get("damage_class", {}).get("name")
            if damage_class in ["physical", "special"]:
                return {
                    "name": data.get("name"),
                    "id": data.get("id"),
                    "accuracy": data.get("accuracy"),
                    "pp": data.get("pp"),
                    "power": data.get("power"),
                    "type": data.get("type", {}).get("name"),
                }
            else:
                print(f"L'attaque {data.get('name')} est de type '{damage_class}', elle est exclue.")
                return None

    return None

move = "14"  # Remplace par le nom ou l'ID d'une attaque
result = get_pokemon_move(move)

if result:
    print(result)
else:
    print("Cette attaque n'existe pas, ne fait pas partie de la génération 1, ou n'est pas une attaque physique/spéciale.")




