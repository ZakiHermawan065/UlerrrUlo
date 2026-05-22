import pygame
import random
import sys
import math

# Initialize Pygame
pygame.init()

# Initialize mixer and play background music
playlist = ['BGM1.mp3', 'BGM2.mp3', 'BGM3.mp3', 'BGM4.mp3', 'BGM5.mp3']
random.shuffle(playlist)
current_song = 0
pygame.mixer.init()
pygame.mixer.music.load(playlist[current_song])
pygame.mixer.music.play()
pygame.mixer.music.set_endevent(pygame.USEREVENT)

# Game window dimensions
window_width = 1920
window_height = 1080
game_window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("ULERRR ULO")

# Colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
blue = pygame.Color(0, 0, 255)
green = pygame.Color(0, 255, 0)
red = pygame.Color(255, 0, 0)

# Enemy colors
enemy_colors = [pygame.Color(0, 200, 0), pygame.Color(255, 255, 0), pygame.Color(255, 0, 0)]  # green, yellow, dark red

# Enemy config
ENEMY_COUNT = 3
ENEMY_INIT_LENGTH = 6

# Struktur Data Enemy: list of dicts
enemies = []

def random_enemy_spawn(exclude_positions):
    # Cari posisi random yang tidak overlap dengan exclude_positions
    while True:
        min_x = 3
        max_x = (window_width // snake_block_size) - 4
        min_y = 3
        max_y = (window_height // snake_block_size) - 4
        head_x = random.randint(min_x, max_x) * snake_block_size
        head_y = random.randint(min_y, max_y) * snake_block_size
        pos = [head_x, head_y]
        if pos not in exclude_positions:
            return pos

# Snake properties
snake_speed = 12  # player speed (fps)
enemy_speed = 8   # musuh bergerak setiap x frame (semakin kecil semakin cepat)
snake_block_size = 20
snake_position = [100, 60]  # kelipatan 20
snake_body = [[100, 60], [80, 60], [60, 60], [40, 60], [20, 60], [0, 60]]
direction = 'RIGHT'
change_to = direction

# Food properties
food_pos = [random.randrange(0, window_width // snake_block_size) * snake_block_size,
            random.randrange(0, window_height // snake_block_size) * snake_block_size]
growth = 0  
growth_per_food = 3
food_spawn = True

# Function to display main menu
def main_menu():
    font_title_base = pygame.font.SysFont('freesansbold', 160, bold=True)
    font_menu_base = pygame.font.SysFont('Times New Roman', 80)
    font_tutorial = pygame.font.SysFont('Calibri', 40)

    # Animasi detak untuk 'Press Enter'
    detak_time = 0
    detak_speed = 3
    detak_min = 1.4
    detak_max = 1.6

    # Animasi glow judul
    glow_time = 0
    glow_speed = 5
    glow_min = 80
    glow_max = 100

    clock = pygame.time.Clock()
    while True:
        # Animasi detak
        detak_time += clock.get_time() / 1000.0 * detak_speed
        detak_scale = detak_min + (detak_max - detak_min) * (0.5 + 0.5 * math.sin(detak_time))

        # Animasi glow
        glow_time += clock.get_time() / 1000.0 * glow_speed
        glow_radius = int(glow_min + (glow_max - glow_min) * (0.5 + 0.5 * math.sin(glow_time)))
        glow_alpha = int(128 + 127 * (0.5 + 0.5 * math.sin(glow_time)))

        # Draw background
        game_window.fill(black)

        # Draw glowing title
        title_text = 'ULERRR ULO'
        title_surface = font_title_base.render(title_text, True, blue)
        # Outer glow effect
        for r in range(glow_radius, 0, -8):
            glow_surf = pygame.Surface((title_surface.get_width()+r*2, title_surface.get_height()+r*2), pygame.SRCALPHA)
            alpha = max(0, min(255, int(glow_alpha/r*2)))
            color = (0, 200, 255, alpha)
            try:
                pygame.draw.ellipse(glow_surf, color, (0,0,glow_surf.get_width(),glow_surf.get_height()))
            except TypeError:
                # Fallback ke RGB jika alpha tidak diterima
                pygame.draw.ellipse(glow_surf, (0, 200, 255), (0,0,glow_surf.get_width(),glow_surf.get_height()))
            game_window.blit(glow_surf, (window_width//2 - title_surface.get_width()//2 - r, 80 - r))
        game_window.blit(title_surface, (window_width//2 - title_surface.get_width()//2, 80))

        # Draw detak 'Press Enter'
        opsi_text = 'Press Enter to Start'
        opsi_font = pygame.font.SysFont('Times New Roman', int(40*detak_scale))
        opsi = opsi_font.render(opsi_text, True, white)
        game_window.blit(opsi, (window_width//2 - opsi.get_width()//2, window_height//2))

        # Draw tutorial
        tutorial = font_tutorial.render('Use WASD or Arrow Keys to move', True, white)
        game_window.blit(tutorial, (window_width//2 - tutorial.get_width()//2, window_height*3//4))

        pygame.display.update()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

# Pause menu function
def pause_menu():
    font = pygame.font.SysFont('Times New Roman', 80)
    paused = True
    while paused:
        game_window.fill((120, 120, 120))
        pause_text = font.render('PAUSED', True, (255, 255, 255))
        instr = pygame.font.SysFont('Times New Roman', 40).render('Press ESC or R to resume, M for Menu, Q to quit', True, (200, 200, 200))
        game_window.blit(pause_text, (window_width//2 - pause_text.get_width()//2, window_height//2 - 60))
        game_window.blit(instr, (window_width//2 - instr.get_width()//2, window_height//2 + 20))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False
                elif event.key == pygame.K_r:
                    paused = False
                elif event.key == pygame.K_m:
                    return 'main_menu'
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
            # Handle music end event
            if event.type == pygame.USEREVENT:
                global current_song
                current_song = (current_song + 1) % len(playlist)
                pygame.mixer.music.load(playlist[current_song])
                pygame.mixer.music.play()
    return 'resume'

# Function to display the restart menu
def restart_menu(message='[R] Restart   [M] Main Menu   [Q] Quit'):
    font = pygame.font.SysFont('Times New Roman', 80)
    while True:
        game_window.fill((125, 125, 125))
        lines = message.split('\n')
        for i, line in enumerate(lines):
            rendered_line = font.render(line, True, white)
            game_window.blit(rendered_line, (window_width//2 - rendered_line.get_width()//2, window_height//2 - 80 + i * 90))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return 'restart'
                elif event.key == pygame.K_m:
                    return 'main_menu'
                elif event.key == pygame.K_q:
                    return 'quit'

# Function to reset the game state
def reset_game():
    global snake_position, snake_body, direction, change_to, food_pos, food_spawn, growth
    global player_boost_charge, player_is_boosting, player_boost_duration, player_move_timer
    player_boost_charge = 0.0
    player_is_boosting = False
    player_boost_duration = 0.0
    player_move_timer = 0.0
    # Player spawn
    exclude = []
    head = random_enemy_spawn(exclude)
    snake_position[:] = head
    direction = random.choice(['RIGHT', 'LEFT', 'UP', 'DOWN'])
    change_to = direction
    snake_body.clear()
    snake_body.append(list(snake_position))
    for i in range(1, 6):
        if direction == 'RIGHT':
            snake_body.append([head[0] - i*snake_block_size, head[1]])
        elif direction == 'LEFT':
            snake_body.append([head[0] + i*snake_block_size, head[1]])
        elif direction == 'UP':
            snake_body.append([head[0], head[1] + i*snake_block_size])
        elif direction == 'DOWN':
            snake_body.append([head[0], head[1] - i*snake_block_size])
    # Enemy spawn
    global enemies
    enemies = []
    exclude = [tuple(b) for b in snake_body]
    for idx in range(ENEMY_COUNT):
        e_head = random_enemy_spawn(exclude)
        e_dir = random.choice(['RIGHT', 'LEFT', 'UP', 'DOWN'])
        e_body = [list(e_head)]
        for i in range(1, ENEMY_INIT_LENGTH):
            if e_dir == 'RIGHT':
                e_body.append([e_head[0] - i*snake_block_size, e_head[1]])
            elif e_dir == 'LEFT':
                e_body.append([e_head[0] + i*snake_block_size, e_head[1]])
            elif e_dir == 'UP':
                e_body.append([e_head[0], e_head[1] + i*snake_block_size])
            elif e_dir == 'DOWN':
                e_body.append([e_head[0], e_head[1] - i*snake_block_size])
        enemies.append({
            'body': e_body,
            'dir': e_dir,
            'color': enemy_colors[idx % len(enemy_colors)],
            'init_body': [list(b) for b in e_body],
            'init_dir': e_dir,
            'boost_charge': 0.0,
            'is_boosting': False,
            'boost_duration': 0.0,
            'move_timer': 0.0
        })
# AI sederhana musuh: bergerak ke arah makanan, prioritas x/y random
def move_enemy(enemy, food_pos, player_body, all_enemies):
    head = enemy['body'][0][:]
    current_dir = enemy['dir']
    dirs = ['UP', 'DOWN', 'LEFT', 'RIGHT']
    
    def is_opposite(d1, d2):
        return (d1 == 'UP' and d2 == 'DOWN') or (d1 == 'DOWN' and d2 == 'UP') or \
               (d1 == 'LEFT' and d2 == 'RIGHT') or (d1 == 'RIGHT' and d2 == 'LEFT')

    # Prioritas acak antara x/y
    if random.random() < 0.5:
        axis = ['x', 'y']
    else:
        axis = ['y', 'x']
        
    moved = False
    possible_moves = []
    
    for ax in axis:
        new_dir = None
        if ax == 'x' and head[0] < food_pos[0]:
            new_dir = 'RIGHT'
        elif ax == 'x' and head[0] > food_pos[0]:
            new_dir = 'LEFT'
        elif ax == 'y' and head[1] < food_pos[1]:
            new_dir = 'DOWN'
        elif ax == 'y' and head[1] > food_pos[1]:
            new_dir = 'UP'
            
        if new_dir and not is_opposite(current_dir, new_dir):
            nh = head[:]
            if new_dir == 'RIGHT': nh[0] += snake_block_size
            elif new_dir == 'LEFT': nh[0] -= snake_block_size
            elif new_dir == 'DOWN': nh[1] += snake_block_size
            elif new_dir == 'UP': nh[1] -= snake_block_size
            possible_moves.append((nh, new_dir))
            
    for nh, new_dir in possible_moves:
        if nh in player_body:
            continue
            
        collision = False
        for e in all_enemies:
            # Hindari badan semua ular, termasuk badannya sendiri
            if nh in e['body'][:-1]: # [:-1] agar mengabaikan ujung ekor yang akan berpindah maju
                collision = True
                break
                
        if not collision:
            enemy['body'].insert(0, nh)
            enemy['body'].pop()
            enemy['dir'] = new_dir
            moved = True
            break
            
    if not moved:
        random.shuffle(dirs)
        for d in dirs:
            if is_opposite(current_dir, d):
                continue
                
            nh = head[:]
            if d == 'UP': nh[1] -= snake_block_size
            elif d == 'DOWN': nh[1] += snake_block_size
            elif d == 'LEFT': nh[0] -= snake_block_size
            elif d == 'RIGHT': nh[0] += snake_block_size
            
            if nh in player_body:
                continue
                
            collision = False
            for e in all_enemies:
                if nh in e['body'][:-1]:
                    collision = True
                    break
                    
            if not collision:
                enemy['body'].insert(0, nh)
                enemy['body'].pop()
                enemy['dir'] = d
                moved = True
                break
                
    if not moved:
        # Jika terjebak 100%, paksakan musuh maju searah agar ia menabrak tembok/badan dan memicu kondisi eliminasi
        nh = head[:]
        if current_dir == 'UP': nh[1] -= snake_block_size
        elif current_dir == 'DOWN': nh[1] += snake_block_size
        elif current_dir == 'LEFT': nh[0] -= snake_block_size
        elif current_dir == 'RIGHT': nh[0] += snake_block_size
        enemy['body'].insert(0, nh)
        enemy['body'].pop()
    food_pos = [random.randrange(0, window_width // snake_block_size) * snake_block_size,
                random.randrange(0, window_height // snake_block_size) * snake_block_size]
    food_spawn = True
    growth = 0

main_menu()
# Main game loop with restart feature
while True:
    # Game loop
    game_over = False
    player_won = False
    force_main_menu = False
    reset_game()
    # Daylight cycle variables
    daylight_timer = 0.0
    daylight_cycle_duration = 60.0  # detik
    clock = pygame.time.Clock()
    while not game_over:

        # Tick & daylight cycle update
        dt = clock.tick(60) / 1000.0
        daylight_timer += dt
        t = (daylight_timer % daylight_cycle_duration) / daylight_cycle_duration
        # Bolak-balik: 0->1->0
        if t > 0.5:
            t = 1 - t
        t = t * 2
        bg_val = int(255 * (1 - t))
        bg_color = (bg_val, bg_val, bg_val)

        # --- PLAYER BOOST LOGIC ---
        if player_is_boosting:
            player_boost_duration -= dt
            if player_boost_duration <= 0:
                player_is_boosting = False
                player_boost_charge = 0.0
        else:
            if player_boost_charge < 5.0:
                player_boost_charge = min(5.0, player_boost_charge + dt)

        # --- ENEMY BOOST LOGIC & MOVEMENT ---
        for enemy in enemies:
            if enemy['is_boosting']:
                enemy['boost_duration'] -= dt
                if enemy['boost_duration'] <= 0:
                    enemy['is_boosting'] = False
                    enemy['boost_charge'] = 0.0
            else:
                if enemy['boost_charge'] < 5.0:
                    enemy['boost_charge'] = min(5.0, enemy['boost_charge'] + dt)
                
                if enemy['boost_charge'] >= 5.0 and random.random() < 0.01:
                    enemy['is_boosting'] = True
                    enemy['boost_duration'] = 1.5

            current_enemy_speed = 16 if enemy['is_boosting'] else 8
            enemy['move_timer'] += dt
            if enemy['move_timer'] >= 1.0 / current_enemy_speed:
                enemy['move_timer'] -= 1.0 / current_enemy_speed
                move_enemy(enemy, food_pos, snake_body, enemies)
            
        # Cek tabrakan musuh dengan pembatas, badan player, atau npc lain
        enemies_to_remove = []
        for enemy in enemies:
            head = enemy['body'][0]
            # Tabrak pembatas
            if head[0] < 0 or head[0] > window_width - snake_block_size or head[1] < 0 or head[1] > window_height - snake_block_size:
                enemies_to_remove.append(enemy)
                continue
            # Tabrak badan player
            if head in snake_body:
                enemies_to_remove.append(enemy)
                continue
            # Tabrak npc lain
            for other_enemy in enemies:
                if enemy is other_enemy:
                    continue
                if head in other_enemy['body']:
                    enemies_to_remove.append(enemy)
                    break
                    
        for enemy in enemies_to_remove:
            if enemy in enemies:
                enemies.remove(enemy)
                
        # Cek tabrakan player dengan musuh
        for enemy in enemies:
            if snake_position in enemy['body']:
                game_over = True
                break
                
        # Cek kondisi menang jika semua musuh tereliminasi
        if len(enemies) == 0:
            player_won = True
            game_over = True
            
        # Cek musuh makan makanan
        for enemy in enemies:
            if enemy['body'][0] == food_pos:
                food_spawn = False
                # Panjangkan musuh
                for _ in range(growth_per_food):
                    enemy['body'].append(enemy['body'][-1][:])
        # Fungsi Game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Handle player input
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_UP and direction != 'DOWN':
                    change_to = 'UP'
                if event.key == pygame.K_s or event.key == pygame.K_DOWN and direction != 'UP':
                    change_to = 'DOWN'
                if event.key == pygame.K_a or event.key == pygame.K_LEFT and direction != 'RIGHT':
                    change_to = 'LEFT'
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT and direction != 'LEFT':
                    change_to = 'RIGHT'
                if event.key == pygame.K_SPACE:
                    if player_boost_charge >= 5.0 and not player_is_boosting:
                        player_is_boosting = True
                        player_boost_duration = 1.5
                if event.key == pygame.K_ESCAPE:
                    if pause_menu() == 'main_menu':
                        force_main_menu = True
                        game_over = True
            # Handle music end event
            if event.type == pygame.USEREVENT:
                current_song = (current_song + 1) % len(playlist)
                pygame.mixer.music.load(playlist[current_song])
                pygame.mixer.music.play()

        # --- PLAYER MOVEMENT ---
        current_player_speed = 24 if player_is_boosting else 12
        player_move_timer += dt
        if player_move_timer >= 1.0 / current_player_speed:
            player_move_timer -= 1.0 / current_player_speed
            
            # Validate direction change
            direction = change_to
    
            # Move the snake
            if direction == 'UP':
                snake_position[1] -= snake_block_size
            if direction == 'DOWN':
                snake_position[1] += snake_block_size
            if direction == 'LEFT':
                snake_position[0] -= snake_block_size
            if direction == 'RIGHT':
                snake_position[0] += snake_block_size
    
            # Snake body growing mechanism
            snake_body.insert(0, list(snake_position))
            if snake_position[0] == food_pos[0] and snake_position[1] == food_pos[1]:
                food_spawn = False
                growth += growth_per_food
            else:
                if growth > 0:
                    growth -= 1
                else:
                    snake_body.pop()
    
            # Game Over conditions
            if snake_position[0] < 0 or snake_position[0] > window_width - snake_block_size or \
               snake_position[1] < 0 or snake_position[1] > window_height - snake_block_size:
                game_over = True

        # --- FOOD RESPAWN LOGIC ---
        if not food_spawn:
            food_pos = [random.randrange(0, window_width // snake_block_size) * snake_block_size,
                        random.randrange(0, window_height // snake_block_size) * snake_block_size]
        food_spawn = True

        # Drawing
        game_window.fill(bg_color)
        # Gambar musuh
        for enemy in enemies:
            for block in enemy['body']:
                pygame.draw.rect(game_window, enemy['color'], pygame.Rect(block[0], block[1], snake_block_size, snake_block_size))
        # Gambar player
        for block in snake_body:
            pygame.draw.rect(game_window, blue, pygame.Rect(block[0], block[1], snake_block_size, snake_block_size))
        # Gambar makanan
        pygame.draw.rect(game_window, red, pygame.Rect(food_pos[0], food_pos[1], snake_block_size, snake_block_size))

        # Draw Booster UI (Bottom Right)
        bottle_width = 40
        bottle_height = 100
        bottle_x = window_width - 80
        bottle_y = window_height - 140
        cap_width = 20
        cap_height = 10
        cap_x = bottle_x + (bottle_width // 2) - (cap_width // 2)
        cap_y = bottle_y - cap_height
        
        # Draw bottle cap
        pygame.draw.rect(game_window, white, (cap_x, cap_y, cap_width, cap_height))
        # Draw bottle outline
        pygame.draw.rect(game_window, white, (bottle_x, bottle_y, bottle_width, bottle_height), 2)
        
        # Draw liquid (charge)
        if player_is_boosting:
            fill_ratio = player_boost_duration / 1.5
            fill_color = pygame.Color(255, 100, 0)
        else:
            fill_ratio = player_boost_charge / 5.0
            fill_color = pygame.Color(0, 255, 255) if fill_ratio >= 1.0 else pygame.Color(100, 100, 100)
            
        fill_h = int(bottle_height * fill_ratio)
        if fill_h > 0:
            pygame.draw.rect(game_window, fill_color, (bottle_x, bottle_y + bottle_height - fill_h, bottle_width, fill_h))

        # Update the screen
        pygame.display.update()

    if force_main_menu:
        main_menu()
        continue

    # Show restart menu
    if player_won:
        message = 'You Win\n[R] Restart   [M] Main Menu   [Q] Quit'
    elif game_over:
        message = 'Game Over\n[R] Restart   [M] Main Menu   [Q] Quit'

    action = restart_menu(message)
    if action == 'quit':
        break
    elif action == 'main_menu':
        main_menu()
        continue

pygame.quit()