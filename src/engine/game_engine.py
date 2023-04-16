import json
import pygame
import esper

from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_velocity import CVelocity

from src.ecs.systems.s_enemy_spawner import system_enemy_spawner
from src.ecs.systems.s_input_player import system_input_player
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_screen_bounce import system_screen_bounce
from src.ecs.systems.s_collision_player_enemy import system_collision_player_enemy
from src.ecs.systems.s_collision_bullet_enemy import system_collision_bullet_enemy
from src.ecs.systems.s_active_bullets import system_active_bullets
from src.ecs.systems.s_player_boundary import system_player_boundary

from src.create.prefab_creator import create_enemy_spawner, create_player_square, create_input_player, create_bullet_square


class GameEngine:
    def __init__(self) -> None:
        self._load_config_files()

        pygame.init()
        pygame.display.set_caption(self.window_cfg["title"])
        self.screen = pygame.display.set_mode(
            (self.window_cfg["size"]["w"], self.window_cfg["size"]["h"]),
            pygame.SCALED)

        self.clock = pygame.time.Clock()
        self.is_running = False
        self.framerate = self.window_cfg["framerate"]
        self.delta_time = 0
        self.bg_color = pygame.Color(self.window_cfg["bg_color"]["r"],
                                     self.window_cfg["bg_color"]["g"],
                                     self.window_cfg["bg_color"]["b"])
        self.ecs_world = esper.World()

    def _load_config_files(self):
        route = "assets/cfg_01/"
        with open(route + "window.json", encoding="utf-8") as window_file:
            self.window_cfg = json.load(window_file)
        with open(route + "enemies.json") as enemies_file:
            self.enemies_cfg = json.load(enemies_file)
        with open(route + "level_01.json") as level_01_file:
            self.level_01_cfg = json.load(level_01_file)
        with open(route + "player.json") as player_file:
            self.player_cfg = json.load(player_file)
        with open(route + "bullet.json") as bullet_file:
            self.bullet_cfg = json.load(bullet_file)

    def run(self) -> None:
        self._create()
        self.is_running = True
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
        self._clean()

    def _create(self):
        self.player_entity = create_player_square(
            self.ecs_world, self.player_cfg, self.level_01_cfg["player_spawn"])
        self.player_c_vel = self.ecs_world.component_for_entity(
            self.player_entity, CVelocity)
        create_enemy_spawner(self.ecs_world, self.level_01_cfg)
        create_input_player(self.ecs_world)
        pass

    def _calculate_time(self):
        self.clock.tick(self.framerate)
        self.delta_time = self.clock.get_time() / 1000.0

    def _process_events(self):
        for event in pygame.event.get():
            system_input_player(self.ecs_world, event, self.do_action)
            if event.type == pygame.QUIT:
                self.is_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.is_running = False

    def _update(self):
        system_enemy_spawner(self.ecs_world, self.enemies_cfg, self.delta_time)
        system_movement(self.ecs_world, self.delta_time)
        system_player_boundary(self.ecs_world, self.screen, self.player_entity)
        system_screen_bounce(self.ecs_world, self.screen)
        system_collision_player_enemy(
            self.ecs_world, self.player_entity, self.level_01_cfg)
        system_collision_bullet_enemy(self.ecs_world)
        system_active_bullets(self.ecs_world, self.screen)
        self.ecs_world._clear_dead_entities()

    def _draw(self):
        self.screen.fill(self.bg_color)
        system_rendering(self.ecs_world, self.screen)
        pygame.display.flip()

    def _clean(self):
        self.ecs_world.clear_database()
        pygame.quit()

    def do_action(self, c_input: CInputCommand):
        if c_input.name == "PLAYER_LEFT":
            if c_input.phase == CommandPhase.START:
                self.player_c_vel.vel.x -= self.player_cfg["input_velocity"]
            elif c_input.phase == CommandPhase.END:
                self.player_c_vel.vel.x += self.player_cfg["input_velocity"]
        if c_input.name == "PLAYER_RIGHT":
            if c_input.phase == CommandPhase.START:
                self.player_c_vel.vel.x += self.player_cfg["input_velocity"]
            elif c_input.phase == CommandPhase.END:
                self.player_c_vel.vel.x -= self.player_cfg["input_velocity"]
        if c_input.name == "PLAYER_UP":
            if c_input.phase == CommandPhase.START:
                self.player_c_vel.vel.y -= self.player_cfg["input_velocity"]
            elif c_input.phase == CommandPhase.END:
                self.player_c_vel.vel.y += self.player_cfg["input_velocity"]
        if c_input.name == "PLAYER_DOWN":
            if c_input.phase == CommandPhase.START:
                self.player_c_vel.vel.y += self.player_cfg["input_velocity"]
            elif c_input.phase == CommandPhase.END:
                self.player_c_vel.vel.y -= self.player_cfg["input_velocity"]
        if c_input.name == "PLAYER_FIRE":
            if c_input.phase == CommandPhase.START:
                pos = pygame.mouse.get_pos()
                create_bullet_square(self.ecs_world, self.bullet_cfg, self.player_entity,
                                     pos, self.level_01_cfg["player_spawn"]["max_bullets"])
