from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
from math import sin, cos, radians, sqrt
import random


# Game constants and state variables
GRID_N = 20
CELL_DIM = 60


avatar_pos = [0.0, 0.0, 0.0]
avatar_heading = 0.0  # degrees
avatar_hp = 5
player_score = 0
is_dead = False
has_won = False


ammo = 15
cam_elevation = 400
cam_spin = 0
third_person_view = False


ENEMY_TARGET_COUNT = 3
enemy_list = []
ENEMY_BASE_DELAY = 100
enemy_timer = 0
enemy_respawn_counter = ENEMY_BASE_DELAY


shots = []
SHOT_SPEED = 10


treasure_list = []
TREASURE_SLOTS = 5
TREASURE_KINDS = ['orb', 'crate', 'barrel']


maps_collection = []
active_map_index = 0
show_map_menu = True


AVATAR_RAD = 20


# Maze maps
_map1 = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0]
]


_map2 = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0]
]


_map3 = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0]
]


maps_collection = [_map1, _map2, _map3]


# Utility functions
def grid_to_world(cx, cy):
    half = (GRID_N * CELL_DIM) / 2
    wx = (cx * CELL_DIM) - half + CELL_DIM / 2
    wy = (cy * CELL_DIM) - half + CELL_DIM / 2
    return wx, wy


def world_to_grid(wx, wy):
    half = (GRID_N * CELL_DIM) / 2
    gx = int((wx + half) / CELL_DIM)
    gy = int((wy + half) / CELL_DIM)
    return gx, gy


def map_valid_position(wx, wy):
    if show_map_menu:
        return False
    half = (GRID_N * CELL_DIM) / 2
    if abs(wx) > half - AVATAR_RAD or abs(wy) > half - AVATAR_RAD:
        return False
    gx, gy = world_to_grid(wx, wy)
    if not (0 <= gx < GRID_N and 0 <= gy < GRID_N):
        return False
    current_map = maps_collection[active_map_index]
    if current_map[gx][gy] == 1:
        return False
    # Check nearby walls to avoid clipping
    for dx, dy in [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]:
        nx, ny = gx + dx, gy + dy
        if 0 <= nx < GRID_N and 0 <= ny < GRID_N:
            if current_map[nx][ny] == 1:
                wall_x = (nx * CELL_DIM) - half
                wall_y = (ny * CELL_DIM) - half
                # Cell center coordinates
                if abs(wx - (wall_x + CELL_DIM / 2)) < CELL_DIM / 2 + AVATAR_RAD and \
                   abs(wy - (wall_y + CELL_DIM / 2)) < CELL_DIM / 2 + AVATAR_RAD:
                    return False
    return True


# Treasure spawn
def spawn_single_treasure():
    current_map = maps_collection[active_map_index]
    while True:
        gx = random.randint(1, GRID_N - 2)
        gy = random.randint(1, GRID_N - 2)
        if current_map[gx][gy] == 0:
            kind = random.choice(TREASURE_KINDS)
            current_map[gx][gy] = 2
            treasure_list.append({
                'pos': (gx, gy),
                'kind': kind,
                'scale': random.uniform(0.8, 1.2),
                't': random.uniform(0, 2 * math.pi)
            })
            break


def build_map():
    global treasure_list
    base = maps_collection[active_map_index]
    maps_collection[active_map_index] = [row[:] for row in base]
    treasure_list = []
    for _ in range(TREASURE_SLOTS):
        spawn_single_treasure()


# Enemy pathfinding
def neighbors(cx, cy):
    n = []
    current_map = maps_collection[active_map_index]
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        nx, ny = cx + dx, cy + dy
        if 0 <= nx < GRID_N and 0 <= ny < GRID_N and current_map[nx][ny] != 1:
            n.append((nx, ny))
    return n


def find_route(sx, sy, tx, ty):
    queue = [(sx, sy, [])]
    seen = set()
    while queue:
        x, y, path = queue.pop(0)
        if (x, y) == (tx, ty):
            return path
        if (x, y) in seen:
            continue
        seen.add((x, y))
        for nx, ny in neighbors(x, y):
            queue.append((nx, ny, path + [(nx, ny)]))
    return []


def create_enemy_instance():
    half = (GRID_N * CELL_DIM) / 2
    current_map = maps_collection[active_map_index]
    while True:
        gx = random.randint(1, GRID_N - 2)
        gy = random.randint(1, GRID_N - 2)
        if current_map[gx][gy] == 0:
            wx, wy = grid_to_world(gx, gy)
            px, py, _ = avatar_pos
            if sqrt((wx - px) ** 2 + (wy - py) ** 2) > 180:
                return {
                    'pos': [wx, wy, 30.0],
                    'size': 30.0,
                    'phase': random.random() * 2 * math.pi,
                    'route': [],
                    'target_grid': None
                }


def initial_enemies():
    global enemy_list
    enemy_list = [create_enemy_instance() for _ in range(ENEMY_TARGET_COUNT)]


# Enemy updates
def refresh_enemies():
    global enemy_list, avatar_hp, is_dead, player_score, enemy_timer, enemy_respawn_counter
    for e in enemy_list[:]:
        e['phase'] += 0.05
        e['size'] = 25 + 5 * sin(e['phase'])
        ex, ey, ez = e['pos']
        px, py, pz = avatar_pos
        gx, gy = world_to_grid(ex, ey)
        pgx, pgy = world_to_grid(px, py)
        if not e['route'] or e['target_grid'] != (pgx, pgy):
            e['route'] = find_route(gx, gy, pgx, pgy)
            e['target_grid'] = (pgx, pgy)
        if e['route']:
            nx, ny = e['route'][0]
            tx, ty = grid_to_world(nx, ny)
            dx = tx - ex
            dy = ty - ey
            dist = sqrt(dx * dx + dy * dy) if (dx != 0 or dy != 0) else 0
            if dist > 0:
                spd = 0.2 if not is_dead else 0.0
                e['pos'][0] += (dx / dist) * spd
                e['pos'][1] += (dy / dist) * spd
            if dist < 5:
                e['route'].pop(0)


        # Collision with player
        px, py, _ = avatar_pos
        ex, ey, _ = e['pos']
        d = sqrt((px - ex) ** 2 + (py - ey) ** 2) if (px != ex or py != ey) else 0
        if d < 40 and not is_dead:
            avatar_hp -= 1
            try:
                enemy_list.remove(e)
            except ValueError:
                pass
            enemy_timer = 0
            if avatar_hp <= 0:
                is_dead = True


    # Spawn logic
    if len(enemy_list) < ENEMY_TARGET_COUNT:
        enemy_timer += 1
        if enemy_timer >= enemy_respawn_counter:
            enemy_list.append(create_enemy_instance())
            enemy_timer = 0


# Shots handling
def shoot():
    global shots, ammo
    if ammo <= 0:
        return
    x, y, z = avatar_pos
    ang = avatar_heading
    if third_person_view:
        bx = x + 5 * sin(radians(ang))
        by = y + 5 * cos(radians(ang))
        bz = z + 30
    else:
        bx = x
        by = y
        bz = z + 30
    shots.append({
        'pos': [bx, by, bz],
        'ang': ang,
        'dist': 0
    })
    ammo -= 1


def update_shots():
    global shots, player_score, enemy_list
    updated = []
    for s in shots:
        ar = radians(s['ang'])
        s['pos'][0] += SHOT_SPEED * sin(ar)
        s['pos'][1] += SHOT_SPEED * cos(ar)
        s['dist'] += SHOT_SPEED
        if not map_valid_position(s['pos'][0], s['pos'][1]):
            continue
        hit = False
        for e in enemy_list[:]:
            if 'pos' not in e:
                continue
            ex, ey, ez = e['pos']
            bx, by, bz = s['pos']
            dx = ex - bx
            dy = ey - by
            dz = ez - bz
            dsq = dx * dx + dy * dy + dz * dz
            if dsq < (e['size'] + 10) ** 2:
                try:
                    enemy_list.remove(e)
                except ValueError:
                    pass
                player_score += 10
                hit = True
                break
        if not hit:
            updated.append(s)
    shots[:] = updated


# Drawing treasures
def render_treasure(t):
    gx, gy = t['pos']
    wx, wy = grid_to_world(gx, gy)
    glPushMatrix()
    glTranslatef(wx, wy, 25)
    t['t'] += 0.05
    scale = 1 + 0.1 * math.sin(t['t'])
    if t['kind'] == 'orb':
        glColor3f(0.1, 0.6, 0.9)
        gluSphere(gluNewQuadric(), 15 * t['scale'] * scale, 20, 20)
    elif t['kind'] == 'crate':
        glColor3f(0.6, 0.3, 0.2)
        glutSolidCube(25 * t['scale'] * scale)
    else:  # barrel
        glColor3f(0.9, 0.4, 0.2)
        glRotatef(90, 1, 0, 0)
        gluCylinder(gluNewQuadric(), 12 * t['scale'] * scale, 12 * t['scale'] * scale, 30 * t['scale'] * scale, 32, 4)
    glPopMatrix()


def render_map():
    if show_map_menu:
        return
    half = (GRID_N * CELL_DIM) / 2
    # Floor
    glColor3f(0.95, 0.95, 0.85)
    glBegin(GL_QUADS)
    glVertex3f(-half, -half, 0)
    glVertex3f(half, -half, 0)
    glVertex3f(half, half, 0)
    glVertex3f(-half, half, 0)
    glEnd()


    current_map = maps_collection[active_map_index]
    # Walls
    glColor3f(0.15, 0.45, 0.15)
    for i in range(GRID_N):
        for j in range(GRID_N):
            if current_map[i][j] == 1:
                wx = (i * CELL_DIM) - half
                wy = (j * CELL_DIM) - half
                glPushMatrix()
                glTranslatef(wx + CELL_DIM / 2, wy + CELL_DIM / 2, CELL_DIM / 2)
                glutSolidCube(CELL_DIM)
                glPopMatrix()


    for t in treasure_list:
        render_treasure(t)


def render_avatar():
    if show_map_menu:
        return
    x, y, z = avatar_pos
    glPushMatrix()
    glTranslatef(x, y, z)
    if is_dead:
        glRotatef(90, 1, 0, 0)
        glTranslatef(0, 30, 0)
    else:
        glRotatef(-avatar_heading, 0, 0, 1)


    # Body
    glColor3f(0.2, 0.3, 0.7)
    glPushMatrix()
    glTranslatef(0, 0, 30)
    glBegin(GL_QUADS)
    glVertex3f(-12, -6, 20)
    glVertex3f(12, -6, 20)
    glVertex3f(12, 6, 20)
    glVertex3f(-12, 6, 20)
    glVertex3f(-12, -6, -20)
    glVertex3f(12, -6, -20)
    glVertex3f(12, 6, -20)
    glVertex3f(-12, 6, -20)
    glVertex3f(-12, -6, -20)
    glVertex3f(-12, 6, -20)
    glVertex3f(-12, 6, 20)
    glVertex3f(-12, -6, 20)
    glVertex3f(12, -6, -20)
    glVertex3f(12, 6, -20)
    glVertex3f(12, 6, 20)
    glVertex3f(12, -6, 20)
    glVertex3f(-12, -6, 20)
    glVertex3f(12, -6, 20)
    glVertex3f(12, -6, -20)
    glVertex3f(-12, -6, -20)
    glVertex3f(-12, 6, 20)
    glVertex3f(12, 6, 20)
    glVertex3f(12, 6, -20)
    glVertex3f(-12, 6, -20)
    glEnd()
    glPopMatrix()


    # Head
    glColor3f(0.95, 0.8, 0.6)
    glPushMatrix()
    glTranslatef(0, 0, 55)
    gluSphere(gluNewQuadric(), 10, 20, 20)
    glPopMatrix()


    # Weapon or barrel
    glPushMatrix()
    if third_person_view:
        glTranslatef(0, 5, 30)
        glRotatef(-90, 1, 0, 0)
    else:
        glTranslatef(0, 0, 40)
        glRotatef(-90, 1, 0, 0)
    glColor3f(0.25, 0.25, 0.25)
    gluCylinder(gluNewQuadric(), 3, 2, 30, 20, 20)
    glPopMatrix()


    glPopMatrix()


def render_enemies():
    if show_map_menu:
        return
    for e in enemy_list:
        x, y, z = e['pos']
        s = e['size']
        glPushMatrix()
        glTranslatef(x, y, z)
        glColor3f(0.8, 0.1, 0.1)
        gluSphere(gluNewQuadric(), s, 20, 20)
        glPushMatrix()
        glTranslatef(s / 2, s / 2, s / 2)
        glColor3f(1, 1, 1)
        gluSphere(gluNewQuadric(), s / 4, 10, 10)
        glPopMatrix()
        glPopMatrix()


def render_shots():
    if show_map_menu:
        return
    glColor3f(0.05, 0.05, 0.05)
    for s in shots:
        bx, by, bz = s['pos']
        glPushMatrix()
        glTranslatef(bx, by, bz)
        gluSphere(gluNewQuadric(), 5, 10, 10)
        glPopMatrix()


# HUD and text
def draw_text_screen(x, y, txt):
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glColor3f(1, 1, 1)
    glRasterPos2f(x, y)
    for ch in txt:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def render_hud():
    draw_text_screen(10, 780, f"Score: {player_score}  HP: {avatar_hp}  Ammo: {ammo}")
    if is_dead:
        draw_text_screen(300, 700, "YOU DIED. Press R to restart")
    elif has_won:
        draw_text_screen(300, 700, "CONGRATS! YOU ESCAPED. Press R to restart")
    view_txt = "First-Person" if third_person_view else "Third-Person"
    draw_text_screen(10, 740, f"View: {view_txt} (Right-click to toggle)")


def render_map_menu():
    draw_text_screen(400, 500, "Choose a Map:")
    draw_text_screen(400, 450, "Press 1 to Choose Map A")
    draw_text_screen(400, 400, "Press 2 to Choose Map B")
    draw_text_screen(400, 350, "Press 3 to Choose Map C")


# Input handlers
def key_handler(key, x, y):
    global avatar_heading, avatar_pos, is_dead, avatar_hp, player_score, has_won
    global show_map_menu, active_map_index
    keyb = key
    if keyb == b'r':
        restart_game()
        return


    if show_map_menu:
        if keyb == b'1':
            active_map_index = 0
            show_map_menu = False
            restart_game()
        elif keyb == b'2':
            active_map_index = 1
            show_map_menu = False
            restart_game()
        elif keyb == b'3':
            active_map_index = 2
            show_map_menu = False
            restart_game()
        return


    if is_dead or has_won:
        return


    mv = 5
    rot = 12
    if keyb == b'w':
        nx = avatar_pos[0] + mv * sin(radians(avatar_heading))
        ny = avatar_pos[1] + mv * cos(radians(avatar_heading))
        if map_valid_position(nx, ny):
            avatar_pos[0] = nx
            avatar_pos[1] = ny
    elif keyb == b's':
        nx = avatar_pos[0] - mv * sin(radians(avatar_heading))
        ny = avatar_pos[1] - mv * cos(radians(avatar_heading))
        if map_valid_position(nx, ny):
            avatar_pos[0] = nx
            avatar_pos[1] = ny
    elif keyb == b'a':
        avatar_heading -= rot
    elif keyb == b'd':
        avatar_heading += rot
    glutPostRedisplay()


def special_handler(key, x, y):
    global cam_elevation, cam_spin, third_person_view
    if key == GLUT_KEY_UP:
        cam_elevation = min(cam_elevation + 10, 1500)
    elif key == GLUT_KEY_DOWN:
        cam_elevation = max(cam_elevation - 10, 150)
    elif key == GLUT_KEY_LEFT:
        cam_spin -= 5
    elif key == GLUT_KEY_RIGHT:
        cam_spin += 5
    glutPostRedisplay()




def mouse_handler(button, state, x, y):
    global third_person_view
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and not is_dead and not has_won and not show_map_menu:
        shoot()
    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN and not show_map_menu:
        third_person_view = not third_person_view
    glutPostRedisplay()




# Camera, reset, game loop
def configure_camera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, 1.25, 1, 2000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    if show_map_menu:
        return
    px, py, pz = avatar_pos
    if third_person_view:
        look_x = px + 100 * sin(radians(avatar_heading))
        look_y = py + 100 * cos(radians(avatar_heading))
        cam_x = px + 5 * sin(radians(avatar_heading))
        cam_y = py + 5 * cos(radians(avatar_heading))
        cam_z = pz + 40
        gluLookAt(cam_x, cam_y, cam_z, look_x, look_y, cam_z - 10, 0, 0, 1)
    else:
        radius = 500
        eye_x = radius * sin(radians(cam_spin))
        eye_y = radius * cos(radians(cam_spin))
        gluLookAt(eye_x, eye_y, cam_elevation, 0, 0, 0, 0, 0, 1)




def restart_game():
    global avatar_pos, avatar_heading, avatar_hp, player_score, is_dead, has_won, shots, enemy_list, enemy_timer, ammo
    half = (GRID_N * CELL_DIM) / 2
    avatar_pos = [-half + CELL_DIM + AVATAR_RAD, -half + CELL_DIM + AVATAR_RAD, 0.0]
    avatar_heading = 0.0
    avatar_hp = 5
    player_score = 0
    is_dead = False
    has_won = False
    shots = []
    ammo = 15
    enemy_list = []
    enemy_timer = ENEMY_BASE_DELAY
    build_map()
    initial_enemies()




def game_update():
    global player_score, has_won, is_dead
    if show_map_menu:
        return
    if is_dead or has_won:
        return
    # check exit (top-right corner)
    half = (GRID_N * CELL_DIM) / 2
    exit_x = half - CELL_DIM
    exit_y = half - CELL_DIM
    if avatar_pos[0] >= exit_x - AVATAR_RAD and avatar_pos[1] >= exit_y - AVATAR_RAD:
        has_won = True
        return


    refresh_enemies()
    update_shots()


    px, py, pz = avatar_pos
    gx, gy = world_to_grid(px, py)
    if 0 <= gx < GRID_N and 0 <= gy < GRID_N:
        cm = maps_collection[active_map_index]
        if cm[gx][gy] == 2:
            found = None
            for i, t in enumerate(treasure_list):
                tx, ty = t['pos']
                if tx == gx and ty == gy:
                    found = t
                    del treasure_list[i]
                    cm[gx][gy] = 0
                    break
            if found:
                player_score += 50
                if found['kind'] == 'orb':
                    global ammo
                    ammo += 5
                elif found['kind'] == 'crate':
                    ammo += 10
                else:
                    ammo += 15
                spawn_single_treasure()




# Display & idle loop
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    if show_map_menu:
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, 1000, 0, 800)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        render_map_menu()
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
    else:
        configure_camera()
        render_map()
        render_avatar()
        render_enemies()
        render_shots()


        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, 1000, 0, 800)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        render_hud()
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)


    glutSwapBuffers()




def idle():
    game_update()
    glutPostRedisplay()




def init_gl():
    glClearColor(0.05, 0.05, 0.12, 1.0)
    glEnable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)




def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutCreateWindow(b"Maze Escape")
    init_gl()
    glutDisplayFunc(display)
    glutIdleFunc(idle)
    glutKeyboardFunc(key_handler)
    glutSpecialFunc(special_handler)
    glutMouseFunc(mouse_handler)
    glutMainLoop()




if __name__ == "__main__":
    main()