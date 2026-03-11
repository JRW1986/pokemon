from settings import *

class DialogTree:
    def __init__(self, character, player, all_sprites, fonts):
        self.player = player
        self.character = character
        self.font = fonts
        self.all_sprites = all_sprites

        self.dialogue = self.character.get_dialogue()
        self.dialogue_number =  len(self.dialogue)
        self.dialogue_index = 0

        self.current_dialogue = DialogSprite(self.dialogue[self.dialogue_index], self.character, self.all_sprites, self.font)
    
    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.current_dialogue.kill()
            self.dialogue_index += 1
            if self.dialogue_index < self.dialogue_number:
                self.current_dialogue = DialogSprite(self.dialogue[self.dialogue_index], self.character, self.all_sprites, self.font)
            else:
                pass

    def update(self):
        self.input()

class DialogSprite(pygame.sprite.Sprite):
    def __init__(self, message, character, groups, font):
        super().__init__(groups)
        self.z = WORLD_LAYERS['top']
        
        # text
        text_surf = font.render(message, False, COLORS['black'])
        padding = 5
        width = max(30,text_surf.get_width() + padding * 2)
        height = text_surf.get_height() + padding * 2

        # background
        surf = pygame.Surface((width, height), pygame.SRCALPHA)
        surf.fill((0,0,0,0))
        pygame.draw.rect(surf, COLORS['pure white'], surf.get_frect(topleft = (0, 0)), 0, 4)
        surf.blit(text_surf, text_surf.get_frect(center = (width / 2, height / 2)))

        self.image = surf
        self.rect = self.image.get_frect(midbottom = character.rect.midtop - vector(0, -10))