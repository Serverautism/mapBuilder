import pygame
import copy


class Game:
    def __init__(self):
        pygame.init()

        self.running = True

        self.colors = {
            'finished': (74, 78, 105),
            'current': (154, 140, 152),
            'background': (242, 233, 228),
            'text': (231, 111, 81),
            'points': (201, 173, 167)
        }

        self.font = pygame.font.SysFont('Arial', 20)

        self.fps = 60
        self.clock = pygame.time.Clock()

        self.screen_width, self.screen_height = 1920, 1080
        self.screen_dimensions = (self.screen_width, self.screen_height)
        self.screen = pygame.display.set_mode(self.screen_dimensions)

        self.render_width, self.render_height = 1920, 1080
        self.render_dimensions = (self.render_width, self.render_height)
        self.render_surface = pygame.Surface(self.render_dimensions)

        self.point_rect_width = 10
        self.grid_size = 16
        self.min_grid_size = 8
        self.show_grid = False
        self.show_menu = True
        self.snap_to_grid = False

        self.all_polygons = []
        self.current_polygon = []

    def run(self):
        while self.running:
            self.clock.tick(self.fps)
            self.handle_input()

            self.draw_polygons()
            self.draw_current_polygon()

            if self.show_grid:
                self.draw_grid()

            self.render_surface.blit(self.font.render('M: toggle menu'.format(self.grid_size), True, self.colors['text']), (5, 5))

            if self.show_menu:
                self.render_surface.blit(self.font.render('grid size: {} (+/-)'.format(self.grid_size), True, self.colors['text']), (5, 25))
                self.render_surface.blit(self.font.render('G: toggle grid'.format(self.grid_size), True, self.colors['text']), (5, 45))
                self.render_surface.blit(self.font.render('S: snap to grid: {}'.format(self.snap_to_grid), True, self.colors['text']), (5, 65))
                self.render_surface.blit(self.font.render('N: start new obstacle'.format(self.point_rect_width), True, self.colors['text']), (5, 85))
                self.render_surface.blit(self.font.render('R: restart current obstacle'.format(self.point_rect_width), True, self.colors['text']), (5, 105))
                self.render_surface.blit(self.font.render('U: undo last obstacle'.format(self.point_rect_width), True, self.colors['text']), (5, 125))
                self.render_surface.blit(self.font.render('DEL: clear map'.format(self.point_rect_width), True, self.colors['text']), (5, 145))
                self.render_surface.blit(self.font.render('P: print finished map'.format(self.point_rect_width), True, self.colors['text']), (5, 165))

            self.screen.blit(pygame.transform.scale(self.render_surface, self.screen_dimensions), (0, 0))
            pygame.display.update()
            self.render_surface.fill(self.colors['background'])

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

                elif event.key == pygame.K_n:
                    self.flush_current()

                elif event.key == pygame.K_p:
                    self.output_map()

                elif event.key == pygame.K_DELETE:
                    self.reset()

                elif event.key == pygame.K_u:
                    self.all_polygons.pop(-1)

                elif event.key == pygame.K_r:
                    self.current_polygon.clear()

                elif event.key == pygame.K_PLUS:
                    self.grid_size += 1

                elif event.key == pygame.K_MINUS:
                    self.grid_size -= 1
                    if self.grid_size < self.min_grid_size:
                        self.grid_size = self.min_grid_size

                elif event.key == pygame.K_g:
                    if self.show_grid:
                        self.show_grid = False
                    else:
                        self.show_grid = True

                elif event.key == pygame.K_m:
                    if self.show_menu:
                        self.show_menu = False
                    else:
                        self.show_menu = True

                elif event.key == pygame.K_s:
                    if self.snap_to_grid:
                        self.snap_to_grid = False
                    else:
                        self.snap_to_grid = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.snap_to_grid:
                        x = round(event.pos[0] / self.grid_size) * self.grid_size
                        y = round(event.pos[1] / self.grid_size) * self.grid_size
                        self.current_polygon.append((x, y))
                    else:
                        self.current_polygon.append(event.pos)

    def draw_polygons(self):
        for poly in self.all_polygons:
            pygame.draw.polygon(self.render_surface, self.colors['finished'], poly)

    def draw_current_polygon(self):
        if len(self.current_polygon) > 2:
            pygame.draw.polygon(self.render_surface, self.colors['current'], self.current_polygon)

        for point in self.current_polygon:
            pygame.draw.circle(self.render_surface, self.colors['points'], point, int(self.point_rect_width/2))

    def draw_grid(self):
        for i in range(0, self.render_height, self.grid_size):
            for j in range(0, self.render_width, self.grid_size):
                pygame.draw.rect(self.render_surface, self.colors['points'], (j, i, self.grid_size, self.grid_size), width=1)

    def output_map(self):
        print('\n[')
        for i, poly in enumerate(self.all_polygons):
            if i == len(self.all_polygons) - 1:
                print(poly)
            else:
                print(str(poly) + ',')
        print(']')

    def reset(self):
        self.current_polygon.clear()
        self.all_polygons.clear()

    def flush_current(self):
        if len(self.current_polygon) > 2:
            self.all_polygons.append(copy.deepcopy(self.current_polygon))
            self.current_polygon = []
        else:
            print('ERROR: not enough points set...')


if __name__ == '__main__':
    app = Game()
    app.run()
