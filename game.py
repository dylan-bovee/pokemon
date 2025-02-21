import pygame
import random
from pokemon import Pokemon
from capture_settings import CaptureSystem
from pokeball_animation import PokeBallAnimation  # Import de l'animation de la Poké Ball

class PokemonGame:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Pokémon Game")

        self.font = pygame.font.Font(None, 28)

        # Charger les Pokémon
        self.player_pokemon = Pokemon("Charmander", back_sprite=True)
        self.opponent_pokemon = Pokemon("Pikachu")

        # Initialiser le système de capture
        self.capture_system = CaptureSystem(self.opponent_pokemon)

        # Positions des Pokémon
        self.player_x, self.player_y = 80, self.HEIGHT - 250
        self.opponent_x, self.opponent_y = self.WIDTH - 180, 100

        # Gestion du tour et de l'interface
        self.is_player_turn = True
        self.running = True
        self.menu_state = "choice"
        self.message = "Que voulez-vous faire ?"

        # Animation de la Poké Ball
        self.pokeball_animation = None  

    def draw_pokemon_info(self, x, y, pokemon, level):
        """Affiche les informations d'un Pokémon avec une barre de vie."""
        name_text = self.font.render(pokemon.name, True, (0, 0, 0))
        level_text = self.font.render(f"Niv. {level}", True, (0, 0, 0))
        hp_text = self.font.render(f"PV: {pokemon.current_hp}/{pokemon.hp}", True, (0, 0, 0))

        box_width, box_height = 180, 80
        pygame.draw.rect(self.screen, (255, 255, 255), (x, y, box_width, box_height))
        pygame.draw.rect(self.screen, (0, 0, 0), (x, y, box_width, box_height), 2)

        self.screen.blit(name_text, (x + 10, y + 5))
        self.screen.blit(level_text, (x + 10, y + 25))
        self.screen.blit(hp_text, (x + 10, y + 45))

        hp_percentage = pokemon.current_hp / pokemon.hp
        hp_bar_width = int((box_width - 20) * hp_percentage)
        pygame.draw.rect(self.screen, (0, 200, 0) if hp_percentage > 0.3 else (200, 0, 0), (x + 10, y + 65, hp_bar_width, 10))
        pygame.draw.rect(self.screen, (0, 0, 0), (x + 10, y + 65, box_width - 20, 10), 2)

    def draw_message(self):
        """Affiche les messages d'action en jeu."""
        msg_text = self.font.render(self.message, True, (0, 0, 0))
        pygame.draw.rect(self.screen, (255, 255, 255), (50, self.HEIGHT - 170, 700, 40))
        pygame.draw.rect(self.screen, (0, 0, 0), (50, self.HEIGHT - 170, 700, 40), 2)
        self.screen.blit(msg_text, (60, self.HEIGHT - 160))

    def draw_choice_menu(self):
        """Affiche le choix entre Attaque et Capture."""
        pygame.draw.rect(self.screen, (200, 200, 200), (50, self.HEIGHT - 120, 300, 80))
        attack_text = self.font.render("1. Attaquer", True, (0, 0, 0))
        capture_text = self.font.render("2. Capturer", True, (0, 0, 0))
        self.screen.blit(attack_text, (60, self.HEIGHT - 110))
        self.screen.blit(capture_text, (60, self.HEIGHT - 80))

    def draw_attack_menu(self):
        """Affiche le menu des attaques après avoir choisi 'Attaquer'."""
        pygame.draw.rect(self.screen, (200, 200, 200), (50, self.HEIGHT - 120, 300, 80))
        charge_text = self.font.render("1. Charge", True, (0, 0, 0))
        ember_text = self.font.render("2. Flammèche", True, (0, 0, 0))
        self.screen.blit(charge_text, (60, self.HEIGHT - 110))
        self.screen.blit(ember_text, (60, self.HEIGHT - 80))

    def attack(self, attack_name, damage):
        """Gère une attaque du joueur et passe le tour à l'adversaire."""
        self.message = f"{self.player_pokemon.name} utilise {attack_name} !"
        self.opponent_pokemon.take_damage(damage)
        pygame.time.delay(500)
        self.end_turn()

    def attempt_capture(self):
        """Tente la capture avec animation de la Poké Ball."""
        self.pokeball_animation = PokeBallAnimation(self.screen, self.player_x + 50, self.player_y, self.opponent_x, self.opponent_y)

    def opponent_turn(self):
        """Gère l'attaque aléatoire de l'adversaire."""
        if self.opponent_pokemon.current_hp > 0:
            attack_choice = random.choice([("Éclair", 12), ("Griffe", 8)])
            self.message = f"{self.opponent_pokemon.name} utilise {attack_choice[0]} !"
            self.player_pokemon.take_damage(attack_choice[1])
            pygame.time.delay(500)
            self.is_player_turn = True
            self.menu_state = "choice"

    def draw_scene(self):
        """Dessine l'écran de jeu."""
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.player_pokemon.sprite, (self.player_x, self.player_y))
        self.screen.blit(self.opponent_pokemon.sprite, (self.opponent_x, self.opponent_y))
        self.draw_pokemon_info(self.WIDTH - 220, self.player_y - 50, self.player_pokemon, 12)
        self.draw_pokemon_info(20, self.opponent_y - 50, self.opponent_pokemon, 8)
        self.draw_message()

        if self.menu_state == "choice":
            self.draw_choice_menu()
        elif self.menu_state == "attack":
            self.draw_attack_menu()

        self.capture_system.draw_message(self.screen, self.font)

        # Dessiner l'animation de la Poké Ball si active
        if self.pokeball_animation and self.pokeball_animation.active:
            self.pokeball_animation.draw()

    def end_turn(self):
        """Vérifie si le combat est terminé et passe au tour de l'adversaire."""
        if self.opponent_pokemon.current_hp == 0:
            self.message = f"{self.opponent_pokemon.name} est K.O. ! Vous gagnez !"
            self.running = False
        else:
            self.is_player_turn = False
            self.opponent_turn()
            if self.player_pokemon.current_hp == 0:
                self.message = f"{self.player_pokemon.name} est K.O. ! Vous perdez..."
                self.running = False

    def run(self):
        """Boucle principale du jeu."""
        while self.running:
            self.draw_scene()
            pygame.display.update()
            
            if self.pokeball_animation and self.pokeball_animation.active:
                self.pokeball_animation.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN and self.is_player_turn:
                    if self.menu_state == "choice":
                        if event.key == pygame.K_1:
                            self.menu_state = "attack"
                        elif event.key == pygame.K_2:
                            self.attempt_capture()
                    elif self.menu_state == "attack":
                        if event.key == pygame.K_1:
                            self.attack("Charge", 10)
                        elif event.key == pygame.K_2:
                            self.attack("Flammèche", 15)
                        self.menu_state = "choice"


if __name__ == "__main__":
    game = PokemonGame()
    game.run()
