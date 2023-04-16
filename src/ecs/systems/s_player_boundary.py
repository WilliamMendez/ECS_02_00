import esper
import pygame
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface

def system_player_boundary(world: esper.World, screen: pygame.Surface, player_entity: int):
    player_transform = world.component_for_entity(player_entity, CTransform)
    player_surface = world.component_for_entity(player_entity, CSurface)

    player_rect = player_surface.surf.get_rect(topleft=player_transform.pos)
    screen_rect = screen.get_rect()

    player_rect.clamp_ip(screen_rect)
    player_transform.pos.x = player_rect.x
    player_transform.pos.y = player_rect.y
