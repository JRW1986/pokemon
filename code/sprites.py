from settings import *
from random import uniform

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