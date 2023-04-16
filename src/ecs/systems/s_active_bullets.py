import esper
import pygame
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity

def system_active_bullets(world: esper.World, screen: pygame.Surface):
    components = world.get_components(CTagBullet, CTransform, CVelocity)
    for entity, (c_bullet, c_transform, c_velocity) in components:
        # if bullet is out of screen, delete it
        if c_transform.pos.x < 0 or c_transform.pos.x > screen.get_width() or \
                c_transform.pos.y < 0 or c_transform.pos.y > screen.get_height():
            world.delete_entity(entity)
            

