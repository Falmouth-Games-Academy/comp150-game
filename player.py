# Standard imports
import math

# Third party imports
import pygame
import Characters
import Map
import Objects


# Local imports (todo: remove these comments when we're all comfortable with
#                this ordering)


def distance((x1, y1), (x2, y2)):
    """Returns the distance between two points, in tile units"""
    return math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))


class Player(Character):
    max_speed = 7.0  # The maximum running speed, in tiles/sec
    acceleration = 35.0  # Rate of acceleration while running, in tiles/sec/sec
    friction = 90.0  # Rate of slowdown when releasing movement keys
    x_velocity = 0.0  # Rate of movement per axis in tiles/sec
    y_velocity = 0.0

    def __init__(self, x, y):
        """Init: Loads default player sprite and scales it up"""
        # Load character image
        self.sprite = pygame.image.load('graphics/game_character.png')
        self.sprite = self.sprite.convert(24)
        # Scale character so we can see his beauty
        self.sprite = pygame.transform.smoothscale(
                        self.sprite,
                        (MapClass.TILE_SIZE, MapClass.TILE_SIZE))
        self.x = x
        self.y = y
        self.collision.width = 1.0
        self.collision.height = 1.0
        self.collision.solid = True

    def update(self):
        global delta_time
        # Perform character movement
        key_pressed = pygame.key.get_pressed()

        # Make a normalised vector of movement based on user input
        move_x = 0.0
        move_y = 0.0
        if key_pressed[pygame.K_w]:
            move_y -= 1.0
        if key_pressed[pygame.K_s]:
            move_y += 1.0
        if key_pressed[pygame.K_d]:
            move_x += 1.0
        if key_pressed[pygame.K_a]:
            move_x -= 1.0

        vec_length = distance((0, 0), (move_x, move_y))
        # If the movement vector is nonzero, move; otherwise do friction
        # todo: determine why 'if vec_length is not 0.0' didn't work correctly
        if vec_length > 0.000:
            # Normalise
            move_x /= vec_length
            move_y /= vec_length

            # Accelerate according to the direction of the vector
            self.x_velocity += move_x * self.acceleration * delta_time
            self.y_velocity += move_y * self.acceleration * delta_time

            # Cap player max speed
            current_speed = distance((0, 0), (self.x_velocity, self.y_velocity))
            if current_speed > self.max_speed:
                self.x_velocity *= self.max_speed / current_speed
                self.y_velocity *= self.max_speed / current_speed
        else:
            # Normalise to friction speed at max
            current_speed = distance((0, 0),
                                (self.x_velocity, self.y_velocity))
            decel_speed = self.friction  # speed of deceleration

            # If the player is moving slower than the friction rate,
            # cut the deceleration rate down to simply cancel out movement
            if current_speed < decel_speed * delta_time:
                decel_speed = current_speed / delta_time

            if current_speed > 0:
                move_x = -self.x_velocity * decel_speed / current_speed
                move_y = -self.y_velocity * decel_speed / current_speed

            # Decelerate accordingly
            self.x_velocity += move_x * delta_time
            self.y_velocity += move_y * delta_time

        # Move player by velocity
        moved = self.move(self.x_velocity * delta_time,
                          self.y_velocity * delta_time)

        # Stop velocity if player collided with something
        if not moved:
            self.x_velocity = 0
            self.y_velocity = 0


class PikachuStatue(Object):
    def __init__(self, x, y):
        self.sprite = pygame.image.load('graphics/pikachu.png')
        self.sprite = pygame.transform.smoothscale(self.sprite,
                                                   (MapClass.TILE_SIZE, MapClass.TILE_SIZE))
        self.sprite = self.sprite.convert(24)
        self.x = x
        self.y = y
        self.collision.width = 1.0
        self.collision.height = 1.0
        self.collision.solid = True


