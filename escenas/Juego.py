import pygame 
import sys 
from configuracion import screenancho, screenalto, blanco
#entidades
from entidades.Entity import Player , Entity

from entidades.boss import BossPancho

#diccionario
from entidades.pancho_config import player_config, player_definitions, pancho_config, pancho_definitions

#Camara
from utilidades.camera import Camera

class Juego:
    def __init__(self, screen):
        self.screen=screen
        self.next_scene=None

        self.ground_level = 127*4 
        self.floor_color = (43, 25, 40)
        
        try:
            self.escenario = pygame.image.load('recursos/imagenes/escenario.png').convert_alpha()
            
            self.malla_jugador=pygame.image.load("recursos/imagenes/player_sprites.png").convert_alpha()
            self.malla_pancho=pygame.image.load("recursos/imagenes/pancho_sprites.png").convert_alpha()
            pygame.mixer.music.load('recursos/musica/Musicaboss.mp3')
            pygame.mixer.music.play(-1, fade_ms=2000)
            pygame.mixer.music.set_volume(0.4)

            self.ancho_escenario = self.escenario.get_width()
        except pygame.error as e:
            print("error de sprite: {e}")
            sys.exit()

        self.all_sprites=pygame.sprite.Group()
        self.enemies=pygame.sprite.Group()


        self.player= Player(
            name="Heroe",
            spritesheet=self.malla_jugador,
            visual_config=player_config,
            animation_data=player_definitions,
            default_animation="idle",
            floor_y=self.ground_level
        )
        self.all_sprites.add(self.player)


        self.pancho = BossPancho(
            x=1000, 
            y=self.ground_level, 
            floor_y=self.ground_level, 
            player_target=self.player, 
            spritesheet=self.malla_pancho,
            visual_config=pancho_config,
            animation_data=pancho_definitions
        )
        self.all_sprites.add(self.pancho)

        self.enemies.add(self.pancho)

        self.camera = Camera(
            who=self.player,
            ancho_pantalla= screenancho,
            ancho_escenario=self.ancho_escenario
        )

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    self.next_scene="menu_principal"
                    

                self.player.player_attack(event)  # Tecla Z
                self.player.player_jump(event)    # Tecla X
                self.player.player_dashing(event) # Tecla C


    def update(self):
        keys=pygame.key.get_pressed()

        self.player.Running_player(keys)
        
        self.all_sprites.update()

        self.camera.update()
    def draw(self):

        offset = self.camera.offset_x

        if self.escenario:
            self.screen.blit(self.escenario, (-offset,0))
        else:
            self.screen.fill(blanco)

        for sprites in self.all_sprites:
            draw_rect = sprites.rect.move(-offset,9)
            self.screen.blit(sprites.image, draw_rect)
        
        #debug_player_rect = self.player.rect.move(-offset, 0)
        #pygame.draw.rect(self.screen, (255, 0, 0), debug_player_rect, 2)
        
        #debug_pancho_rect = self.pancho.rect.move(-offset, 0)
        #pygame.draw.rect(self.screen, (255, 0, 0), debug_pancho_rect, 2)

        self.pancho.draw_projectile(self.screen, offset)
