from settings import *
from sprites import MonsterSprite, MonsterLevelSprite, MonsterStatsSprite

class Battle:
    def __init__(self, player_monsters, opponent_monsters, monster_frames, bg_surf, fonts):
        # general
        self.display_surface = pygame.display.get_surface()
        self.bg_surf = bg_surf
        self.monster_frames = monster_frames
        self.fonts = fonts
        self.monster_data = {'player': player_monsters, 'opponent': opponent_monsters}
        self.frame_index = 0
        
        # groups
        self.battle_sprites = pygame.sprite.Group()
        self.player_sprites = pygame.sprite.Group()
        self.opponent_sprites = pygame.sprite.Group()
        
        self.setup()

    def setup(self):
        for entity, monsters in self.monster_data.items():
            for index, monster in {k:v for k,v in monsters.items() if k <= 2}.items():
                self.create_monster(monster, index, index, entity, 0)

    def create_monster(self, monster, index, pos_index, entity, dt):
        frames = self.monster_frames['monsters'][monster.name]
        self.frame_index += ANIMATION_SPEED * dt
       
        if entity == 'player':
            pos = list(BATTLE_POSITIONS['left'].values())[pos_index]
            groups = (self.battle_sprites, self.player_sprites)
            frames = {state: [pygame.transform.flip(frame, True, False) for frame in frames] for state, frames in frames.items()}
        else:
            pos = list(BATTLE_POSITIONS['right'].values())[pos_index]
            groups = (self.battle_sprites, self.opponent_sprites)
        
        monster_sprite =MonsterSprite(
            pos,
            frames,
            groups,
            monster,
            index,
            pos_index,
            entity
        )
        
        # ui
        level_pos = monster_sprite.rect.midleft + vector(-30, -30) if entity == 'player' else monster_sprite.rect.midright + vector(30, -30)
        stat_pos = monster_sprite.rect.bottomleft + vector(90, 35)
        MonsterLevelSprite(level_pos, monster_sprite, self.fonts['regular'], self.battle_sprites)
        MonsterStatsSprite(stat_pos, monster_sprite, self.fonts['regular'], self.battle_sprites)

    def update(self, dt):
        self.display_surface.blit(self.bg_surf, (0, 0))
        self.battle_sprites.update(dt)
        self.battle_sprites.draw(self.display_surface)