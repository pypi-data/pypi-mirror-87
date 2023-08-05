#  ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####

import pygame
from renderer import Mesh, CameraOrtho


def cube():
    camera = CameraOrtho((45, 45), (0, 0), 5)
    mesh = Mesh(
        ((-1, -1, -1), (-1, -1, 1), (-1, 1, -1), (-1, 1, 1), (1, -1, -1), (1, -1, 1), (1, 1, -1), (1, 1, 1)),
        ((3, 7, 5, 1), (1, 5, 4, 0), (0, 4, 6, 2), (6, 2, 3, 7), (5, 7, 6, 4), (1, 3, 2, 0)),
        ((128, 128, 128), (128, 128, 128), (128, 128, 128), (128, 128, 128), (128, 128, 128), (128, 128, 128))
    )

    pygame.init()
    pygame.display.set_caption("3D Example: Cube")
    WINDOW = pygame.display.set_mode((720, 720))

    clock = pygame.time.Clock()
    dragging = False
    drag_start_pos = (0, 0)
    view_start_pos = (0, 0)
    while True:
        clock.tick(60)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    camera.size /= 1.1
                elif event.button == 5:
                    camera.size *= 1.1

        WINDOW.fill((0, 0, 0))
        WINDOW.blit(camera.render(mesh, (720, 720)), (0, 0))

        if pygame.mouse.get_pressed()[0]:
            if dragging:
                mouse_pos = pygame.mouse.get_pos()
                new_view = (view_start_pos[0] - (mouse_pos[1]-drag_start_pos[1])/5, view_start_pos[1] + (mouse_pos[0]-drag_start_pos[0])/5)
                camera.angle = new_view
            else:
                dragging = True
                drag_start_pos = pygame.mouse.get_pos()
                view_start_pos = camera.angle[:]
        else:
            dragging = False

cube()