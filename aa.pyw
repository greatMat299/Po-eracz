
import random
import time
import sys
import pygame
import testGIF

pygame.init()

# -----------------------inicjalizacja przed grą------------------------
# zmienne elementów
WIDTH, HEIGHT = 1400, 650
playerWidth, playerHeight = 210, 210
x, y = WIDTH // 2, HEIGHT // 2
speed = 10
rekinX = 10
rekinY = HEIGHT // 2
coinFont = pygame.font.SysFont("Rubik", 50)
laserAlertFont = pygame.font.SysFont("OCR A Extended", 50)

# dźwięki
chaseTheme = pygame.mixer.Sound("chase_theme.mp3")
laserTheme = pygame.mixer.Sound("laser.mp3")
loseTheme = pygame.mixer.Sound("lose2.wav")
gejzerExplTheme = pygame.mixer.Sound("gejzer_explosion.mp3")
glonTheme = pygame.mixer.Sound("glon.wav")
coinTheme = pygame.mixer.Sound("coin.mp3")
laserAlertTheme = pygame.mixer.Sound("laserAlert.mp3")
closeToRekinTheme = pygame.mixer.Sound("closeToRekin.mp3")

# ustawienia animacji

# kolory

black = (0, 0, 0)
yellow= (255,255,0)
white = (255, 255, 255)
gray = (55,55,55)

# Funkcje pygame

ryba = []
for _ in range(0, 2):
    ryba.append(pygame.image.load(f"b{_}.png"))
rekinLista = []
for _ in range(0, 4):
    rekinLista.append(pygame.image.load(f"shark{_}.png"))


background = pygame.image.load("sea.jpg")
backgroundWidth = background.get_width()
pygame.display.set_caption("Test")
bgs = [background, background]
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

playerImage = pygame.image.load('b0.png').convert_alpha()
playerImage = pygame.transform.scale(playerImage, (playerWidth, playerHeight))
rekinImage = pygame.image.load('shark0.png').convert_alpha()
rekinImage = pygame.transform.scale(rekinImage, (WIDTH / 2, HEIGHT / 1))
coinImage = pygame.image.load('coin.png').convert_alpha()
coinImage = pygame.transform.scale(coinImage, (75, 85))
gradientImage = pygame.image.load('gradient.png').convert_alpha()
gradientImage = pygame.transform.scale(gradientImage, (WIDTH, HEIGHT))
redGradientImage = pygame.image.load('red_gradient.png').convert_alpha()
redGradientImage = pygame.transform.scale(redGradientImage, (WIDTH, HEIGHT))
blueGradientImage = pygame.image.load('blue_gradient.png').convert_alpha()
blueGradientImage = pygame.transform.scale(blueGradientImage, (WIDTH, HEIGHT))
pilaImage = pygame.image.load('pila.png').convert_alpha()
pilaImage = pygame.transform.scale(pilaImage, (225,150))

player = pygame.Rect(x, y, 100, 70)
laser = pygame.Rect(x, y, WIDTH, playerHeight//3)

smieci = []

for _ in range(9):
    smiec = pygame.image.load(f"smiec{_}.png")
    smiec = pygame.transform.scale(smiec, (100,100))
    smieci.append(smiec)

wszystkiePrzeszkody = []
przeszkody = []
monety = []
gejzery = []
glony = []
pily = []
for _ in range(9):
    Px = WIDTH + (1500 * _)
    Py = round(random.randint(0 + 50, HEIGHT - 50), -2)
    print(Py)
    przeszkoda = pygame.Rect(Px, Py, 100, 60)
    przeszkody.append(przeszkoda)
    wszystkiePrzeszkody.append(przeszkoda)
for _ in range(5):
    Mx = WIDTH + 300 * _
    My = random.randint(0 + 50, HEIGHT - 50)
    moneta = pygame.Rect(Mx, My, 75, 85)
    monety.append(moneta)
    wszystkiePrzeszkody.append(moneta)
for _ in range(2):
    Gx = WIDTH + 4300 * _
    Gy = random.randint(0 + 50, HEIGHT - 50)
    gejzer = pygame.Rect(Gx, Gy, 200, 50)
    gejzery.append(gejzer)
    wszystkiePrzeszkody.append(gejzer)
for _ in range(3):
    Glx = WIDTH + 600 * _
    Gly = random.randint(0 + 50, HEIGHT - 50)
    glon = pygame.Rect(Glx, Gly, 150, 100)
    glony.append(glon)
    wszystkiePrzeszkody.append(glon)
for _ in range(2):
    PilX = WIDTH + 50 * random.randint(10,300)
    PilY = random.randint(0 + 90, HEIGHT - 90)
    pila = pygame.Rect(PilX, PilY, 225, 80)
    pily.append(pila)

# print(*przeszkody)

# --------------------funkcje---------------------
def ruch(klawisz, pla, czyUmarl):
    if czyUmarl == False:
        if klawisz[pygame.K_d]:
            if pla.x < WIDTH // 2:
                pla.x += 3
        if klawisz[pygame.K_a]:
            if pla.x > 0:
                pla.x -= speed / 2
        if klawisz[pygame.K_w]:
            if pla.y > 0:
                pla.y -= speed
        if klawisz[pygame.K_s]:
            if pla.y < HEIGHT - playerHeight + 140:
                pla.y += speed


# ruch tła i sprawdzanie czy D zostało naciśnięte
def tlo(bgX, bgY, klawisz, czyUmarl, czyBiegnie):
    # przesuwaj tło jeżeli gracz żyje
    predkoscAnimacjiD = 10
    predkoscAnimacji = 10
    if czyUmarl == False:
        speed = 3
        sprint = 1
        shake = 5

        if klawisz[pygame.K_d]:
            predkoscAnimacjiD = 4
            czyBiegnie = True
            if bgX % 2 == 0:
                bgX = bgX
                bgY -= shake
            else:
                bgY += shake
            sprint = 3
        else:
            czyBiegnie = False
        bgX -= speed * sprint
    return bgX, bgY, predkoscAnimacjiD,predkoscAnimacji, czyBiegnie




def muzyka():
    a = pygame.mixer.Sound.play(chaseTheme)  # muzyka w tle
    a = pygame.mixer_music.load("chase_theme.mp3")
    a = pygame.mixer_music.play(-1)
    main(player, playerImage, x, y,rekinImage)


def smierc(ileMonet):

    run = True
    death = pygame.mixer.Sound('death.mp3')
    pygame.mixer.Sound.play(death)

    bg = pygame.Rect(0, 0, WIDTH, HEIGHT)
    pygame.draw.rect(screen, black, bg)
    pygame.display.update()
    time.sleep(2.2)


    wybor = -1
    zgon_font = pygame.font.SysFont("Comic Sans", 100)
    tekst_zgonu = zgon_font.render("Zostałeś zjedzony", True, white)

    tekstTak = zgon_font.render("Respawn",True, gray)
    tekstNie = zgon_font.render("Give Up...",True, gray)

    text_rect = tekst_zgonu.get_rect(center=(WIDTH // 2, HEIGHT // 3 - 50))
    font = pygame.font.SysFont("Comic Sans", 36)
    iloscMonet = font.render(f"Score: {ileMonet}", True, yellow)
    textTak = font.render("Respawn!", True, gray)
    textNie = font.render("Give Up...", True, gray)
    petla = 0
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keyboard = pygame.key.get_pressed()


        bg = pygame.Rect(0, 0, WIDTH, HEIGHT)
        if petla == 40:
            pygame.draw.rect(screen,(random.randint(20,30),random.randint(0,20),random.randint(0,20)),bg)
            petla = 0
        # Rysuj napis "Zostałeś zjedzony"

        shake = 6
        if petla%39==0:
            screen.blit(tekst_zgonu, (WIDTH//5+shake,HEIGHT//4))
            screen.blit(iloscMonet, ((WIDTH // 2.4 + 50 + shake - 3), HEIGHT // 1.7))
        else:
            screen.blit(tekst_zgonu, (WIDTH // 5, HEIGHT // 4))
            screen.blit(iloscMonet, ((WIDTH // 2.4 + 50), HEIGHT // 1.7))
        screen.blit(textTak, (WIDTH//4.5,HEIGHT//2))
        screen.blit(textNie, (WIDTH//1.5,HEIGHT//2))

        if keyboard[pygame.K_a]:
            wybor = 0
            textTak = font.render("Respawn!", True, white)
            textNie = font.render("Give Up...", True, gray)
        elif keyboard[pygame.K_d]:
            wybor = 1
            textNie = font.render("Give Up...", True, (255,0,0))
            textTak = font.render("Respawn!", True, gray)
        if keyboard[pygame.K_SPACE] or keyboard[pygame.K_RETURN] or keyboard[pygame.K_e]:
            match wybor:
                case 0:
                    print("Respenie")
                    pygame.mixer.quit()
                    pygame.mixer.init()
                    muzyka()
                case 1:
                    sys.exit()
                case _:
                    print("bim")
        petla+= 1
        pygame.display.update()

def kolizja(blok, player):
    if player.x + playerWidth <= blok.x + 150:
        player.x = blok.x - 100
    elif player.y >= blok.y - player.height and player.y < blok.y + blok.height / 2:
        player.y -= speed
    elif player.y >= blok.y:
        player.y += speed



# -------------------------główna gra-----------------------

# uciekanie
def main(player, playerImage, x, y, rekinImage):
    player = pygame.Rect(x, y, 100, 70)
    rekin = pygame.Rect(-100, y, 100, 100)
    updateRekin = 0
    updateAnimacjaF = 0
    updateAnimacjaS = 0
    wykonanoAnimacjaF = 0
    wykonanoAnimacjaS = 0
    restAnimacja = 0
    predkosc = 1
    speed = 10
    current_frame = 0
    bgX = 0
    bgY = 0
    gejzerPower = 350
    ileMonet = 0
    ileLaserow = 3
    theScore = 0

    run = True
    czyUmarl = False
    czyBiegnie = False
    czyLaser = False
    czyMozeLaser = True
    czyWGlonie = False
    czySpaniePowerup = False
    czyMozeSpanie = True
    czyBliskoRekin = False

    ileCzasuLaser = 60  # laser trwa 60 klatek, czyli 1 sekundę (jeżeli mamy 60 fps)
    ileCzasuSpanie = 60  # moc spania trwa 60 sekund
    time_delay = 10000  # 10 sekund cooldownu na laser
    laser_timer = pygame.USEREVENT + 1

    while run:
        # screen.fill(black)
        # eventy
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == laser_timer and czyUmarl==False:
                if czyMozeLaser==False:
                    print("laser online")
                    pygame.mixer.Sound.play(laserAlertTheme)
                    czyMozeLaser=True
        # wczytywanie klawiszy
        if czyUmarl == False:
            klawisz = pygame.key.get_pressed()
        # ruch gora, dol, lewo(bez prawej)
        ruch(klawisz, player, czyUmarl)

        # theScore+=1.666667
        # print(round((theScore/100.0),-2))

        # scrollowanie tła
        for i in range(2):
            if i == 0:
                screen.blit(bgs[i], (backgroundWidth * i + bgX, bgY - 20))

            else:
                screen.blit(bgs[i], (backgroundWidth * i + bgX - 3, bgY - 20))

        # sprawdzanie czy tło wyszło poza pole widzenia
        if -bgX > backgroundWidth:
            bgX = 0

        # pobranie nowych zmiennych do scrollowania tła
        bgX, bgY, predkoscAnimacjiD, predkoscAnimacji, czyBiegnie = tlo(bgX, bgY, klawisz, czyUmarl, czyBiegnie)

        # gracz
        if updateAnimacjaF > predkoscAnimacjiD:
            playerImage = testGIF.updateFish(ryba, wykonanoAnimacjaF)
            updateAnimacjaF = 0
            wykonanoAnimacjaF += 1
        if wykonanoAnimacjaF == len(ryba):
            wykonanoAnimacjaF = 0
        updateAnimacjaF += 1


        # pygame.draw.rect(screen,white,player)    # !!!!!!!!!!!!!!!!!!!!!!!!!!!POKAZUJE KOLIZJE RYBY!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        # rekin
        if updateAnimacjaS > predkoscAnimacji:
             rekinImage = testGIF.updateShark(rekinLista, wykonanoAnimacjaS)
             updateAnimacjaS = 0
             wykonanoAnimacjaS += 1
        if wykonanoAnimacjaS == len(rekinLista):
             wykonanoAnimacjaS = 0
             updateAnimacjaS += 1
        updateAnimacjaS+=1

        if updateRekin == 1:
            rekinSpeed = 5
            if rekin.y > player.y - rekin.height * 3.2:
                if rekin.y - rekin.height < HEIGHT:
                    rekin.y -= rekinSpeed
            elif rekin.y < player.y - rekin.height * 3.2:
                if rekin.y < HEIGHT - 400:
                    rekin.y += rekinSpeed
            screen.blit(rekinImage, (-280, rekin.y))
            updateRekin = 0
        updateRekin += 1

        # akcje mocy "spania"
        if klawisz[pygame.K_t] and czyMozeSpanie == True and czyLaser == False:
            if czySpaniePowerup == False:
                czySpaniePowerup = True

        if czySpaniePowerup == True:
            screen.blit(blueGradientImage, (0, 0))
            if ileCzasuSpanie >= 0:
                ileCzasuSpanie -= 1
                print(ileCzasuSpanie)

        if ileCzasuSpanie == 0:
            if czySpaniePowerup == True:
                ileCzasuSpanie = 60
                print("spanie 0")
                czySpaniePowerup = False
                czyMozeSpanie = False

        # akcje laseru
        if klawisz[pygame.K_SPACE] and czyMozeLaser == True and ileLaserow > 0 and czySpaniePowerup == False:
            if czyLaser == False:
                pygame.mixer.Sound.play(laserTheme)
            czyLaser = True

        if czyLaser == True and ileCzasuLaser >= 0:
            ileCzasuLaser -= 1
            pygame.draw.rect(screen, (255, 0, 0), laser)
            laser.y = player.y
            laser.x = player.x+50
        screen.blit(playerImage, (player.x - 40, player.y - 77))
        if ileCzasuLaser == 0:
            if czyLaser == True and ileLaserow > 0:
                pygame.mixer.Sound.stop(laserTheme)
                ileCzasuLaser = 60
                ileLaserow -= 1
                pygame.time.set_timer(laser_timer, time_delay)
                czyMozeLaser = False
                czyLaser = False

        # pojawanie się przeszkód

        # if czyUmarl == False:
        #     for a in przeszkody:
        #         #pygame.draw.rect(screen, white, a)
        #     for b in monety:
        #         #screen.blit(coinImage, (b.x, b.y))
        #     #for przeszkoda in przeszkody:
        #         if b.colliderect(przeszkoda):
        #             b.y += 20
        #     # for c in gejzery:
        #     #     pygame.draw.rect(screen, black, c)
        #     for d in glony:
        #         #pygame.draw.rect(screen, (0, 255, 0), d)

        # przesuwanie sie przeszkód
        # for e in wszystkiePrzeszkody:
        #     if e.x > 0 - e.width:
        #         if klawisz[pygame.K_d]:
        #             e.x -= speed * 1.5
        #         else:
        #             fish = pygame.transform.scale(fish,(100,100))
        #             e.x -= speed
        #             screen.blit(fish, (e.x, e.y))
        #     else:
        #         e.x = WIDTH + e.width
        #         e.y = round(random.randint(0, HEIGHT), -2)
        if czySpaniePowerup==False:
            for e in przeszkody:
                if e.x > 0 - e.width:
                    for smiec in smieci:
                        if smieci.index(smiec) == przeszkody.index(e):
                            smiec = pygame.transform.scale(smiec, (150, 100))
                            if klawisz[pygame.K_d]:
                                e.x -= speed * 1.5
                            else:

                                e.x -= speed
                            screen.blit(smiec, (e.x, e.y))
                else:
                    e.x = WIDTH + e.width
                    e.y = round(random.randint(0, HEIGHT), -2)

            glon = pygame.image.load("glon.png")

            for e in glony:
                glon = pygame.transform.scale(glon, (150, 200))
                if e.x > 0 - e.width:
                    if klawisz[pygame.K_d]:
                        e.x -= speed * 1.5
                    else:
                        e.x -= speed
                    screen.blit(glon, (e.x, e.y-50))
                else:
                    e.x = WIDTH + e.width
                    e.y = round(random.randint(0, HEIGHT))

            moneta = pygame.image.load("coin.png")

            for e in monety:
                moneta = pygame.transform.scale(moneta, (100, 100))
                if e.x > 0 - e.width:
                    if klawisz[pygame.K_d]:
                        e.x -= speed * 1.5
                        screen.blit(moneta, (e.x, e.y - 50))
                    else:
                        e.x -= speed
                        screen.blit(moneta, (e.x, e.y - 50))
                else:
                    e.x = WIDTH + e.width
                    e.y = round(random.randint(0, HEIGHT), -2)

            for e in wszystkiePrzeszkody:
                if e.x < rekin.x+400 and e.y > rekin.y+200 and e.y < rekin.y+400 :
                    e.x = 3000
                    e.y = random.randint(0,HEIGHT-e.height)

        for pila in pily:
            # pygame.draw.rect(screen, (50, 50, 50), pila)
            screen.blit(pilaImage, (pila.x, pila.y - 30))
            pila.x -= 18
            if pila.x > 0 - pila.width:
                if klawisz[pygame.K_d]:
                    pila.x -= speed * 1.5
                else:
                    pila.x -= speed
            else:
                pila.y = round(random.randint(0 + 30, HEIGHT - 30), -2)
                pila.x = WIDTH + 50 * random.randint(10, 300)

        # sprawdza czy laser dotyka przeszkody
        if laser.collidelistall(przeszkody) and czyLaser == True:
            h = laser.collidelistall(przeszkody)
            przeszLaser = przeszkody[h[0]]
            przeszLaser.y += HEIGHT * 2

        # sprawdza czy laser dotyka przeszkody
        if laser.collidelistall(pily) and czyLaser == True:
            h = laser.collidelistall(pily)
            pilaLaser = pily[h[0]]
            pilaLaser.y += HEIGHT * 2

        # sprawdza czy gracz dotknął jakikolwiek element z listy 'przeszkody'
        if player.collidelistall(przeszkody) and czyUmarl==False and czySpaniePowerup==False:
            a = player.collidelistall(przeszkody)
            blok = przeszkody[a[0]]
            # obiekty blokują gracza
            kolizja(blok, player)

        # sprawdza czy gracz dotknął jakikolwiek element z listy 'pily'
        if player.collidelistall(pily) and czyUmarl == False and czySpaniePowerup == False:
            a = player.collidelistall(pily)
            pilyPrzesz = pily[a[0]]
            kolizja(pilyPrzesz, player)

        # sprawdza czy gracz dotknął jakikolwiek element z listy 'monety'
        if player.collidelistall(monety) and czyUmarl == False and czySpaniePowerup == False:
            a = player.collidelistall(monety)
            monetaPrzesz = monety[a[0]]
            # moneta znika z pola widzenia, po czym 1 punkt jest dodawany
            monetaPrzesz.y = HEIGHT * 2
            ileMonet += 1
            # przesuwanie monet jeżeli one są w przeszkodzie

        # sprawdza czy gracz dotknął jakikolwiek element z listy 'glony'
        if player.collidelistall(glony) and czyUmarl==False and czySpaniePowerup==False:
            a = player.collidelistall(glony)
            glonPrzesz = glony[a[0]]
            if czyWGlonie == False:
                pygame.mixer.Sound.play(glonTheme)
                czyWGlonie = True
            # prędkość gracza zmiejsza się do 5 po dotknięciu glonu
            speed = 5
            if czyUmarl == False:
                player.x -= 5
            for przeszkoda in przeszkody:
                if glonPrzesz.colliderect(przeszkoda):
                    glonPrzesz.y += 30
        else:
            speed = 10
            pygame.mixer.Sound.stop(glonTheme)
            czyWGlonie = False
            # glonPrzesz.y = HEIGHT * 2

        # sprawdza czy gracz dotknął jakikolwiek element z listy 'gejzery'
        if player.collidelistall(gejzery) and czyUmarl==False and czySpaniePowerup==False:
            a = player.collidelistall(gejzery)
            gejzerPrzesz = glony[a[0]]
            # gracz jest "eksplodowany" o 350 pikseli w górę po dotknięciu gejzeru
            player.y -= gejzerPower
            pygame.mixer.Sound.play(gejzerExplTheme)
            # jeżeli gracz będzie wystrzelony poza obszar widzenia, wraca on na samą górę (y=0)
            if player.y < 0:
                player.y = 0

        # sprawdza czy gracz jest w strefie rekina i go uśmierca
        # print(player.x)
        # print(rekin.x+rekinImage.get_width()/2)
        if player.x < rekin.x + rekinImage.get_width() / 2:
            if czyUmarl == False:
                pygame.mixer.Sound.play(loseTheme)
                pygame.mixer.Sound.stop(closeToRekinTheme)
                print("Powód zgonu: Covid-19")
                czyUmarl = True
                czyBiegnie = False
                speed = 0
                pygame.mixer.Sound.stop(chaseTheme)
                break
        # sprawdza czy gracz jest blisko rekina i daje czerwony gradient
        elif player.x < (rekin.x + rekinImage.get_width() / 2) + 80:
            screen.blit(redGradientImage, (0, 0))
            if czyBliskoRekin == False:
                print("blisko rekin")
                pygame.mixer.Sound.play(closeToRekinTheme)
                chaseTheme.set_volume(0.3)
                czyBliskoRekin = True
            else:
                czyBliskoRekin = False
                pygame.mixer.Sound.stop(closeToRekinTheme)
                chaseTheme.set_volume(1)

        # aktualizowanie tekstu z punktami
        if czyUmarl == False:
            font_surface = coinFont.render(str(ileMonet), True, black)
            laserAlertFontSurface = laserAlertFont.render("LASER AKTYWNY", True, (255, 0, 0))
            if czyMozeLaser == True and czyLaser == False:
                screen.blit(laserAlertFontSurface, (WIDTH // 3, 10))
            if czyBiegnie == True:
                screen.blit(gradientImage, (0, 0))
            screen.blit(coinImage, (0, 10))
            screen.blit(font_surface, (80, 22))


        pygame.display.update()
        clock.tick(75)
    if czyUmarl:
        a = pygame.mixer_music.stop()
        smierc(ileMonet)
    pygame.quit()


if __name__ == "__main__":
    muzyka()
