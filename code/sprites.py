from turtle import pos

from settings import *
from random import uniform
from support import draw_bar

# overworld sprites
class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z = WORLD_LAYERS['main']):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = z
        self.y_sort = self.rect.centery
        self.hitbox = self.rect.copy()

class BorderSprite(Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)
        self.hitbox = self.rect.copy()

class TransitionSprite(Sprite):
    def __init__(self, pos, size, target, groups):
        surf = pygame.Surface(size)
        super().__init__(pos, surf, groups)
        self.target = target

class CollisionSprite(Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)
        self.hitbox = self.rect.inflate(0, -self.rect.height * 0.4)

class CollisionTreeSprite(Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)
        self.hitbox = self.rect.inflate(-self.rect.width * 0.5, -self.rect.height * 0.7)
        self.hitbox.center = self.rect.center - vector(0, 20)

class MonsterPatchSprite(Sprite):
    def __init__(self, pos, surf, groups, biome):
        super().__init__(pos, surf, groups, z = WORLD_LAYERS['main'] if biome != 'sand' else WORLD_LAYERS['bg'])
        self.y_sort -= 40
        self.biome = biome

class AnimatedSprite(Sprite):
    def __init__(self, pos, frames, groups, z = WORLD_LAYERS['main']):
        self.frames_index, self.frames = 0, frames
        super().__init__(pos, frames[0], groups, z)

    def animate(self, dt):
        self.frames_index += ANIMATION_SPEED * dt
        self.image = self.frames[int(self.frames_index) % len(self.frames)]
        
    def update(self, dt):
        self.animate(dt)

# battle sprites
class MonsterSprite(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, monster, index, pos_index, entity):
        # data
        self.index = index
        self.pos_index = pos_index
        self.entity = entity
        self.monster = monster
        self.frames_index = 0
        self.frames = frames
        self.state = 'idle'
        self.animation_speed = ANIMATION_SPEED + uniform(-1, 1)

        # sprite setup
        super().__init__(groups)
        self.image = self.frames[self.state][self.frames_index]
        self.rect = self.image.get_frect(center = pos)

    def animate(self, dt):
        self.frames_index += ANIMATION_SPEED * dt
        self.image = self.frames[self.state][int(self.frames_index) % len(self.frames[self.state])]

    def update(self, dt):
        self.animate(dt)

class MonsterLevelSprite(pygame.sprite.Sprite):
    def __init__(self, pos, monster_sprite, font, groups):
        super().__init__(groups)
        self.monster_sprite = monster_sprite
        self.font = font
        self.pos = pos
        padding = 7

        text_surf = font.render(f"Lv. {monster_sprite.monster.level}", False, COLORS['black'])
        self.image = pygame.Surface((text_surf.get_width() + 2 * padding, text_surf.get_height() + 2 * padding))
        self.image.fill(COLORS['white'])
        self.image.blit(text_surf, (padding, padding))
        self.rect = self.image.get_rect(midbottom = self.pos)
        self.xp_rect = pygame.FRect(0, self.rect.height - 2, self.rect.width, 2)

    def update(self, _):
        padding = 7
        self.image.fill(COLORS['white'])
        
        text_surf = self.font.render(f"Lv. {self.monster_sprite.monster.level}", False, COLORS['black'])
        self.rect = self.image.get_rect(midbottom = self.pos)
        self.image.blit(text_surf, (padding, padding))
        
        draw_bar(self.image, self.xp_rect, self.monster_sprite.monster.xp, self.monster_sprite.monster.level_up, COLORS['black'], COLORS['white'], 0)


class MonsterStatsSprite(pygame.sprite.Sprite):
    def __init__(self, pos, monster_sprite, size, font, groups):
        super().__init__(groups)
        self.monster_sprite = monster_sprite
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect(midbottom = pos)

        text_surf = font.render(f"HP: {monster_sprite.monster.health}", False, COLORS['black'])
        padding = 15

        
        self.image.fill(COLORS['white'])
        self.image.blit(text_surf, (padding, padding))
        self.rect = self.image.get_rect(midbottom = pos)
