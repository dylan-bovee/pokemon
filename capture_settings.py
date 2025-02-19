import random
import json
import pygame

class CaptureSystem:
    def __init__(self, target_pokemon):
        self.target_pokemon = target_pokemon
        self.message = ""
        self.message_timer = 0  

    def attempt_capture(self):
        """Tente de capturer un Pokémon avec une chance basée sur ses PV restants."""
        if self.target_pokemon.current_hp == 0:
            return False, "Le Pokémon est déjà K.O. !"

        # Calcul de la probabilité de capture (max 60% quand PV = 0)
        capture_chance = 0.3
        if random.random() < capture_chance:
            return True, f"{self.target_pokemon.name} capturé !"
        else:
            return False, "La capture a échoué !"

    def save_capture(self, pokemon_name):
        """Ajoute un Pokémon capturé dans un fichier JSON."""
        filename = "captured_pokemons.json"

        try:
            with open(filename, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {"pokemons_captures": []}  # Créer une liste vide si le fichier n'existe pas

        data["pokemons_captures"].append(pokemon_name)  # Ajouter le Pokémon

        with open(filename, "w") as file:
            json.dump(data, file, indent=4)  # Sauvegarder

        print(f"{pokemon_name} a été ajouté à {filename} !")

    def draw_message(self, screen, font):
        """Affiche un message à l'écran pendant 2 secondes."""
        if self.message and pygame.time.get_ticks() < self.message_timer:
            text = font.render(self.message, True, (0, 0, 0))
            text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() - 50))
            pygame.draw.rect(screen, (255, 255, 255), text_rect.inflate(20, 10))
            pygame.draw.rect(screen, (0, 0, 0), text_rect.inflate(20, 10), 2)
            screen.blit(text, text_rect)

    def handle_capture(self):
        """Gère la tentative de capture et stocke le message."""
        success, message = self.attempt_capture()
        self.message = message
        self.message_timer = pygame.time.get_ticks() + 2000  # Affiche pendant 2 secondes

        if success:
            self.save_capture(self.target_pokemon.name)  # Sauvegarde la capture

        return success
