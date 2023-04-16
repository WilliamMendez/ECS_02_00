import esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy


def system_collision_player_enemy(world: esper.World, player_entity: int, lvl_cfg:dict):
    components = world.get_components(CSurface, CTransform, CTagEnemy)
    pl_t = world.component_for_entity(player_entity, CTransform)
    pl_s = world.component_for_entity(player_entity, CSurface)

    pl_s.surf.get_rect(topleft=pl_t.pos)

    for enemy_entity, (c_s, c_t, c_e) in components:
        if enemy_entity != player_entity:
            enemy_rect = c_s.surf.get_rect(topleft=c_t.pos)
            if pl_s.surf.get_rect(topleft=pl_t.pos).colliderect(enemy_rect):
                world.delete_entity(enemy_entity)
                pl_t.pos.x = lvl_cfg['player_spawn']['position']['x'] - pl_s.surf.get_rect().width / 2
                pl_t.pos.y = lvl_cfg['player_spawn']['position']['y'] - pl_s.surf.get_rect().height / 2
                # print(pl_t.pos)
