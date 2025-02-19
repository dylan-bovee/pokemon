import requests
import io
import pygame

class Pokemon:
    def __init__(self, name, back_sprite=False):
        self.name = name.capitalize()
        self.data = self._fetch_pokemon_data(name, back_sprite)

        if self.data:
            self.id = self.data["id"]
            self.types = self.data["type"]
            self.hp = self.data["hp"]
            self.attack = self.data["attack"]
            self.sprite_url = self.data["sprite"]
            self.current_hp = self.hp  # PV actuels
            self.sprite = self._load_sprite()
        else:
            raise ValueError(f"Le Pokémon '{name}' n'a pas été trouvé.")

    def _fetch_pokemon_data(self, name, back_sprite):
        url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            return {
                "name": data["name"].capitalize(),
                "id": data["id"],
                "type": [t["type"]["name"] for t in data["types"]],
                "hp": data["stats"][0]["base_stat"],
                "attack": data["stats"][1]["base_stat"],
                "sprite": data["sprites"]["back_default"] if back_sprite else data["sprites"]["front_default"]
            }
        return None

    def _load_sprite(self):
        response = requests.get(self.sprite_url)
        sprite = pygame.image.load(io.BytesIO(response.content))
        width, height = sprite.get_size()
        return pygame.transform.scale(sprite, (width * 2, height * 2))
