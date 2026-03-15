from settings import *

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
        

    def display_list(self):
        for index, monster in self.monster.items():
            top = self.main_rect.top + index * self.item_height
            item_rect = pygame.FRect(self.main_rect.left,top, self.list_width, self.item_height)

            text_surf = self.fonts['regular'].render(monster.name, False, COLORS['white'])
            text_rect = text_surf.get_frect(midleft = item_rect.midleft + vector(100, 0))

            pygame.draw.rect(self.display_surface, COLORS['light'], item_rect)
            self.display_surface.blit(text_surf, text_rect)
            icon_surf = self.monster_icons[monster.name]
            icon_rect = icon_surf.get_frect(midleft = item_rect.midleft + vector(20, 0))
            self.display_surface.blit(icon_surf, icon_rect)


    def update(self, dt):

        # draw background
        self.display_surface.blit(self.tint_surf, (0,0))
        pygame.draw.rect(self.display_surface, COLORS['dark'], self.main_rect)
        self.display_list()