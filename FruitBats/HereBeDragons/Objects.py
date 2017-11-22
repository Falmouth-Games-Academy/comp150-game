import math

import pygame

from Map import MapClass, MAP
from Collision import CollisionBox
from Helpers import Vector


class Object:
    # Main variables for characters
    x = 0  # in game tile units (1.0 = 1 tile)
    y = 0  # in game tile units
    sprite = None  # current object sprite (todo: animations etc)
    collision = None  # collision data (None=no collision/ghost)
    sprite_angle = 0  # angle of rotation for this sprite in degrees
    sprite_origin = None  # origin of sprite
    debug_render_hitbox = False  # whether to render the hitbox (for debugging)
    debug_dyna = None

    def __init__(self, x, y):
        """Initialise object at the given position"""
        self.x = x
        self.y = y
        self.collision = CollisionBox((0.0, 0.0), (1.0, 1.0), True)

    def update(self, delta_time, player, object_list, map):
        self.debug_dyna = player.dynasword
        pass  # to be overloaded by objects

    def render(self, screen, camera):
        """Renders the object (function overloadable by subclasses)"""
        if self.sprite is not None:
            if self.sprite_angle is not 0:
                # Clamp sprite_angle to 0 <= x < 360 with math magic
                self.sprite_angle -= int(self.sprite_angle / 360) * 360
                if self.sprite_angle < 0:
                    self.sprite_angle -= int((self.sprite_angle / 360) - 1) \
                                            * 360
                # Draw rotated sprite
                rotated_sprite = pygame.transform.rotate(self.sprite,
                                                         self.sprite_angle)

                # Behold my somehow-rotate-around-an-origin code!
                # Declare X and Y position to draw at
                place_x = self.x * MAP.TILE_SIZE
                place_y = self.y * MAP.TILE_SIZE

                # Move back to centre of rotated image, which is always static
                place_x -= rotated_sprite.get_width() / 2
                place_y -= rotated_sprite.get_height() / 2

                # Find the centre of the original image
                centre_x = self.sprite.get_width() / 2
                centre_y = self.sprite.get_height() / 2

                if isinstance(self.sprite_origin, Vector):
                    # Perform a shift by the inverted origin, rotated
                    sine = math.sin(math.radians(self.sprite_angle))
                    cosine = math.cos(math.radians(self.sprite_angle))

                    # Shift along the X pixels by origin X
                    place_x -= cosine * (self.sprite_origin.x - centre_x)
                    place_y += sine * (self.sprite_origin.x - centre_x)
                    # Shift along the Y pixels by origin Y
                    place_x -= sine * (self.sprite_origin.y - centre_y)
                    place_y -= cosine * (self.sprite_origin.y - centre_y)

                # Blit!
                screen.blit(rotated_sprite,
                            (place_x - camera.x * MAP.TILE_SIZE,
                             place_y - camera.y * MAP.TILE_SIZE))
            else:
                if isinstance(self.sprite_origin, Vector):
                    # Draw sprite at origin
                    screen.blit(self.sprite, ((self.x - camera.x) * MAP.TILE_SIZE - self.sprite_origin.x, (self.y - camera.y) * MAP.TILE_SIZE - self.sprite_origin.y))
                else:
                    # Draw regular sprite
                    screen.blit(self.sprite,
                                ((self.x - camera.x) * MAP.TILE_SIZE,
                                 (self.y - camera.y) * MAP.TILE_SIZE))

        if self.debug_render_hitbox and self.collision:
            # Draw a collision box around the sprite
            # Prepare (potentially rotated) collision box vectors
            camera_vector = Vector(camera.x, camera.y)

            coll_origin = (Vector(self.x, self.y) - camera_vector) * MAP.TILE_SIZE + Vector(self.collision.x, self.collision.y)

            if self.sprite_origin:
                coll_origin -= self.get_right() * self.sprite_origin.x
                coll_origin -= self.get_down() * self.sprite_origin.y

            coll_right = self.get_right() * self.collision.width * MAP.TILE_SIZE
            coll_down = self.get_down() * self.collision.height * MAP.TILE_SIZE

            # Check collision with player dynasword
            if self.debug_dyna:
                other_coll_origin = Vector(self.debug_dyna.x, self.debug_dyna.y)

                if self.debug_dyna.sprite_origin:
                    other_coll_origin -= self.debug_dyna.get_right() * self.debug_dyna.sprite_origin.x
                    other_coll_origin -= self.debug_dyna.get_down() * self.debug_dyna.sprite_origin.y

                other_coll_right = self.debug_dyna.get_right() * self.debug_dyna.collision.width * MAP.TILE_SIZE
                other_coll_down = self.debug_dyna.get_down() * self.debug_dyna.collision.height * MAP.TILE_SIZE

            # Render sides of box
            # Draw pivot point
            vec = self.get_pos_at_pixel((self.sprite.get_width() / 2, 0)) - camera_vector
            vec2 = self.get_pos_at_pixel((self.sprite.get_width() / 2, self.sprite.get_height())) - camera_vector
            pygame.draw.line(screen, (0, 0, 255), tuple(vec * MAP.TILE_SIZE), tuple(vec2 * MAP.TILE_SIZE), 1)
            if self.sprite_origin:
                centre_point = (Vector(self.x, self.y) - camera_vector) * MAP.TILE_SIZE
                pygame.draw.circle(screen, (255, 0, 0), (int(centre_point.x), int(centre_point.y)), 3, 1)
            else:
                pygame.draw.circle(screen, (255, 0, 0), (int(coll_origin.x), int(coll_origin.y)), 3, 1)
            # Draw left
            pygame.draw.line(screen, (255, 0, 0), tuple(coll_origin), tuple(coll_origin + coll_down), 1)
            # Draw bottom
            pygame.draw.line(screen, (255, 0, 0), tuple(coll_origin + coll_down), tuple(coll_origin + coll_down + coll_right), 1)
            # Draw right
            pygame.draw.line(screen, (255, 0, 0), tuple(coll_origin + coll_down + coll_right), tuple(coll_origin + coll_right), 1)
            # Draw top
            pygame.draw.line(screen, (255, 0, 0), tuple(coll_origin + coll_right), tuple(coll_origin), 1)

            # Render bounding box
            if self.sprite_angle is not 0:
                x_off = (self.x - camera.x) * MAP.TILE_SIZE
                y_off = (self.y - camera.y) * MAP.TILE_SIZE
                bounds = self.collision.get_bounding_box(self.sprite_angle, self.sprite_origin)
                bounds_rect = pygame.Rect(x_off + bounds[0]*MAP.TILE_SIZE, y_off + bounds[1]*MAP.TILE_SIZE, (bounds[2] - bounds[0])*MAP.TILE_SIZE, (bounds[3] - bounds[1])*MAP.TILE_SIZE)
                pygame.draw.rect(screen, (0, 0, 0), bounds_rect, 1)

    def move(self, (move_x, move_y), object_list):
        """Performs collision checking and moves object by offset of
           move_x and move_y if possible

           (move_x, move_y) -- How far to move, in tile units
           object_list -- List of objects in the environment (for
                          collision)

           Todo: Push the player out of a surface in the opposite
           direction to their attempted movement, return a vector
           portraying how much they moved
        """

        # Decide where the object is (trying) to go
        desired_x = self.x + move_x
        desired_y = self.y + move_y
        collided = False

        # Perform collision detection with objects
        if self.collision and self.collision.solid:
            # Determine current area of our collision box
            if self.sprite_origin:
                self_box = self.collision.get_bounding_box(self.sprite_angle, tuple(self.sprite_origin), (self.x + move_x, self.y + move_y))
            else:
                self_box = self.collision.get_bounding_box(self.sprite_angle, (0, 0), (self.x + move_x, self.y + move_y))

            # Check with other objects
            for object in object_list:
                if object == self:
                    continue  # don't collide with yourself plz
                if not (object.collision and object.collision.solid):
                    continue  # don't collide with non-solids

                if object.sprite_origin:
                    obj_box = object.collision.get_bounding_box(object.sprite_angle, tuple(object.sprite_origin), (object.x, object.y))
                else:
                    obj_box = object.collision.get_bounding_box(object.sprite_angle, (0, 0), (object.x, object.y))

                if not (self_box[0] >= obj_box[2] or self_box[2] <= obj_box[0] or self_box[1] >= obj_box[3] or self_box[3] <= obj_box[1]):
                    desired_x = self.x
                    desired_y = self.y
                    collided = True

        self.x = desired_x
        self.y = desired_y
        return not collided

    def get_pos_at_pixel(self, (pixel_x, pixel_y)):
        """Converts a position within the object's sprite to its exact tile position on a map. Useful with rotatable objects.
            Arguments:
                (pixel_x, pixel_y) (float): X and Y position in the sprite
            Returns:
                (Vector) The position on the map
        """
        if self.sprite_origin is not None:
            if self.sprite_angle == 0.0:
                return Vector(self.x + (float(pixel_x) - self.sprite_origin.x) / MAP.TILE_SIZE, self.y + (float(pixel_y) - self.sprite_origin.y) / MAP.TILE_SIZE)
            else:
                vec = Vector(self.x, self.y)
                vec += self.get_right() * ((float(pixel_x - self.sprite_origin.x)) / MAP.TILE_SIZE)
                vec += self.get_down() * ((float(pixel_y - self.sprite_origin.y)) / MAP.TILE_SIZE)
                return vec
        else:
            if self.sprite_angle == 0.0:
                return Vector(self.x + float(pixel_x) / MAP.TILE_SIZE, self.y + float(pixel_y) / MAP.TILE_SIZE)
            else:
                vec = Vector(self.x, self.y)
                vec += self.get_right() * (float(pixel_x) / MAP.TILE_SIZE)
                vec += self.get_down() * (float(pixel_y) / MAP.TILE_SIZE)

    def get_down(self):
        """Returns local 'down' Vector according to sprite rotation. Default is 0,1"""
        return Vector(math.sin(math.radians(self.sprite_angle)), math.cos(math.radians(self.sprite_angle)))

    def get_right(self):
        """Returns local 'right' Vector according to sprite rotation. Default is 1,0"""
        return Vector(math.cos(math.radians(self.sprite_angle)), -math.sin(math.radians(self.sprite_angle)))