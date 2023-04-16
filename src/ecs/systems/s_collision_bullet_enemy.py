import esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_bullet import CTagBullet

def system_collision_bullet_enemy(world: esper.World):
    bullets = world.get_components(CSurface, CTransform, CTagBullet)
    enemies = world.get_components(CSurface, CTransform, CTagEnemy)

    for bullet_entity, (c_bullet_s, c_bullet_t, c_bullet_tag) in bullets:
        for enemy_entity, (c_enemy_s, c_enemy_t, c_enemy_tag) in enemies:
            if bullet_entity != enemy_entity:
                bullet_rect = c_bullet_s.surf.get_rect(topleft=c_bullet_t.pos)
                enemy_rect = c_enemy_s.surf.get_rect(topleft=c_enemy_t.pos)
                if bullet_rect.colliderect(enemy_rect):
                    world.delete_entity(bullet_entity)
                    world.delete_entity(enemy_entity)


