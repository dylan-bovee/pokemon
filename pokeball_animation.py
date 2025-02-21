import pygame
import requests
import io
import math

class PokeBallAnimation:
    def __init__(self, screen, start_x, start_y, target_x, target_y):
        self.screen = screen
        self.image = self.load_pokeball_image()  # Charger l’image depuis PokeAPI
        self.start_x, self.start_y = start_x, start_y
        self.target_x, self.target_y = target_x, target_y
        self.x, self.y = start_x, start_y
        self.t = 0  # Temps (pour gérer la courbe)
        self.speed = 0.002  # Vitesse de l'animation
        self.active = True  # Si l'animation est en cours

    def load_pokeball_image(self):
        """Télécharge l’image de la Poké Ball depuis PokeAPI et la charge en Pygame."""
        url = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/poke-ball.png"
        response = requests.get(url)

        if response.status_code == 200:
            image_bytes = io.BytesIO(response.content)
            image = pygame.image.load(image_bytes)  # Charger l’image depuis la mémoire
            return pygame.transform.scale(image, (30, 30))  # Redimensionner la Poké Ball
        else:
            print("⚠️ Erreur : Impossible de charger la Poké Ball depuis PokeAPI.")
            return pygame.Surface((30, 30))  # Surface vide si l’image ne charge pas

    def update(self):
        """Déplace la Poké Ball en suivant une trajectoire courbée."""
        if self.active:
            self.t += self.speed  # Augmenter le temps pour animer la courbe
            
            # Utilisation d'une courbe de Bézier quadratique
            if self.t >= 1:
                self.active = False  # Fin de l'animation
                return
            
            # Calcul de la position en suivant une courbe
            curve_x = (1 - self.t) ** 2 * self.start_x + 2 * (1 - self.t) * self.t * (self.start_x + (self.target_x - self.start_x) // 2) + self.t ** 2 * self.target_x
            curve_y = (1 - self.t) ** 2 * self.start_y + 2 * (1 - self.t) * self.t * (self.start_y - 100) + self.t ** 2 * self.target_y
            
            self.x, self.y = curve_x, curve_y  # Mise à jour de la position

    def draw(self):
        """Affiche la Poké Ball à sa position actuelle."""
        if self.active:
            self.screen.blit(self.image, (self.x, self.y))
