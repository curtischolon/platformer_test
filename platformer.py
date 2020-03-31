import arcade


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "School's Out!"

# sprite constants
CHARACTER_SCALING = 0.25
TILE_SCALING = 0.5

PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 3
PLAYER_JUMP_SPEED = 40

# Scrolling
LEFT_VIEWPORT_MARGIN = 250
RIGHT_VIEWPORT_MARGIN = 250
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 100


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        self.wall_list = None
        self.player_list = None
        self.floor = None

        self.background = None
        # player
        self.player_sprite = None

        self.physics_engine = None

        # used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

    def setup(self):
        """setup happens here"""
        self.background = arcade.load_texture("./assets/tiles/png/BG.png")

        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        # sets the floor
        for x in range(0, 1250, 64):
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

        image_source = "./assets/characters/main_character/idle (1).png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 128
        # self.player_sprite.bottom = self.floor
        self.player_sprite.center_y = 32

        self.player_list.append(self.player_sprite)

        # map_name = "./assets/maps/map.tmx"
        # platforms_layer_name = 'Platforms'
        # my_map = arcade.tilemap.read_tmx(map_name)
        # self.wall_list = arcade.tilemap.process_layer(my_map, platforms_layer_name, TILE_SCALING)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, GRAVITY)

    def on_draw(self):
        """rendering happens here"""

        arcade.start_render()
        # code to draw the screen goes here

        scale = SCREEN_WIDTH / self.background.width
        arcade.draw_lrwh_rectangle_textured(-300, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

        self.wall_list.draw()
        self.player_list.draw()

    def on_key_press(self, key, modifiers):

        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):

        self.physics_engine.update()

        # track if we need to change the viewport
        changed = False

        # scroll left
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary and self.view_left > 0:
            self.view_left -= left_boundary - self.player_sprite.left
            changed = True

        # scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed = True

        # scroll up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed = True

        # scroll down
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
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