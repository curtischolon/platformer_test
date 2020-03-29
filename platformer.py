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


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        self.wall_list = None
        self.player_list = None

        # player
        self.player_sprite = None

        self.physics_engine = None

    def setup(self):
        """setup happens here"""
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        # sets the floor
        for x in range(0, 1250, 64):
            wall = arcade.Sprite("./assets/tiles/png/tile/2.png", TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)
        floor = wall.height

        coordinate_list = [[512, floor],
                           [256, floor],
                           [768, floor]]

        for coordinate in coordinate_list:
            wall = arcade.Sprite("./assets/tiles/png/objects/crate.png", TILE_SCALING)
            wall.center_x, wall.bottom = coordinate
            self.wall_list.append(wall)

        image_source = "./assets/characters/main_character/idle (1).png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 128
        self.player_sprite.bottom = self.ground

        self.player_list.append(self.player_sprite)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, GRAVITY)

    def on_draw(self):
        """rendering happens here"""

        arcade.start_render()
        # code to draw the screen goes here

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


def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == '__main__':
    main()