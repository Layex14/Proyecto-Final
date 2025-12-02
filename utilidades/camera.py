import pygame

class Camera:
    def __init__(self,who,ancho_pantalla, ancho_escenario):
        self.cameraman = who
        self.ancho_pamtalla = ancho_pantalla
        self.ancho_escenario = ancho_escenario
        self.offset_x = 0
        
    def update(self):
        screen_center_x = self.ancho_pamtalla/2
        desplazamiento_camara = self.cameraman.rect.centerx - screen_center_x

        self.offset_x = max(0,desplazamiento_camara)

        max_offset = self.ancho_escenario - self.ancho_pamtalla
        self.offset_x = min(self.offset_x, max_offset)
