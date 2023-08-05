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
from math import radians, sin, cos
from . import examples


class CameraOrtho:
    def __init__(self, angle=(0, 0), shift=(0, 0), size=5):
        """
        Initializes camera.
        :param angle: Angle of the camera in (latitude, longitude)
        :type angle: Tuple[float, float]
        :param shift: Shift of camera in (x, y)
        :type shift: Tuple[float, float]
        :param size: Orthographic size of camera.
        :type size: float
        """
        self.angle = angle
        self.shift = shift
        self.size = size

    def render(self, mesh, resolution, bg_col=(0, 0, 0, 0)):
        """
        Renders mesh as a pygame surface.
        :param mesh: Mesh to render.
        :type mesh: renderer.Mesh
        :param resolution: Resolution to render in (x, y). The Y size will be adjusted, and the X size will be the ortho size.
        :type resolution: Tuple[int, int]
        :param bg_col: Background color of render in (R, G, B, [A])
        :type bg_col: Tuple[int]
        """
        surface = pygame.Surface(resolution, pygame.SRCALPHA)
        surface.fill(bg_col)

        data = mesh.setup_render()
        for face in data:
            color = face[0]
            locs = []
            for vert in face[1]:
                locs.append(self.project(vert, resolution))
            pygame.draw.polygon(surface, color, locs)

        return surface

    def project(self, vert, res):
        size_hor = self.size
        size_ver = self.size / res[0] * res[1]
        loc_x, loc_y, loc_z = vert
        view_ver = radians(self.angle[0])
        view_hor = radians(self.angle[1])

        px_hor = loc_x*cos(view_hor) + loc_y*sin(view_hor)
        px_hor *= res[0] / size_hor
        px_hor += res[0] / 2

        px_ver = loc_z*sin(view_ver) - loc_x*sin(view_hor)*cos(view_ver) + loc_y*cos(view_hor)*cos(view_ver)
        px_ver *= res[1] / size_ver
        px_ver += res[1] / 2

        return (px_hor, px_ver)


class Mesh:
    def __init__(self, verts, faces, colors):
        """
        Initializes mesh.
        :param verts: Tuple of (x, y, z) locations.
        :type verts: Tuple[Tuple[float, float, float]]
        :param faces: Tuple of vertex indexes.
        :type faces: Tuple[Tuple[int]]
        :param colors: Colors (r, g, b) corresponding to each face.
        :type colors: Tuple[Tuple[int, int, int]]
        """
        self.set_mesh(verts, faces, colors)

    def set_mesh(self, verts, faces, colors):
        """
        Initializes mesh.
        :param verts: Tuple of (x, y, z) locations.
        :type verts: Tuple[Tuple[float, float, float]]
        :param faces: Tuple of vertex indexes.
        :type faces: Tuple[Tuple[int]]
        :param colors: Colors (r, g, b) corresponding to each face.
        :type colors: Tuple[Tuple[int, int, int]]
        """
        self.verts = verts
        self.colors = colors
        self.faces = []
        for face in faces:
            self.faces.append([verts[i] for i in face])

    def setup_render(self):
        """
        Returns a list that the renderer can understand. This should only be called by the renderer.
        """
        faces = []
        for i, face in enumerate(self.faces):
            if len(face) == 3:
                faces.append((self.colors[i], face))
            else:
                curr_color = self.colors[i]
                for vert in range(1, len(face)-1):
                    faces.append((curr_color, (face[0], face[vert], face[vert+1])))

        return faces