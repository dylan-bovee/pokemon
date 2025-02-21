import json

class SaveManager:
    def __init__(self, filename="save.json"):
        self.filename = filename

    def save_game(self, player_pokemon, captured_pokemons):
        data = {
            "player_pokemon": {
                "name": player_pokemon.name,
                "level": player_pokemon.level,
                "exp": player_pokemon.exp
            },
            "captured_pokemons": [
                {
                    "name": pokemon.name,
                    "level": pokemon.level,
                    "exp": pokemon.exp
                } for pokemon in captured_pokemons
            ]
        }
        with open(self.filename, "w") as file:
            json.dump(data, file, indent=4)

    def load_game(self):
        try:
            with open(self.filename, "r") as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            return None