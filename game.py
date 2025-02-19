import pygame
import random
from pokemon import Pokemon

class PokemonGame:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Pokémon Game")

        self.font = pygame.font.Font(None, 28)

        # Charger les Pokémon
        self.player_pokemon = Pokemon("charmander", back_sprite=True)
        self.opponent_pokemon = Pokemon("pikachu")

        # Positions des Pokémon
        self.player_x, self.player_y = 80, self.HEIGHT - 200
        self.opponent_x, self.opponent_y = self.WIDTH - 180, 80

        # Gestion du tour
        self.is_player_turn = True  # Le joueur commence
        self.selected_attack = None  # Stocke l'attaque sélectionnée

        self.running = True

    def draw_pokemon_info(self, x, y, pokemon, level):
        """ Affiche les informations d'un Pokémon avec une barre de vie. """
        name_text = self.font.render(pokemon.name, True, (0, 0, 0))
        level_text = self.font.render(f"Niv. {level}", True, (0, 0, 0))

        name_width, _ = self.font.size(pokemon.name)
        level_width, _ = self.font.size(f"Niv. {level}")

        info_width = name_width + level_width + 25
        info_height = 60

        pygame.draw.rect(self.screen, (255, 255, 255), (x, y, info_width, info_height))
        pygame.draw.rect(self.screen, (0, 0, 0), (x, y, info_width, info_height), 2)

        self.screen.blit(name_text, (x + 10, y + 5))
        self.screen.blit(level_text, (x + name_width + 15, y + 5))

        hp_percentage = pokemon.current_hp / pokemon.hp
        hp_bar_width = int((info_width - 20) * hp_percentage)
        pygame.draw.rect(self.screen, (0, 200, 0) if hp_percentage > 0.3 else (200, 0, 0), (x + 10, y + 35, hp_bar_width, 12))
        pygame.draw.rect(self.screen, (0, 0, 0), (x + 10, y + 35, info_width - 20, 12), 2)

    def charge_attack(self):
        """ Animation de Charge et dégâts à Pikachu. """
        self.animate_attack(self.player_x, self.opponent_x, "charge")
        self.opponent_pokemon.current_hp -= 10
        if self.opponent_pokemon.current_hp < 0:
            self.opponent_pokemon.current_hp = 0
        self.end_turn()

    def ember_attack(self):
        """ Animation de Flammèche et dégâts à Pikachu. """
        self.animate_attack(self.player_x, self.opponent_x, "ember")
        self.opponent_pokemon.current_hp -= 15
        if self.opponent_pokemon.current_hp < 0:
            self.opponent_pokemon.current_hp = 0
        self.end_turn()

    def opponent_turn(self):
        """ Tour de Pikachu avec un choix aléatoire entre Éclair et Griffe. """
        attack_choice = random.choice(["thunder_shock", "scratch"])
        if attack_choice == "thunder_shock":
            self.animate_attack(self.opponent_x, self.player_x, "thunder_shock")
            self.player_pokemon.current_hp -= 12
        else:
            self.animate_attack(self.opponent_x, self.player_x, "scratch")
            self.player_pokemon.current_hp -= 8

        if self.player_pokemon.current_hp < 0:
            self.player_pokemon.current_hp = 0

        self.is_player_turn = True

    def animate_attack(self, attacker_x, target_x, attack_type):
        """ Animation selon le type d'attaque. """
        original_attacker_x = attacker_x
        original_target_x = target_x

        if attack_type == "charge" or attack_type == "scratch":
            # Attaque physique : le Pokémon avance et l'autre recule
            for _ in range(5):
                attacker_x += 5 if attack_type == "charge" else -5
                target_x += -3 if attack_type == "charge" else 3
                self.draw_scene()
                pygame.display.update()
                pygame.time.delay(30)
        
        elif attack_type == "ember":
            # Animation Flammèche 🔥
            for _ in range(5):
                self.draw_scene()
                flame = pygame.Rect(target_x - 30, self.opponent_y + 20, 20, 20)
                pygame.draw.ellipse(self.screen, (255, 100, 0), flame)
                pygame.display.update()
                pygame.time.delay(30)
        
        elif attack_type == "thunder_shock":
            # Animation Éclair ⚡
            for _ in range(5):
                self.draw_scene()
                lightning = pygame.Rect(target_x + 30, self.player_y + 20, 10, 40)
                pygame.draw.line(self.screen, (255, 255, 0), (lightning.x, lightning.y), (lightning.x + 10, lightning.y + 40), 3)
                pygame.display.update()
                pygame.time.delay(30)

        attacker_x = original_attacker_x
        target_x = original_target_x

    def draw_menu(self):
        """ Affiche le menu des attaques. """
        pygame.draw.rect(self.screen, (200, 200, 200), (50, self.HEIGHT - 100, 300, 80))
        charge_text = self.font.render("1. Charge", True, (0, 0, 0))
        ember_text = self.font.render("2. Flammèche", True, (0, 0, 0))
        self.screen.blit(charge_text, (60, self.HEIGHT - 90))
        self.screen.blit(ember_text, (60, self.HEIGHT - 60))

    def draw_scene(self):
        """ Dessine la scène. """
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.player_pokemon.sprite, (self.player_x, self.player_y))
        self.screen.blit(self.opponent_pokemon.sprite, (self.opponent_x, self.opponent_y))
        self.draw_pokemon_info(self.WIDTH - 200, self.player_y, self.player_pokemon, 12)
        self.draw_pokemon_info(10, self.opponent_y, self.opponent_pokemon, 8)
        if self.is_player_turn:
            self.draw_menu()

    def end_turn(self):
        """ Termine le tour du joueur et fait jouer Pikachu. """
        self.is_player_turn = False
        pygame.time.delay(500)
        self.opponent_turn()

    def run(self):
        """ Boucle principale du jeu. """
        while self.running:
            self.draw_scene()
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN and self.is_player_turn:
                    if event.key == pygame.K_1:
                        self.charge_attack()
                    elif event.key == pygame.K_2:
                        self.ember_attack()

        pygame.quit()
