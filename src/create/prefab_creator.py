import math
import random
import pygame
import esper
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_input_command import CInputCommand

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_player import CTagPlayer


def create_square(world: esper.World, size: pygame.Vector2,
                  pos: pygame.Vector2, vel: pygame.Vector2, col: pygame.Color) -> int:
    cuad_entity = world.create_entity()
    world.add_component(cuad_entity,
                        CSurface(size, col))
    world.add_component(cuad_entity,
                        CTransform(pos))
    world.add_component(cuad_entity,
                        CVelocity(vel))
    return cuad_entity


def create_enemy_square(world: esper.World, pos: pygame.Vector2, enemy_info: dict):
    size = pygame.Vector2(enemy_info["size"]["x"],
                          enemy_info["size"]["y"])
    color = pygame.Color(enemy_info["color"]["r"],
                         enemy_info["color"]["g"],
                         enemy_info["color"]["b"])
    vel_max = enemy_info["velocity_max"]
    vel_min = enemy_info["velocity_min"]
    if vel_max == vel_min:
        vel_range = vel_min
    else:
        vel_range = random.randrange(vel_min, vel_max)
    velocity = pygame.Vector2(random.choice([-vel_range, vel_range]),
                              random.choice([-vel_range, vel_range]))
    enemy = create_square(world, size, pos, velocity, color)
    world.add_component(enemy, CTagEnemy())


def create_player_square(world: esper.World, player_info: dict, player_lvl_info: dict) -> int:
    size = pygame.Vector2(player_info["size"]["x"],
                          player_info["size"]["y"])
    color = pygame.Color(player_info["color"]["r"],
                         player_info["color"]["g"],
                         player_info["color"]["b"])
    pos = pygame.Vector2(player_lvl_info["position"]["x"] - size.x / 2,
                         player_lvl_info["position"]["y"] - size.y / 2)
    # print(pos)
    vel = pygame.Vector2(0, 0)
    player = create_square(world, size, pos, vel, color)
    world.add_component(player, CTagPlayer())
    return player


def create_enemy_spawner(world: esper.World, level_data: dict):
    spawner_entity = world.create_entity()
    world.add_component(spawner_entity,
                        CEnemySpawner(level_data["enemy_spawn_events"]))


def create_input_player(world: esper.World):
    input_left = world.create_entity()
    input_right = world.create_entity()
    input_up = world.create_entity()
    input_down = world.create_entity()
    input_l_click = world.create_entity()

    world.add_component(input_left, CInputCommand(
        "PLAYER_LEFT", pygame.K_LEFT))
    world.add_component(input_right, CInputCommand(
        "PLAYER_RIGHT", pygame.K_RIGHT))
    world.add_component(input_up, CInputCommand(
        "PLAYER_UP", pygame.K_UP))
    world.add_component(input_down, CInputCommand(
        "PLAYER_DOWN", pygame.K_DOWN))
    world.add_component(input_l_click, CInputCommand(
        "PLAYER_FIRE", pygame.mouse.get_pressed()[0]))


def create_bullet_square(world: esper.World, bullet_info: dict, player: int, mouse_pos: pygame.Vector2, max_bullets: int):
    if len(world.get_component(CTagBullet)) < max_bullets:
        size = pygame.Vector2(bullet_info["size"]["x"],
                            bullet_info["size"]["y"])
        color = pygame.Color(bullet_info["color"]["r"],
                            bullet_info["color"]["g"],
                            bullet_info["color"]["b"])
        velocity = bullet_info["velocity"]

        player_surface = world.component_for_entity(player, CSurface)
        player_transform = world.component_for_entity(player, CTransform)
        player_pos = player_surface.surf.get_rect(topleft=player_transform.pos).center
        # print(player_pos , mouse_pos)

        angle = math.atan2(mouse_pos[1] - player_pos[1], mouse_pos[0] - player_pos[0])
        # print("angle", angle)
        vel = pygame.Vector2(velocity * math.cos(angle), velocity * math.sin(angle))
        # print("vel",vel)

        bullet = create_square(world, size, pygame.Vector2(player_pos), vel, color)
        world.add_component(bullet, CTagBullet())
