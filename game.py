import pygame
from pokemon import Pokemon
from capture_settings import CaptureSystem

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
        self.player_x, self.player_y = 80, self.HEIGHT - 200
        self.opponent_x, self.opponent_y = self.WIDTH - 180, 80

        self.running = True

    def draw_pokemon_info(self, x, y, pokemon, level):
        """Affiche les informations d'un Pokémon avec une barre de vie."""
        bar_width = 100
        bar_height = 10
        hp_ratio = pokemon.current_hp / pokemon.hp

        # Afficher le nom et le niveau
        name_text = self.font.render(f"{pokemon.name} - LVL {level}", True, (0, 0, 0))
        self.screen.blit(name_text, (x, y - 20))

        # Dessiner la barre de vie
        pygame.draw.rect(self.screen, (255, 0, 0), (x, y, bar_width, bar_height))
        pygame.draw.rect(self.screen, (0, 255, 0), (x, y, bar_width * hp_ratio, bar_height))

    def run(self):
        """Boucle principale du jeu."""
        clock = pygame.time.Clock()
        while self.running:
            self.screen.fill((255, 255, 255))

            # Affichage des Pokémon
            self.screen.blit(self.player_pokemon.sprite, (self.player_x, self.player_y))
            self.screen.blit(self.opponent_pokemon.sprite, (self.opponent_x, self.opponent_y))

            # Affichage des infos
            self.draw_pokemon_info(self.WIDTH - 200, self.player_y, self.player_pokemon, 12)
            self.draw_pokemon_info(10, self.opponent_y, self.opponent_pokemon, 8)

            # Affichage des messages de capture
            self.capture_system.draw_message(self.screen, self.font)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b:
                        success = self.capture_system.handle_capture()
                        if success:
                            self.running = False  # Quitter après capture réussie

            pygame.display.update()
            clock.tick(60)

        pygame.quit()
