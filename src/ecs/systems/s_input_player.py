import esper
import pygame
from typing import Callable

from src.ecs.components.c_input_command import CInputCommand, CommandPhase

def system_input_player(ecs_world: esper.World, event: pygame.event.Event, do_action: Callable[[CInputCommand], None]):
    components = ecs_world.get_component(CInputCommand)
    for _, c_input in components:
        if event.type == pygame.KEYDOWN:
            if event.key == c_input.key:
                c_input.phase = CommandPhase.START
                do_action(c_input)
        elif event.type == pygame.KEYUP:
            if event.key == c_input.key:
                c_input.phase = CommandPhase.END
                do_action(c_input)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                c_input.phase = CommandPhase.START
                do_action(c_input)
