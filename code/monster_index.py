from settings import *
from timer import Timer

class MonsterIndex:
    def __init__(self, monster, fonts, monster_frames):
        self.display_surface = pygame.display.get_surface()
        self.fonts = fonts
        self.monster = monster
        self.monster_frames = monster_frames

        # frame
        self.monster_icons = self.monster_frames['icons']

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
        # main bg
        rect = pygame.FRect(self.main_rect.left + self.list_width, self.main_rect.top, self.main_rect.width - self.list_width, self.main_rect.height)
        pygame.draw.rect(self.display_surface, COLORS['dark'], rect)

    def update(self, dt):
        self.timer['nav'].update()
        self.timer['select'].update()
        self.input()
        # draw background
        self.display_surface.blit(self.tint_surf, (0,0))
        self.display_list()
        self.display_main(dt)