import arcade
from pyglet.gl.lib import GLException

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "School's Out!"

# sprite constants
CHARACTER_SCALING = 0.25
TILE_SCALING = 0.5

PLAYER_MOVEMENT_SPEED = 5
UPDATES_PER_FRAME = 10
GRAVITY = 3
PLAYER_JUMP_SPEED = 40

RIGHT_FACING = 0
LEFT_FACING = 1

# Scrolling
LEFT_VIEWPORT_MARGIN = 250
RIGHT_VIEWPORT_MARGIN = 250
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 100


def load_texture_pair(filename):
    x = [
        arcade.load_texture(filename, can_cache=False),
        arcade.load_texture(filename, mirrored=True, can_cache=False)
    ]
    # print(f"{filename} Width: {x[0].width} Height: {x[0].height}, Mirrored: Width: {x[1].width} Height: {x[1].height}")

    return x

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.direction_facing = RIGHT_FACING
        self.current_texture = 0
        self.scale = CHARACTER_SCALING
        main_path = "./assets/characters/main_character"
        self.idle_texture_pair = load_texture_pair(f'{main_path}/idle (1).png')

        self.walk_textures = []
        for i in range(1, 15):
            texture = load_texture_pair(f'{main_path}/Walk ({i}).png')
            self.walk_textures.append(texture)

    def update_animation(self, delta_time: float=1/60):
        if self.change_x < 0 and self.direction_facing == RIGHT_FACING:
            self.direction_facing = LEFT_FACING
        elif self.change_x > 0 and self.direction_facing == LEFT_FACING:
            self.direction_facing = RIGHT_FACING

        if self.change_x == 0 and self.change_y == 0:
            self.texture = self.idle_texture_pair[self.direction_facing]
            return

        self.current_texture += 1
        if self.current_texture > 13 * UPDATES_PER_FRAME:
            self.current_texture = 0

        # print(f"{self.current_texture} // {UPDATES_PER_FRAME}: {self.current_texture // UPDATES_PER_FRAME}  {self.direction_facing}")
        try:
            self.texture = self.walk_textures[self.current_texture // UPDATES_PER_FRAME][self.direction_facing]
        except GLException:
            pass



class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        self.wall_list = None
        self.player_list = None
        self.floor = None
        self.background = None
        self.physics_engine = None
        self.player = None

        # used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

    def setup(self):
        """setup happens here"""
        self.background = arcade.load_texture("./assets/tiles/png/BG.png")
        print(self.background.width)

        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        # sets the floor
        for x in range(0, 8000, 64):
            wall = arcade.Sprite("./assets/tiles/png/tile/2.png", TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)
        self.floor = wall.height

        coordinate_list = [[512, self.floor],
                           [256, self.floor],
                           [768, self.floor]]

        for coordinate in coordinate_list:
            wall = arcade.Sprite("./assets/tiles/png/objects/crate.png", TILE_SCALING)
            wall.center_x, wall.bottom = coordinate
            self.wall_list.append(wall)

        # image_source = f"./assets/characters/main_character/idle (1).png"
        self.player = Player()
        self.player.center_x = 128
        # self.player_sprite.bottom = self.floor
        self.player.center_y = 32

        self.player_list.append(self.player)

        # map_name = "./assets/maps/map.tmx"
        # platforms_layer_name = 'Platforms'
        # my_map = arcade.tilemap.read_tmx(map_name)
        # self.wall_list = arcade.tilemap.process_layer(my_map, platforms_layer_name, TILE_SCALING)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, self.wall_list, GRAVITY)


    def on_draw(self):
        """rendering happens here"""

        arcade.start_render()
        # code to draw the screen goes here

        scale = SCREEN_WIDTH / self.background.width
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

        self.wall_list.draw()
        self.player_list.draw()

    def on_key_press(self, key, modifiers):

        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player.change_y = PLAYER_JUMP_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.change_x = 0

    def on_update(self, delta_time):

        self.player.update_animation()
        self.physics_engine.update()

        # track if we need to change the viewport
        changed = False

        # scroll left
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player.left < left_boundary and self.view_left > 0:
            self.view_left -= left_boundary - self.player.left
            changed = True

        # scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.player.right > right_boundary:
            self.view_left += self.player.right - right_boundary
            changed = True

        # scroll up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player.top > top_boundary:
            self.view_bottom += self.player.top - top_boundary
            changed = True

        # scroll down
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player.bottom
            changed = True

        if changed:
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            arcade.set_viewport(self.view_left, SCREEN_WIDTH + self.view_left,
                                self.view_bottom, SCREEN_HEIGHT + self.view_bottom)


def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == '__main__':
    main()