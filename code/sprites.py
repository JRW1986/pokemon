from turtle import pos

from settings import *
from random import uniform
from support import draw_bar
from game_data import MONSTER_DATA
from timer import Timer

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
    def __init__(self, pos, frames, groups, monster, index, pos_index, entity, apply_attack, create_monster):
        # data
        self.index = index
        self.pos_index = pos_index
        self.entity = entity
        self.monster = monster
        self.frames_index = 0
        self.frames = frames
        self.state = 'idle'
        self.animation_speed = ANIMATION_SPEED + uniform(-1, 1)
        self.z = BATTLE_LAYERS['monster']
        self.highlight = False
        self.target_sprite = None
        self.current_attack = None
        self.apply_attack = apply_attack
        self.create_monster = create_monster
        # sprite setup
        super().__init__(groups)
        self.image = self.frames[self.state][self.frames_index]
        self.rect = self.image.get_frect(center = pos)

        # timers
        self.timers = {
            'remove highlight': Timer(300, func = lambda: self.set_highlight(False)),
            'kill': Timer(600, func = self.destroy)
        }

    def animate(self, dt):
        self.frames_index += ANIMATION_SPEED * dt
        if self.state == 'attack' and self.frames_index >= len(self.frames['attack']):
            self.apply_attack(self.target_sprite, self.current_attack, self.monster.get_base_damage(self.current_attack))
            self.state = 'idle'
        
        self.adjusted_frame_index = int(self.frames_index) % len(self.frames[self.state])
        self.image = self.frames[self.state][self.adjusted_frame_index]

        if self.highlight:
            white_surf = pygame.mask.from_surface(self.image).to_surface()
            white_surf.set_colorkey('black')
            self.image = white_surf

    def set_highlight(self, value):
        self.highlight = value
        if value:
            self.timers['remove highlight'].activate()

    def activate_attack(self, target_sprite, attack):
        self.state = 'attack'
        self.frames_index = 0
        self.target_sprite = target_sprite
        self.current_attack = attack
        self.monster.reduce_energy(attack)

    def delayed_kill(self, new_monster):
        if not self.timers['kill'].active:
            self.next_monster_data = new_monster
            self.timers['kill'].activate()
    
    def destroy(self):
        if self.next_monster_data:
            self.create_monster(*self.next_monster_data)
        self.kill()

    def update(self, dt):
        for timer in self.timers.values():
            timer.update()
        self.animate(dt)
        self.monster.update(dt)

class MonsterOutlineSprite(pygame.sprite.Sprite):
    def __init__(self, monster_sprite, groups, frames):
        super().__init__(groups)
        self.z = BATTLE_LAYERS['outline']
        self.monster_sprite = monster_sprite
        self.frames = frames

        self.image = self.frames[self.monster_sprite.state][self.monster_sprite.frames_index]
        self.rect = self.image.get_frect(center = self.monster_sprite.rect.center)

    def update(self, _):
        self.image = self.frames[self.monster_sprite.state][self.monster_sprite.adjusted_frame_index]

class MonsterLevelSprite(pygame.sprite.Sprite):
    def __init__(self, pos, monster_sprite, font, groups):
        super().__init__(groups)
        self.monster_sprite = monster_sprite
        self.font = font
        self.pos = pos
        padding = 7
        self.z = BATTLE_LAYERS['name']
        
        text_surf = font.render(f"Lv. {monster_sprite.monster.level}", False, COLORS['black'])
        self.image = pygame.Surface((text_surf.get_width() + 2 * padding, text_surf.get_height() + 2 * padding))
        self.image.fill(COLORS['white'])
        self.image.blit(text_surf, (padding, padding))
        self.rect = self.image.get_rect(midbottom = self.pos)
        
    def update(self, _):
        padding = 7
        self.image.fill(COLORS['white'])
        
        text_surf = self.font.render(f"Lv. {self.monster_sprite.monster.level}", False, COLORS['black'])
        self.rect = self.image.get_rect(midbottom = self.pos)
        self.image.blit(text_surf, (padding, padding))
        
        self.xp_rect = pygame.FRect(0, self.rect.height - 2, self.rect.width, 2)
        draw_bar(self.image, self.xp_rect, self.monster_sprite.monster.xp, self.monster_sprite.monster.level_up, COLORS['black'], COLORS['white'], 0)

        if not self.monster_sprite.groups():
            self.kill()

class MonsterStatsSprite(pygame.sprite.Sprite):
    def __init__(self, pos, monster_sprite, size, groups, font):
        super().__init__(groups)
        self.monster_sprite = monster_sprite
        self.font = font
        self.image = pygame.Surface(size)
        self.rect = self.image.get_frect(midbottom = pos)
        self.z = BATTLE_LAYERS['overlay']

    def update(self, _):
        self.image.fill(COLORS['white'])

        for index, (value, max_value) in enumerate(self.monster_sprite.monster.get_info()):
            color = (COLORS['red'], COLORS['blue'], COLORS['gray'])[index]
            if index < 2: # health and energy
                text_surf = self.font.render(f"{int(value)} / {max_value}", False, COLORS['black'])
                text_rect = text_surf.get_frect(midleft = (10, 10 + index * 20))
                
                self.image.blit(text_surf, text_rect)
                bar_rect = draw_bar(self.image, pygame.FRect(0, 0, self.rect.width -15, 3).move(9, index * 20 + 18), value, max_value, color, COLORS['light-gray'], 2)
            else: # initiative
                initative_rect = pygame.FRect((0, self.rect.height - 2), (self.rect.width, 20))
                bar_rect = draw_bar(self.image, initative_rect, value, max_value, color, COLORS['white'], 0)
        
        if not self.monster_sprite.groups():
            self.kill()

class AttackSprite(AnimatedSprite):
    def __init__(self, pos, frames, groups):
        super().__init__(pos, frames, groups, z = BATTLE_LAYERS['overlay'])
        self.rect.center = pos

    def animate(self, dt):
        self.frames_index += ANIMATION_SPEED * dt
        if self.frames_index < len(self.frames):
            self.image = self.frames[int(self.frames_index)]
        else:
            self.kill()

    def update(self, dt):
        self.animate(dt)

class TimedSprite(Sprite):
    def __init__(self, pos, surf, groups, duration):
        super().__init__(pos, surf, groups, z = BATTLE_LAYERS['overlay'])
        self.rect.center = pos
        self.death_timer = Timer(duration, autostart = True, func = self.kill)

    def update(self, _):
        self.death_timer.update()