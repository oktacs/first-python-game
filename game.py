# 1 - import things
# import library pygame
import pygame
# import konstanta dalam pygame
from pygame.locals import *
# import library math
import math
# import randin utk membuat bilangan acak
from random import randint

# 2 - inisialisasi game, deklarasi objek dan variable
pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
# key mapping
keys = {
	"top": False,
	"bottom": False,
	"left": False,
	"right": False
}
running = True
playerpos = [100, 100] # posisi awal player
score = 0 # menyimpan score
arrows = [] # list arrows # menyimpan titik koordinat anak panah
enemy_timer = 100 # waktu kemunculan musuh, tiap game loop nilainya akan dikurangi 1
enemies = [[width, 100]] # list utk menampung koordinat musuh
health_point = 194 # default health point for castle, gambar lebarnya 194px
countdown_timer = 90000 # 90 detik
# game over saat waktu habis dan player menang atau saat health_point adl 0
# exit code for game and win condition
exitcode = 0
EXIT_CODE_GAME_OVER = 0
EXIT_CODE_WIN = 1

# 3
# load game assets (image)
player = pygame.image.load("resources/images/dude.png")
grass = pygame.image.load("resources/images/grass.png")
castle = pygame.image.load("resources/images/castle.png")
arrow = pygame.image.load("resources/images/bullet.png")
enemy_img = pygame.image.load("resources/images/badguy.png")
healthbar = pygame.image.load("resources/images/healthbar.png")
health = pygame.image.load("resources/images/health.png")
gameover = pygame.image.load("resources/images/gameover.png")
youwin = pygame.image.load("resources/images/youwin.png")

# load audio
pygame.mixer.init()
hit_sound = pygame.mixer.Sound("resources/audio/explode.wav")
enemy_hit_sound = pygame.mixer.Sound("resources/audio/enemy.wav")
shoot_sound = pygame.mixer.Sound("resources/audio/shoot.wav")
hit_sound.set_volume(0.05)
enemy_hit_sound.set_volume(0.05)
shoot_sound.set_volume(0.05)

# background music
pygame.mixer.music.load("resources/audio/moonlight.wav")
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)

# 4 - game looping
while(running):
    
    # 5 - bersihkan layar
    screen.fill(0)
    
    # 6 - bentuk game object
    # rumputnya
    for x in range(int(width/grass.get_width()+1)):
        for y in range(int(height/grass.get_height()+1)):
            screen.blit(grass, (x*100, y*100))
	
	# markas kelincinya
    screen.blit(castle, (0, 30))
    screen.blit(castle, (0, 135))
    screen.blit(castle, (0, 240))
    screen.blit(castle, (0, 345))

    # playernya
    # ambil poisisi pointer, menghasilkan list yang menampung koordinat pointer
    # hitung besar sudut perpindahan mouse dengan math.atan2()
    # rotasi player, 57.29 dari nilai radius 360/2phi
    # gambar ulang player dengan posisi baru
    mouse_position = pygame.mouse.get_pos()
    angle = math.atan2(mouse_position[1] - (playerpos[1]+32), mouse_position[0] - (playerpos[0]+26))
    player_rotation = pygame.transform.rotate(player, 360 - angle * 57.29)
    new_playerpos = (playerpos[0] - player_rotation.get_rect().width / 2, playerpos[1] - player_rotation.get_rect().height / 2)
    screen.blit(player_rotation, new_playerpos)

    # panahnya
    # sin dan cos digunakan utk menentukan kecepatan panah dari titik awal ke titik akhir
    # jika panah sudah mencapai batas layar, hapus panah dengan fungsi pop() supaya tdk memakan banyak memori
    # lakukan increment nilai index panah
    # projectile berisi nilai koordinat awal panah dari list arrows
    for bullet in arrows:
        arrow_index = 0
        velx = math.cos(bullet[0])*10
        vely = math.sin(bullet[0])*10
        bullet[1] += velx
        bullet[2] += vely
        if bullet[1] < -64 or bullet[1] > width or bullet[2] < -64 or bullet[2] > height:
            arrows.pop(arrow_index)
        arrow_index += 1
        for projectile in arrows:
            new_arrow = pygame.transform.rotate(arrow, 360-projectile[0]*57.29)
            screen.blit(new_arrow, (projectile[1], projectile[2]))
    
    # musuhnya
    # waktu musuh akan muncul, buat musuh baru dengan append
    # rest enemy timer ke random time
    enemy_timer -= 1
    if enemy_timer == 0:
        enemies.append([width, randint(50, height-32)])
        enemy_timer = randint(1, 100)

    index = 0
    # musuh bergerak dengan v = 5px ke kiri
    # hapus musuh dengan pop() jika musuh sudah mencapai batas layar kiri
    for enemy in enemies:
        enemy[0] -= 5
        if enemy[0] < -64:
            enemies.pop(index)
        
        # collision antara enemy dan castle
        # enemy_rect adl objek rectangle utk musuh
        # bullet_rect adl objek rectangle utk anak panah
        # jika musuh menabrak markas kelinci pada x = 64, maka itu artinya kita diserang
        # mengurangi health_value saat markas diserang
        enemy_rect = pygame.Rect(enemy_img.get_rect())
        enemy_rect.top = enemy[1] # ambil titik y
        enemy_rect.left = enemy[0] # ambil titik x
        if enemy_rect.left < 64:
            enemies.pop(index)
            health_point -= randint(5, 20)
            # efek suara akan diputar dg play()
            # collision enemy dg castle
            hit_sound.play()
            print("Oh no! We are attacked!")

        # cek tabrakan
        # colliderect() utk deteksi apakah anak panah berbenturan dg musuh atau tidak
        index_arrow = 0
        for bullet in arrows:
            bullet_rect = pygame.Rect(arrow.get_rect())
            bullet_rect.left = bullet[1]
            bullet_rect.top = bullet[2]
            # benturan anak panah dengan musuh
            if enemy_rect.colliderect(bullet_rect):
                score += 1
                enemies.pop(index)
                arrows.pop(index_arrow)
                # collision arrow dg enemy
                enemy_hit_sound.play()
                print("Boom! You're dead!")
                print("Score: {}".format(score))
            index_arrow += 1
        index += 1

    # gambar musuh ke layar
    for enemy in enemies:
        screen.blit(enemy_img, enemy)
    
    # health barnya
    screen.blit(healthbar, (5,5))
    for hp in range(health_point):
        screen.blit(health, (hp+8, 8))

    # countdown dan jamnya
    # objek font digunakan untuk membuat text
    # countdown didapatkan dari get_ticks()
    # render() pada objek font digunakan utk render teks ke layar
    # parameter render() yaitu text atau teks yg akan ditampilkan,
    # lalu antialias agar teksnya terlihat mulus, nilainya adl True
    # lalu parameter terakhir adl nilai warna. (255, 255, 255) adl warna putih
    font = pygame.font.Font(None, 24)
    minutes = int((countdown_timer-pygame.time.get_ticks())/60000) # 60000 sama dg 60 s
    seconds = int((countdown_timer-pygame.time.get_ticks()/1000%60))
    time_text = "{:02}:{:02}".format(minutes, seconds)
    clock = font.render(time_text, True, (255,255,255))
    textRect = clock.get_rect()
    textRect.topright = [635, 5]
    screen.blit(clock, textRect)

    # 7 - update screen
    pygame.display.flip()

    # 8 - event loop
    for event in pygame.event.get():
        # event ketika tombol exit diklik
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        
        # fire
        if event.type == pygame.MOUSEBUTTONDOWN:
            arrows.append([angle, new_playerpos[0]+32, new_playerpos[1]+32])
            shoot_sound.play()

        # check keydown and keyup
        # pengecekan tombol wasd
        if event.type == pygame.KEYDOWN:
            if event.key == K_w:
                keys["top"] = True
            elif event.key == K_a:
                keys["left"] = True
            elif event.key == K_s:
                keys["bottom"] = True
            elif event.key == K_d:
                keys["right"] = True
        if event.type == pygame.KEYUP:
            if event.key == K_w:
                keys["top"] = False
            elif event.key == K_a:
                keys["left"] = False
            elif event.key == K_s:
                keys["bottom"] = False
            elif event.key == K_d:
                keys["right"] = False

    # 9 - move the player sejauh 5 px
    if keys["top"]:
        playerpos[1] -= 5 # kurangi nilai y
    elif keys["bottom"]:
        playerpos[1] += 5 # tambah nilai y
    if keys["left"]:
        playerpos[0] -= 5 # kurangi nilai x
    elif keys["right"]:
        playerpos[0] += 5 # tambah nilai x
    
    # 10 - win/lose check
    if pygame.time.get_ticks() > countdown_timer:
        running = False
        exitcode = EXIT_CODE_WIN
    if health_point <= 0:
        running = False
        exitcode = EXIT_CODE_GAME_OVER

# 11 - win/lose display
if exitcode == EXIT_CODE_GAME_OVER:
	screen.blit(gameover, (0, 0))
else:
	screen.blit(youwin, (0, 0))

# tampilkan score
text = font.render("Score: {}".format(score), True, (255, 255, 255))
textRect = text.get_rect()
textRect.centerx = screen.get_rect().centerx
textRect.centery = screen.get_rect().centery + 24
screen.blit(text, textRect)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit(0)
	pygame.display.flip()