import arcade
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Arcade Space Shooter"
SCALE = 1.0


class FlyingSprite(arcade.Sprite):
    """
    Simple class for a sprite. We override update so that the sprite
    can self delete when it goes out of the screen.
    """
    def update(self):
        super().update()

        if self.right < 0:
            self.remove_from_sprite_lists()


class SpaceShooter(arcade.Window):
    """
    Main game window
    """
    def __init__(self, width, height, title):
        """
        Initialize the game
        """
        super().__init__(width, height, title)

        self.pause = False  # To be able to enter pause state
        self.collision = False  # Used to draw a game over text in on_draw

        # Declared in __init__ to satisfy PEP8.
        self.collision_sound = None
        self.move_down_sound = None
        self.move_up_sound = None
        self.background_music = None
        self.player = None

        # Create list for the game objects
        self.enemies_list = arcade.SpriteList()
        self.clouds_list = arcade.SpriteList()
        self.all_sprites = arcade.SpriteList()

    def setup(self):
        """
        Get the game ready to play.
        :return:
        """
        arcade.set_background_color(arcade.color.SKY_BLUE)

        # Set up the player
        self.player = arcade.Sprite("images/jet.png", SCALE)
        self.player.center_y = self.height / 2
        self.player.left = 10
        self.all_sprites.append(self.player)

        # Spawn a new enemy every 0.25 seconds
        arcade.schedule(self.add_enemy, 0.25)

        # Spawn a new cloud every second
        arcade.schedule(self.add_cloud, 1.0)

        # Setup the game sounds
        self.collision_sound = arcade.load_sound("sounds/Collision.wav")
        self.move_up_sound = arcade.load_sound("sounds/Rising_putter.wav")
        self.move_down_sound = arcade.load_sound("sounds/Falling_putter.wav")

        # Load background music.
        self.background_music = arcade.load_sound("sounds/Apoxode_-_Electric_1.wav")
        arcade.play_sound(self.background_music)

    def add_enemy(self, delta_time: float):
        """
        Called by scheduler to add an enemy on the screen.
        :param delta_time: Time elapsed.
        :return: None
        """
        if self.pause:
            return

        enemy = FlyingSprite("images/missile.png", SCALE)
        enemy.left = random.randint(self.width, self.width + 80)
        enemy.top = random.randint(10, self.height - 10)
        enemy.velocity = (random.randint(-20, -5), 0)

        self.enemies_list.append(enemy)
        self.all_sprites.append(enemy)

    def add_cloud(self, delta_time: float):
        """
        Called by the scheduler to add a cloud on the screen.
        :param delta_time: Time elapsed
        :return: None
        """
        if self.pause:
            return

        cloud = FlyingSprite("images/cloud.png", SCALE)
        cloud.left = random.randint(self.width, self.width + 80)
        cloud.top = random.randint(10, self.height - 10)
        cloud.velocity = (random.randint(-5, -2), 0)

        self.clouds_list.append(cloud)
        self.all_sprites.append(cloud)

    def on_draw(self):
        """
        Called whenever you need to draw your window
        :return:
        """
        # Clear the screen and start drawing
        arcade.start_render()

        self.all_sprites.draw()

        # If we detected a collision, show a message
        if self.collision:
            arcade.draw_text("BOOM! A missile hit you. GAME OVER",
                             100,
                             self.height / 2,
                             (255, 0, 0),
                             24,
                             0)
            self.pause = True

    def on_update(self, delta_time: float):
        # If pause, don't do anything
        if self.pause:
            return

        # Check to see if player moves off screen
        if self.player.top > self.height:
            self.player.top = self.height
        if self.player.right > self.width:
            self.player.right = self.width
        if self.player.left < 0:
            self.player.left = 0
        if self.player.bottom < 0:
            self.player.bottom = 0

        # Collision detection
        if len(self.player.collides_with_list(self.enemies_list)) > 0:
            self.collision = True
            arcade.play_sound(self.collision_sound)

        # Update everything
        for sprite in self.all_sprites:
            sprite.center_x = int(sprite.center_x + sprite.change_x * delta_time)
            sprite.center_y = int(sprite.center_y + sprite.change_y * delta_time)

    def on_key_press(self, symbol: int, modifiers: int):
        """
        Handles user input from the keyboard.
        Q/Esc: quit game
        P: Pause/unpause the game
        W/A/S/D + arrow keys: move the player

        Arguments:
            symbol {int} -- which key was pressed
            modifiers {int} -- which modifiers were pressed
        """
        if symbol == arcade.key.Q or symbol == arcade.key.ESCAPE:
            # Quit immediately
            arcade.close_window()

        if symbol == arcade.key.P:
            self.pause = not self.pause

        if symbol == arcade.key.UP or symbol == arcade.key.W:
            self.player.change_y = 5
            arcade.play_sound(self.move_up_sound)

        if symbol == arcade.key.DOWN or symbol == arcade.key.S:
            self.player.change_y = -5
            arcade.play_sound(self.move_down_sound)

        if symbol == arcade.key.LEFT or symbol == arcade.key.A:
            self.player.change_x = -5

        if symbol == arcade.key.RIGHT or symbol == arcade.key.D:
            self.player.change_x = 5

    def on_key_release(self, symbol: int, modifiers: int):
        """
        Undo the movement vectors when movement keys are released.

        Arguments:
            symbol {int} -- which key was released
            modifiers {int} -- which modifiers were pressed.
        """
        if (
            symbol == arcade.key.W
            or symbol == arcade.key.S
            or symbol == arcade.key.UP
            or symbol == arcade.key.DOWN
        ):
            self.player.change_y = 0

        if (
            symbol == arcade.key.A
            or symbol == arcade.key.D
            or symbol == arcade.key.LEFT
            or symbol == arcade.key.RIGHT
        ):
            self.player.change_x = 0            


if __name__ == "__main__":
    app = SpaceShooter(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    app.setup()
    arcade.run()
