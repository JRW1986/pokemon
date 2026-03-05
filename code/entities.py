from settings import *

class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups):
        super().__init__(groups)

        # graphics setup
        self.frames = frames
        self.frame_index = 0

        # sprite setup
        self.image = self.frames['down'][self.frame_index]
        self.rect = self.image.get_frect(center = pos)

    def animate(self, dt):
        self.frame_index += ANIMATION_SPEED * dt
        self.image = self.frames['down'][int(self.frame_index) % len(self.frames['down'])]

    def update(self, dt):
        self.animate(dt)
        

class Player(Entity):
    def __init__(self, pos, frames, groups):
        super().__init__(pos, frames, groups)
        
        self.direction = vector()

    def input(self):
        keys = pygame.key.get_pressed()
        input_vector = vector()

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            input_vector.y -= 1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            input_vector.y += 1
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            input_vector.x -= 1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            input_vector.x += 1

        self.direction = input_vector

    def move(self, dt):
        self.rect.center += self.direction * 250 * dt

    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)