from settings import *
from timer import Timer
from support import draw_bar
from game_data import MONSTER_DATA, ATTACK_DATA

class MonsterIndex:
    def __init__(self, monster, fonts, monster_frames):
        self.display_surface = pygame.display.get_surface()
        self.fonts = fonts
        self.monster = monster
        self.monster_frames = monster_frames
        self.frame_index = 0

        # frame
        self.monster_icons = self.monster_frames['icons']
        self.monster_frame = self.monster_frames['monsters']
        self.ui_frames = self.monster_frames['ui']

        # tint surf
        self.tint_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.tint_surf.set_alpha(200)

        # dimensions
        self.main_rect = pygame.FRect(0,0, WINDOW_WIDTH * 0.6, WINDOW_HEIGHT * 0.8).move_to(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

        # list of monsters
        self.visible_items = 6
        self.list_width = self.main_rect.width * 0.3
        self.item_height = self.main_rect.height / self.visible_items
        self.index = 0
        self.selected_index = None

        # max value for bars
        self.max_stats = {}
        for data in MONSTER_DATA.values():
            for stat, value in data['stats'].items():
                if stat != 'element':
                    if stat not in self.max_stats:
                        self.max_stats[stat] = value
                    else:
                        self.max_stats[stat] = value if value > self.max_stats[stat] else self.max_stats[stat]
        self.max_stats['health'] = self.max_stats.pop('max_health')
        self.max_stats['energy'] = self.max_stats.pop('max_energy')

        # timer
        self.timer = {
            'nav': Timer(200, repeat = False),
            'select': Timer(200, repeat = False)
        }

    def input(self):
        keys = pygame.key.get_pressed()

        if (keys[pygame.K_UP] or keys[pygame.K_w]) and not self.timer['nav'].active:
            self.index -= 1
            self.timer['nav'].activate()
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and not self.timer['nav'].active:
            self.index += 1
            self.timer['nav'].activate()
        if keys[pygame.K_SPACE] and not self.timer['select'].active:
            if self.selected_index != None:
                selected_monster = self.monster[self.selected_index]
                current_monster = self.monster[self.index]
                self.monster[self.index] = selected_monster
                self.monster[self.selected_index] = current_monster
                self.selected_index = None
                self.timer['select'].activate()
            else:
                self.selected_index = self.index
                self.timer['select'].activate()
                 
                
        self.index = self.index % len(self.monster)

    def display_list(self):
        bg_rect = pygame.FRect(self.main_rect.left, self.main_rect.top, self.list_width, self.main_rect.height)
        pygame.draw.rect(self.display_surface, COLORS['dark'], bg_rect, 0,12,0,12,0)
        
        v_offset = 0 if self.index < self.visible_items else -(self.index - self.visible_items + 1) * self.item_height
        for index, monster in self.monster.items():
            # colors
            bg_color = COLORS['gray'] if self.index != index else COLORS['light']
            text_color = COLORS['white'] if self.selected_index != index else COLORS['gold']

            top = self.main_rect.top + index * self.item_height + v_offset
            item_rect = pygame.FRect(self.main_rect.left,top, self.list_width, self.item_height)

            text_surf = self.fonts['regular'].render(monster.name, False, text_color)
            text_rect = text_surf.get_frect(midleft = item_rect.midleft + vector(100, 0))

            icon_surf = self.monster_icons[monster.name]
            icon_rect = icon_surf.get_frect(midleft = item_rect.midleft + vector(20, 0))

            if item_rect.colliderect(self.main_rect):
                # check corners
                if item_rect.collidepoint(self.main_rect.topleft):
                    pygame.draw.rect(self.display_surface, bg_color, item_rect,0,0,12)
                elif item_rect.collidepoint(self.main_rect.bottomleft + vector(1,-1)):
                    pygame.draw.rect(self.display_surface, bg_color, item_rect,0,0,0,0,12,0)
                else:
                    pygame.draw.rect(self.display_surface, bg_color, item_rect)
                    
                self.display_surface.blit(text_surf, text_rect)
                self.display_surface.blit(icon_surf, icon_rect)

        # shadow
        shadow_surf = pygame.Surface((4, self.main_rect.height))
        shadow_surf.set_alpha(100)
        self.display_surface.blit(shadow_surf, (self.main_rect.left + self.list_width - 4, self.main_rect.top))

        # divider
        for i in range(min(self.visible_items, len(self.monster))):
            y = self.main_rect.top + self.item_height * i
            left = self.main_rect.left
            right = self.main_rect.left + self.list_width
            pygame.draw.line(self.display_surface, COLORS['light-gray'], (left, y), (right, y))

    def display_main(self, dt):
        # data
        monster = self.monster[self.index]

        # main bg
        rect = pygame.FRect(self.main_rect.left + self.list_width, self.main_rect.top, self.main_rect.width - self.list_width, self.main_rect.height)
        pygame.draw.rect(self.display_surface, COLORS['dark'], rect, 0,12,0,12,0)
        pygame.draw.rect(self.display_surface, COLORS['light-gray'], rect, 4,12,0,12,0)

        # monster display
        top_rect = pygame.FRect(rect.left, rect.top, rect.width, rect.height * 0.4)
        pygame.draw.rect(self.display_surface, COLORS[monster.element], top_rect, 0,0,0,12)
        
        # monster image
        self.frame_index += ANIMATION_SPEED * dt

        monster_surf = self.monster_frame[monster.name]['idle'][int(self.frame_index) % len(self.monster_frame[monster.name]['idle'])]
        monster_rect = monster_surf.get_frect(center = top_rect.center)
        self.display_surface.blit(monster_surf, monster_rect)

        # monster name
        name_surf = self.fonts['bold'].render(monster.name, False, COLORS['white'])
        name_rect = name_surf.get_frect(topleft = top_rect.topleft + vector(10, 10))
        self.display_surface.blit(name_surf, name_rect)

        # monster level
        level_surf = self.fonts['regular'].render(f'Level {monster.level}', False, COLORS['white'])
        level_rect = level_surf.get_frect(bottomleft = top_rect.bottomleft + vector(10, -16))
        self.display_surface.blit(level_surf, level_rect)
        draw_bar(
            surf = self.display_surface,
            rect = pygame.FRect(level_rect.bottomleft, (100, 4)),
            value = monster.xp,
            max_value = monster.level_up,
            color = COLORS['white'],
            bg_color = COLORS['dark']
        )

        # element
        element_surf = self.fonts['regular'].render(f'Element: {monster.element.capitalize()}', False, COLORS['white'])
        element_rect = element_surf.get_frect(bottomright = top_rect.bottomright + vector(-10,-10))
        self.display_surface.blit(element_surf, element_rect)

        # health and energy
        bar_data = {
            'width': rect.width * 0.45,
            'height': 30,
            'top': top_rect.bottom + rect.width * 0.03,
            'left_side': rect.left + rect.width / 4
        }

        # health
        healthbar_rect = pygame.FRect((0,0), (bar_data['width'], bar_data['height'])).move_to(midtop = (bar_data['left_side'], bar_data['top']))
        draw_bar(
            surf = self.display_surface,
            rect = healthbar_rect,
            value = monster.health,
            max_value = monster.get_stat('max_health'),
            color = COLORS[monster.element],
            bg_color = COLORS['black']
        )
        hp_text = self.fonts['regular'].render(f'HP: {monster.health} / {monster.get_stat("max_health")}', False, COLORS['white'])
        hp_rect = hp_text.get_frect(midleft = healthbar_rect.midleft + vector(10, 0))
        self.display_surface.blit(hp_text, hp_rect)

        # energy
        energybar_rect = pygame.FRect((0,0), (bar_data['width'], bar_data['height'])).move_to(topleft = (healthbar_rect.left, healthbar_rect.bottom + bar_data['height'] * 0.5))
        draw_bar(
            surf = self.display_surface,
            rect = energybar_rect,
            value = monster.energy,
            max_value = monster.get_stat('max_energy'),
            color = COLORS['light'],
            bg_color = COLORS['black']
        )
        energy_text = self.fonts['regular'].render(f'Energy: {monster.energy} / {monster.get_stat("max_energy")}', False, COLORS['white'])
        energy_rect = energy_text.get_frect(midleft = energybar_rect.midleft + vector(10, 0))
        self.display_surface.blit(energy_text, energy_rect)

        # info
        sides = {'left': healthbar_rect.left, 'right': element_rect.right}
        info_height = rect.bottom - energybar_rect.bottom

        # stats
        stats_rect = pygame.FRect(sides['left'], energybar_rect.bottom, healthbar_rect.width, info_height).inflate(0, -15)
        pygame.draw.rect(self.display_surface, COLORS['light-gray'], stats_rect)
        stats_text_surf = self.fonts['regular'].render('Stats:', False, COLORS['white'])
        stats_text_rect = stats_text_surf.get_frect(topleft = stats_rect.topleft + vector(5, 0))
        self.display_surface.blit(stats_text_surf, stats_text_rect)

        monster_stats = monster.get_stats()
        stat_height = stats_rect.height / len(monster_stats)

        for index, (stat, value) in enumerate(monster_stats.items()):
            single_stat_rect = pygame.FRect(stats_rect.left, stats_rect.top + (index + 1) * stat_height / 1.11, stats_rect.width, stat_height)
            
            # icon
            icon_surf = self.ui_frames[stat]
            icon_rect = icon_surf.get_frect(midleft = single_stat_rect.midleft + vector(5, -17)).inflate(0, 7)
            self.display_surface.blit(icon_surf, icon_rect)

            # text
            stat_text = self.fonts['regular'].render(f'{stat.capitalize()}: {value}', False, COLORS['white'])
            stat_text_rect = stat_text.get_frect(topleft = single_stat_rect.topleft + vector(25, -16)).inflate(0, -8)
            self.display_surface.blit(stat_text, stat_text_rect)

            # bar
            bar_rect = pygame.FRect((0,0), (single_stat_rect.width - 10, 6)).move_to(bottomleft = single_stat_rect.bottomleft + vector(5, -21))
            draw_bar(
                surf = self.display_surface,
                rect = bar_rect,
                value = value,
                max_value = self.max_stats[stat] * monster.level,
                color = COLORS[monster.element],
                bg_color = COLORS['dark']
            )

            # abilities
            abilities_rect = pygame.FRect(sides['right'] - healthbar_rect.width - 13, energybar_rect.bottom - 41, healthbar_rect.width, info_height).inflate(20, 66)
            pygame.draw.rect(self.display_surface, COLORS['light-gray'], abilities_rect)
            abilities_text_surf = self.fonts['regular'].render('Abilities:', False, COLORS[COLORS['white']])
            abilities_text_rect = abilities_text_surf.get_frect(topleft = abilities_rect.topleft + vector(5, 0))
            self.display_surface.blit(abilities_text_surf, abilities_text_rect)

            for index, ability in enumerate(monster.get_abilities()):
                element = ATTACK_DATA[ability]['element']

                text_surf = self.fonts['regular'].render(ability, False, COLORS['black'])
                x = abilities_rect.left + index % 2 * abilities_rect.width / 2
                y = 29 + abilities_rect.top + int(index / 2) * (text_surf.get_height() + 25)
                text_rect = text_surf.get_frect(topleft = (x + 15, y))
                pygame.draw.rect(self.display_surface, COLORS[element], text_rect.inflate(10, 10), 0, 4)
                self.display_surface.blit(text_surf, text_rect)

    def update(self, dt):
        self.timer['nav'].update()
        self.timer['select'].update()
        self.input()
        # draw background
        self.display_surface.blit(self.tint_surf, (0,0))
        self.display_list()
        self.display_main(dt)
