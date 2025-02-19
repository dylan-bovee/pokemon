import requests
import io
import pygame

class Pokemon:
    def __init__(self, name, back_sprite=False):
        self.name = name.capitalize()
        self.data = self._fetch_pokemon_data(name, back_sprite)

        if self.data:
            self.id = self.data["id"]
            self.types = self.data["types"]  # Correction ici
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
                "types": [t["type"]["name"] for t in data["types"]],  # Correction ici
                "hp": data["stats"][0]["base_stat"],
                "attack": data["stats"][1]["base_stat"],
                "sprite": data["sprites"]["back_default"] if back_sprite else data["sprites"]["front_default"]
            }
        return None

    def _load_sprite(self):
        if not self.sprite_url:  # Vérification ajoutée pour éviter une erreur si l'URL est None
            return pygame.Surface((64, 64))  # Image vide pour éviter les erreurs
        response = requests.get(self.sprite_url)
        sprite = pygame.image.load(io.BytesIO(response.content))
        width, height = sprite.get_size()
        return pygame.transform.scale(sprite, (width * 2, height * 2))

    def take_damage(self, damage):
        self.current_hp -= damage
        print(f"{self.name} subit {damage} dégâts !")
        if self.current_hp <= 0:
            self.current_hp = 0
            print(f"{self.name} est K.O. !")

    def calculate_damage(self, opponent):
        damage = max(5, self.attack - opponent.attack // 2)
        print(f"{self.name} attaque {opponent.name} et inflige {damage} dégâts !")
        return damage
