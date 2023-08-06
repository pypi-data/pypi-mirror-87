import pygame, sys
import random
import math
from pygame import mixer
from pygame.locals import *

#############################################################################################

#Funcoes de mapa

#Funcao para carregar o arquivo de texto contendo o mapa
def load_map(path):
    f=open(path + '.txt','r')
    data=f.read()
    f.close()
    data=data.split('\n')
    gamemap=[]
    for row in data:
        gamemap.append(list(row))
    return gamemap

#Guarda as coordenadas dos tiles que causam "game over"
def loaddangertiles(DANGER,gamemap):
    danger_coord=[]
    for i in range(len(gamemap)-1):
        for j in range(len(gamemap[0])):
            if gamemap[i][j] in DANGER:
                danger_coord.append((32*j,32*i))
    return danger_coord

#Carrega os tiles (32x32) da pasta path
def loadtiles(path,finalnum):
    tiles_img=[]
    for i in range(1,finalnum+1):
        tile_img=pygame.image.load(path+str(i)+'.png')
        tile_img=pygame.transform.smoothscale(tile_img,(32,32))
        tiles_img.append(tile_img)
    return tiles_img

#Funcao para obter todos os retangulos de colisao
def obtainsolidrects():
    global zombies_rects
    global tile_rects
    global ADDED_TILERECTS
    global solid_rects
    global number_zombies
    global ADDED_ZOMBIES_RECTS
    if not ADDED_TILERECTS:
        for i in range(len(tile_rects)):
            solid_rects.append(tile_rects[i])
        ADDED_TILERECTS=True
    if not ADDED_ZOMBIES_RECTS:
        for i in range(number_zombies):
            solid_rects.append(zombies_rects[i])
    else:
        for i in range(len(tile_rects),len(solid_rects)):
            solid_rects[i] = zombies_rects[i-len(tile_rects)]
#Carrega um mapa com todas as suas configuracoes
def loadconfigsmap():
    global mapselection
    global gamemap
    global ADDED_TILE_RECTS
    global ADDED_ZOMBIES_RECTS
    global number_zombies
    global zombies_imgs_idle
    global zombies_imgs_idle_flip
    global zombies_imgs_walk
    global zombies_imgs_walk_flip
    global zombies_imgs_dead
    global zombies_imgs_dead_flip
    global zombies_rects
    global zombies_health
    global zombies_dead_positions
    global zombies_i
    global zombies_changestate
    global zombies_movement
    global zombies_collisions
    global zombies_states
    global checkpoint_x
    global checkpoint_y
    global CHECKPOINT_COORDINATES
    global player_rect
    global player_frame_i
    global player_reset
    global gameover
    global draw_player
    global player_running
    global tile_rects
    global solid_rects
    global danger_tiles
    global maploaded

    player_reset=False
    draw_player=True
    gameover=False
    player_running=False
    gamemap=load_map('map'+mapselection)
    ADDED_ZOMBIES_RECTS=False
    ADDED_TILE_RECTS=False
    tile_rects=[]
    solid_rects=[]
    danger_tiles=loaddangertiles(DANGER,gamemap)
    player_frame_i=0 #variavel do tipo contador, para ir mudando as imagens a cada ciclo do while, para dar a sensacao de animacao
    if mapselection == '1' or mapselection == '0':
        checkpoint_x=286
        checkpoint_y=224
        CHECKPOINT_COORDINATES=[[2610,100]]
    elif mapselection == '2':
        checkpoint_x=280 #posicao inicial do jogador
        checkpoint_y=780
        CHECKPOINT_COORDINATES=[[2610,100]]
    player_rect=pygame.Rect(checkpoint_x,checkpoint_y,player_imgs_idle[0].get_width(),player_imgs_idle[0].get_height())
    zombies_imgs_idle=[]
    zombies_imgs_idle_flip=[]
    zombies_imgs_walk=[]
    zombies_imgs_walk_flip=[]
    zombies_imgs_dead=[]
    zombies_imgs_dead_flip=[]
    zombies_rects=[]
    zombies_health=[]
    zombies_dead_positions=[]
    if mapselection == '0':
        number_zombies=0
        zombies_positions=[[]]
        zombies_states=[]
    elif mapselection == '1':
        number_zombies=4
        zombies_positions=[[2410,96],[1500,288],[3450,96],[3550,96]]
        zombies_states=['walk_r','idle_r','idle_l','walk_l']
    elif mapselection == '2':
        number_zombies=3
        zombies_positions=[[623,471],[350,471],[1317,215]]
        zombies_states=['walk_r','walk_r','walk_l']
    zombies_i=[]
    zombies_changestate=[]
    zombies_movement=[]
    zombies_collisions=[]
    for i in range(number_zombies):
        zombies_imgs_idle.append(zombie_imgs_idle)
        zombies_imgs_idle_flip.append(zombie_imgs_idle_flip)
        zombies_imgs_walk.append(zombie_imgs_walk)
        zombies_imgs_walk_flip.append(zombie_imgs_walk_flip)
        zombies_imgs_dead.append(zombie_imgs_dead)
        zombies_imgs_dead_flip.append(zombie_imgs_dead_flip)
        zombies_rects.append(pygame.Rect(zombies_positions[i][0],zombies_positions[i][1],zombie_imgs_idle[0].get_width(),zombie_imgs_idle[0].get_height()))
        zombies_movement.append([0,0])
        zombies_i.append(0)
        zombies_changestate.append(0)
        zombies_health.append(random.randint(7,10))
        zombies_dead_positions.append([0,0])
    maploaded=True

#Funcoes graficas

#Funcao para carregar uma lista de figuras, como animacoes
def load_animations(path,finalframe,name,scale=1,colorkey=(255,255,255),invertx=False): 
    animation_list=[]
    for i in range(finalframe+1):
        image=pygame.image.load(path+name+'__'+str(i)+'.png')
        image=pygame.transform.smoothscale(image,(int(image.get_width()/scale),int(image.get_height()/scale)))
        image.set_colorkey(colorkey)
        if invertx:
            image=pygame.transform.flip(image,True,False)
        animation_list.append(image)
    return animation_list

#Funcao para desenhar objetos do cenario, de acordo com o mapa selecionado
def draw_below(mapselection,scroll):
    global bush_images
    global tree_images
    global display
    global player_rect
    
    if mapselection == '1':
        
        distancePobject=calc_distance(player_rect.x,320,player_rect.y,288)
        if distancePobject < rendering_dist:
            display.blit(bush_images[0],(320-scroll[0],288-bush_images[0].get_height()-scroll[1]))
        
        distancePobject=calc_distance(player_rect.x,410,player_rect.y,288)
        if distancePobject < rendering_dist:
            display.blit(mush_images[0],(410-scroll[0],288-mush_images[0].get_height()-scroll[1]))
        
        distancePobject=calc_distance(player_rect.x,370,player_rect.y,288)
        if distancePobject < rendering_dist:
            display.blit(tree_images[2],(370-scroll[0],288-tree_images[2].get_height()-scroll[1]))
        
        distancePobject=calc_distance(player_rect.x,232,player_rect.y,288)
        if distancePobject < rendering_dist:
            display.blit(sign_images[1],(232-scroll[0],288-sign_images[1].get_height()-scroll[1]))
        
        distancePobject=calc_distance(player_rect.x,1605,player_rect.y,192)
        if distancePobject < rendering_dist: 
            display.blit(tree_images[1],(1605-scroll[0],192-tree_images[1].get_height()-scroll[1]))
       
        distancePobject=calc_distance(player_rect.x,719,player_rect.y,288)
        if distancePobject < rendering_dist: 
            display.blit(tree_images[1],(719-scroll[0],288-tree_images[1].get_height()-scroll[1]))
        
        distancePobject=calc_distance(player_rect.x,1553,player_rect.y,288)
        if distancePobject < rendering_dist:
            display.blit(stone_images[0],(1553-scroll[0],288-stone_images[0].get_height()-scroll[1]))
        
        distancePobject=calc_distance(player_rect.x,-64,player_rect.y,160)
        if distancePobject < rendering_dist:
            display.blit(stone_images[1],(-64-scroll[0],160-stone_images[1].get_height()-scroll[1]))
        
        distancePobject=calc_distance(player_rect.x,2460,player_rect.y,96)
        if distancePobject < rendering_dist:
            display.blit(stone_images[1],(2460-scroll[0],96-stone_images[1].get_height()-scroll[1]))
        
        distancePobject=calc_distance(player_rect.x,2360,player_rect.y,96)
        if distancePobject < rendering_dist:
            display.blit(bush_images[2],(2360-scroll[0],96-bush_images[2].get_height()-scroll[1]))
        
        distancePobject=calc_distance(player_rect.x,2410,player_rect.y,96)  
        if distancePobject < rendering_dist:
            display.blit(bush_images[3],(2410-scroll[0],96-bush_images[3].get_height()-scroll[1]))
        
        distancePobject=calc_distance(player_rect.x,2510,player_rect.y,100)
        if distancePobject < rendering_dist:
            display.blit(tree_images[3],(2510-scroll[0],100-tree_images[3].get_height()-scroll[1]))
        
        distancePobject=calc_distance(player_rect.x,2610,player_rect.y,100)
        if distancePobject < rendering_dist:
            display.blit(sign_images[1],(2610-scroll[0],100-sign_images[1].get_height()-scroll[1]))
        
        distancePobject=calc_distance(player_rect.x,3350,player_rect.y,96)
        if distancePobject < rendering_dist:
            display.blit(stone_images[1],(3350-scroll[0],96-stone_images[1].get_height()-scroll[1]))

        distancePobject=calc_distance(player_rect.x,3500,player_rect.y,96)
        if distancePobject < rendering_dist:
            display.blit(stone_images[1],(3500-scroll[0],96-stone_images[1].get_height()-scroll[1]))
        
        distancePobject=calc_distance(player_rect.x,3420,player_rect.y,96)
        if distancePobject < rendering_dist:
            display.blit(tree_images[2],(3520-scroll[0],96-tree_images[2].get_height()-scroll[1]))
        
        distancePobject=calc_distance(player_rect.x,4876,player_rect.y,256)
        if distancePobject < rendering_dist:
            display.blit(sign_images[0],(4876-scroll[0],256-sign_images[0].get_height()-scroll[1]))

# Funcoes de jogabilidade

#Funcao para calculo de distancia
def calc_distance(xa,xb,ya,yb):
    distance=math.sqrt((xa-xb)**2+(ya-yb)**2)
    return distance

#Funcao para fazer um fade out 
def fade_out(blockfade):
    global display
    global FADEOUT
    global alphaF
    global fade_image
    global fade_event
    if fade_event:
        if not blockfade:
            if alphaF < 255 and not FADEOUT:
                alphaF+=15
            elif alphaF >= 255 and not FADEOUT:
                FADEOUT=True
            elif alphaF <= 255 and alphaF > 0 and FADEOUT:
                alphaF-=15
            elif alphaF == 0 and FADEOUT:
                FADEOUT=False
                fade_event=False
            fade_image.set_alpha(alphaF)
            display.blit(fade_image,(0,0))
        else:
            display.blit(fade_image,(0,0))

#Funcao que mantem o movimento do kunai, e mantem a variavel de estado em True 
def kunai_throw(x,y,img,display): 
    global kunai_state
    kunai_state=True
    display.blit(img,(x+10,y+18)) 

#Verifica se o kunai colide com inimigos
def checkcollisionkunaienemy():
    global kunai_rect
    global zombies_rects
    global zombies_health
    global zombies_states
    global blood_imgs
    global blood_imgs_flip
    global blood_frame
    global blood_x
    global blood_y
    global display
    
    for i in range(len(zombies_rects)):
        if kunai_right:
            distanceZkunai=calc_distance(kunai_rect.right,zombies_rects[i].left,kunai_rect.y,zombies_rects[i].y)
        elif kunai_left:
            distanceZkunai=calc_distance(kunai_rect.left,zombies_rects[i].right,kunai_rect.y,zombies_rects[i].y)
        if distanceZkunai < 35:           
            kunaistab_sound.play()
            if zombies_health[i]>0:
                zombies_health[i]-=1

#Verifica colisao do player com inimigos
def checkcollisionzombies():
    global player_rect
    global zombies_rects
    global player_reset
    global draw_player
    global player_lives
    global gameover
    global player_running 

    collisionfromtop=False
    for i in range(len(zombies_rects)):
        if abs(player_rect.x - zombies_rects[i].x) < 100:
            if abs(player_rect.y - zombies_rects[i].y) >= player_imgs_idle[0].get_height():
                collisionfromtop=True
                distancePzombies=calc_distance(player_rect.x,zombies_rects[i].x,player_rect.bottom,zombies_rects[i].y)
            else:
                distancePzombies = calc_distance(player_rect.x,zombies_rects[i].x,player_rect.y,zombies_rects[i].y)
            if collisionfromtop:
                collisiondetect=11.5
            else:
                collisiondetect=50
            if distancePzombies < collisiondetect:
                if not player_reset:
                    if draw_player:
                        player_reset=True
                        player_running=False
                        draw_player=False
                        player_lives-=1
                        if player_lives == 0:
                            gameover=True
                            pygame.mixer.music.fadeout(200)
                            gameover_sound.play()

#Funcao para verificar se ocorreu alguma colisao, de um certo retangulo em relacao a todos os tiles
def collision_test(rect,tiles):
    hit_list=[] 
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

#Funcao para movimentar um retangulo 'rect' , de acordo com seu movimento[x,y] , caso nao esteja colidindo com nenhum tile
def move(rect,movement,collision_rects):
    collision_types = {'top': False, 'bottom': False , 'right': False , 'left': False}
    rect.x+=movement[0] #realiza movimento em x
    hit_list=collision_test(rect,collision_rects)
    for tile in hit_list: #retangulo colidiu
        if movement[0] > 0: #colidiu com algo à direita
            rect.right = tile.left # .right = coord. x da borda direita , .left = coord.x da borda esquerda
            collision_types['right'] = True
        elif movement[0] < 0:#colidiu com algo à esquerda
            rect.left = tile.right
            collision_types['left']=True
    rect.y+=movement[1] #realiza movimento em y
    hit_list=collision_test(rect,collision_rects)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom=tile.top
            collision_types['bottom']= True
        elif movement[1] < 0:
            rect.top =tile.bottom
            collision_types['top']=True
    return rect, collision_types

################################################################################################################

#Valor inicial das variaveis

#variaveis de mapa 
printdebug=False
debug=False
mapselection= '1'
gamemap=load_map('map'+mapselection)
rendering_dist=500
maploaded=False
tile_rects=[]
COLLIDE_OFF=['H','I','0','J','5']
DANGER=['H','J']
danger_tiles=loaddangertiles(DANGER,gamemap)
solid_rects=[]
tiles_img=loadtiles('sprites/tileset/Tiles/',19)
TILE_SIZE=tiles_img[0].get_width()
ADDED_TILERECTS=False
ADDED_ZOMBIES_RECTS=False

#configuracaoes iniciais do pygame
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.set_num_channels(64)
clock=pygame.time.Clock() #variavel que será usada para limitar o jogo à 60 fps
pygame.display.set_caption('Ninja vs Zombies') #definindo o título
WINDOW_SIZE=(1280,768) #definindo tamanho da janela
screen = pygame.display.set_mode(WINDOW_SIZE,0,32) #definindo janela
display = pygame.Surface((640,384)) #superficie onde iremos desenhar os graficos do jogo

#variaveis de jogabilidade
player_lives=3
kunai_ammunition=30
player_reset=False
draw_player=True
gameover=False
player_running=False
gameover_img=pygame.image.load('sprites/gameover.jpg')
blockfade=False
fade_image=pygame.image.load('sprites/fade.png')
FADEOUT=False
fade_event=False
alphaF=0
alphaG=0

#fontes de texto
baby_font=pygame.font.Font('sprites/Baby Lovely.ttf',40)
baby_font_render_lives=baby_font.render(str(player_lives),True,(130,7,74))
baby_font_render_ammunition=baby_font.render(str(kunai_ammunition),True,(150,7,74))

#Imagens

#objetos e cenario
bg_image=pygame.image.load('sprites/tileset/BG/BG.png') #Imagem de fundo 
bush_images=load_animations('sprites/tileset/Object/',3,'Bush',1)
tree_images=load_animations('sprites/tileset/Object/',3,'Tree',1)
mush_images=load_animations('sprites/tileset/Object/',1,'Mushroom',1)
stone_images=load_animations('sprites/tileset/Object/',1,'Stone',1)
sign_images=load_animations('sprites/tileset/Object/',1,'Sign',1)

#hud
hud_head=pygame.image.load('sprites/hud_head.png')
hud_head=pygame.transform.smoothscale(hud_head,(hud_head.get_width()//2,hud_head.get_height()//2))
hud_kunai=pygame.image.load('sprites/hud_kunai.png')
hud_kunai=pygame.transform.smoothscale(hud_kunai,(hud_kunai.get_width()//2,hud_kunai.get_height()//2))

#jogador
player_imgs_idle=load_animations('sprites/ninja/',9,'Idle',3.2)
player_imgs_idle_flip=load_animations('sprites/ninja/',9,'Idle',3.2,(255,255,255),True)
player_imgs_run=load_animations('sprites/ninja/',9,'Run',3.2)
player_imgs_run_flip=load_animations('sprites/ninja/',9,'Run',3.2,(255,255,255),True)
player_imgs_jump=load_animations('sprites/ninja/',9,'Jump',3.2)
player_imgs_jump_flip=load_animations('sprites/ninja/',9,'Jump',3.2,(255,255,255),True)
player_imgs_throw=load_animations('sprites/ninja/',9,'Throw',3.2)
player_imgs_throw_flip=load_animations('sprites/ninja/',9,'Throw',3.2,(255,255,255),True)
player_imgs_jump_throw=load_animations('sprites/ninja/',9,'Jump_Throw',3.2)
player_imgs_jump_throw_flip=load_animations('sprites/ninja/',9,'Jump_Throw',3.2,(255,255,255),True)
kunai_img=pygame.image.load('sprites/tileset/Object/Kunai_0.png')
kunai_img=pygame.transform.smoothscale(kunai_img,(int(kunai_img.get_width()/3),int(kunai_img.get_height()/3)))
kunai_img_flip=pygame.transform.flip(kunai_img,True,False)

#zumbi1
zombie_imgs_idle=load_animations('sprites/zombie_m/',14,'Idle',3.4)
zombie_imgs_idle_flip=load_animations('sprites/zombie_m/',14,'Idle',3.4,(255,255,255),True)
zombie_imgs_walk=load_animations('sprites/zombie_m/',9,'Walk',3.4)
zombie_imgs_walk_flip=load_animations('sprites/zombie_m/',9,'Walk',3.4,(255,255,255),True)
zombie_imgs_dead=load_animations('sprites/zombie_m/',12,'Dead',3.3)
zombie_imgs_dead_flip=load_animations('sprites/zombie_m/',12,'Dead',3.3,(255,255,255),True)
blood_imgs=load_animations('sprites/blood/',16,'blood',3)
blood_imgs_flip=load_animations('sprites/blood/',16,'blood',3,(255,255,255),True)
blood_frame=0

#Sons e musicas

mixer.music.load('sounds/guitar1.mp3')
mixer.music.play(-1) #-1: Carrega musica em loop
gameover_sound=mixer.Sound('sounds/gameover.wav')
kunaithrow_sound=mixer.Sound('sounds/knifethrow.wav')
kunaistab_sound=mixer.Sound('sounds/knifestab.wav')

#variaveis de sistema

#Jogador e inimigo
player_frame_i=0 #variavel do tipo contador, para ir mudando as imagens a cada ciclo do while, para dar a sensacao de animacao
player_rect=pygame.Rect(0,0,player_imgs_idle[0].get_width(),player_imgs_idle[0].get_height()) #retangulo para colisoes
zombies_imgs_idle=[]
zombies_imgs_idle_flip=[]
zombies_imgs_walk=[]
zombies_imgs_walk_flip=[]
zombies_imgs_dead=[]
zombies_imgs_dead_flip=[]
zombies_rects=[]
zombies_health=[]
zombies_dead_positions=[]
zombies_i=[]
zombies_changestate=[]
zombies_movement=[]
zombies_collisions=[]
zombies_states=[]
number_zombies=0
blood_x=0
blood_y=0

#Variaveis de movimento
moving_right=False
moving_left=False
flip_right=True #lado onde o jogador está virado
flip_left=False

#Variáveis de pulo
player_y_momentum=0
air_timer=0

#Variáveis de disparo do kunai
kunai_state=False  #True : Foi jogado o kunai. Nao podemos atirar novamente até esperar alguns frames , ou até que ele colida
kunai_state_i=0 #contador, ao atingir um certo valor o kunai some e podemos atirar novamente
kunai_rect=pygame.Rect(2000,2000,kunai_img.get_width(),kunai_img.get_height())
kunai_left=False
kunai_right=False
throwAnimation=False

#Variaveis para movimentar a tela
true_scroll=[0,0]
scroll=[0,0]

##############################################################################################################################

#Ambiente de jogo
while True: 
     
    #Configuracoes iniciais
    
    if not maploaded:
        loadconfigsmap()
    display.fill((146,244,255))
    display.blit(bg_image,(0,0))
    true_scroll[0] += ((player_rect.x-true_scroll[0])-200)/3
    true_scroll[1] += ((player_rect.y-true_scroll[1])-200)/3
    scroll[0]=int(true_scroll[0])
    scroll[1]=int(true_scroll[1])
    baby_font_render_lives=baby_font.render(str(player_lives),True,(180,17,74))
    baby_font_render_ammunition=baby_font.render(str(kunai_ammunition),True,(180,17,74))

    for checkpoint_coord in CHECKPOINT_COORDINATES:
        distancePcheckpoint=calc_distance(player_rect.x,checkpoint_coord[0],player_rect.y,checkpoint_coord[1])
        if distancePcheckpoint < 70 and checkpoint_x < checkpoint_coord[0]:
            checkpoint_x=checkpoint_coord[0]
            checkpoint_y=checkpoint_coord[1]-sign_images[1].get_height()

    #Desenha o mapa do jogo , e define retangulos de colisao
    for i in range(len(gamemap)-1): 
        for j in range(len(gamemap[0])):
            if gamemap[i][j] == '1':
                distancePtile=calc_distance(player_rect.x,j*TILE_SIZE,player_rect.y,i*TILE_SIZE)
                if distancePtile < rendering_dist:
                    display.blit(tiles_img[0],(j*TILE_SIZE-scroll[0],i*TILE_SIZE-scroll[1]))
            if gamemap[i][j] == '2':
                distancePtile=calc_distance(player_rect.x,j*TILE_SIZE,player_rect.y,i*TILE_SIZE)
                if distancePtile < rendering_dist:
                    display.blit(tiles_img[1],(j*TILE_SIZE-scroll[0],i*TILE_SIZE-scroll[1]))
            if gamemap[i][j] == '3':
                distancePtile=calc_distance(player_rect.x,j*TILE_SIZE,player_rect.y,i*TILE_SIZE)
                if distancePtile < rendering_dist:
                    display.blit(tiles_img[2],(j*TILE_SIZE-scroll[0],i*TILE_SIZE-scroll[1]))
            if gamemap[i][j] == '4':
                distancePtile=calc_distance(player_rect.x,j*TILE_SIZE,player_rect.y,i*TILE_SIZE)
                if distancePtile < rendering_dist:
                    display.blit(tiles_img[3],(j*TILE_SIZE-scroll[0],i*TILE_SIZE-scroll[1]))
            if gamemap[i][j] == '5':
                distancePtile=calc_distance(player_rect.x,j*TILE_SIZE,player_rect.y,i*TILE_SIZE)
                if distancePtile < rendering_dist:
                    display.blit(tiles_img[4],(j*TILE_SIZE-scroll[0],i*TILE_SIZE-scroll[1]))
            if gamemap[i][j] == '6':
                distancePtile=calc_distance(player_rect.x,j*TILE_SIZE,player_rect.y,i*TILE_SIZE)
                if distancePtile < rendering_dist:
                    display.blit(tiles_img[5],(j*TILE_SIZE-scroll[0],i*TILE_SIZE-scroll[1]))
            if gamemap[i][j] == '7':
                distancePtile=calc_distance(player_rect.x,j*TILE_SIZE,player_rect.y,i*TILE_SIZE)
                if distancePtile < rendering_dist:
                    display.blit(tiles_img[6],(j*TILE_SIZE-scroll[0],i*TILE_SIZE-scroll[1]))
            if gamemap[i][j] == '8':
                distancePtile=calc_distance(player_rect.x,j*TILE_SIZE,player_rect.y,i*TILE_SIZE)
                if distancePtile < rendering_dist:
                    display.blit(tiles_img[7],(j*TILE_SIZE-scroll[0],i*TILE_SIZE-scroll[1]))
            if gamemap[i][j] == '9':
                distancePtile=calc_distance(player_rect.x,j*TILE_SIZE,player_rect.y,i*TILE_SIZE)
                if distancePtile < rendering_dist:
                    display.blit(tiles_img[8],(j*TILE_SIZE-scroll[0],i*TILE_SIZE-scroll[1]))
            if gamemap[i][j] == 'A':
                distancePtile=calc_distance(player_rect.x,j*TILE_SIZE,player_rect.y,i*TILE_SIZE)
                if distancePtile < rendering_dist:
                    display.blit(tiles_img[9],(j*TILE_SIZE-scroll[0],i*TILE_SIZE-scroll[1]))
            if gamemap[i][j] == 'B':
                distancePtile=calc_distance(player_rect.x,j*TILE_SIZE,player_rect.y,i*TILE_SIZE)
                if distancePtile < rendering_dist:
                    display.blit(tiles_img[10],(j*TILE_SIZE-scroll[0],i*TILE_SIZE-scroll[1]))
            if gamemap[i][j] == 'C':
                distancePtile=calc_distance(player_rect.x,j*TILE_SIZE,player_rect.y,i*TILE_SIZE)
                if distancePtile < rendering_dist:
                    display.blit(tiles_img[11],(j*TILE_SIZE-scroll[0],i*TILE_SIZE-scroll[1]))
            if gamemap[i][j] == 'D':
                distancePtile=calc_distance(player_rect.x,j*TILE_SIZE,player_rect.y,i*TILE_SIZE)
                if distancePtile < rendering_dist:
                    display.blit(tiles_img[12],(j*TILE_SIZE-scroll[0],i*TILE_SIZE-scroll[1]))
            if gamemap[i][j] == 'E':
                distancePtile=calc_distance(player_rect.x,j*TILE_SIZE,player_rect.y,i*TILE_SIZE)
                if distancePtile < rendering_dist:
                    display.blit(tiles_img[13],(j*TILE_SIZE-scroll[0],i*TILE_SIZE-scroll[1]))
            if gamemap[i][j] == 'F':
                distancePtile=calc_distance(player_rect.x,j*TILE_SIZE,player_rect.y,i*TILE_SIZE)
                if distancePtile < rendering_dist:
                    display.blit(tiles_img[14],(j*TILE_SIZE-scroll[0],i*TILE_SIZE-scroll[1]))
            if gamemap[i][j] == 'G':
                distancePtile=calc_distance(player_rect.x,j*TILE_SIZE,player_rect.y,i*TILE_SIZE)
                if distancePtile < rendering_dist:
                    display.blit(tiles_img[15],(j*TILE_SIZE-scroll[0],i*TILE_SIZE-scroll[1]))
            if gamemap[i][j] == 'H':
                distancePtile=calc_distance(player_rect.x,j*TILE_SIZE,player_rect.y,i*TILE_SIZE)
                if distancePtile < rendering_dist:
                    display.blit(tiles_img[16],(j*TILE_SIZE-scroll[0],i*TILE_SIZE-scroll[1]))
            if gamemap[i][j] == 'I':
                distancePtile=calc_distance(player_rect.x,j*TILE_SIZE,player_rect.y,i*TILE_SIZE)
                if distancePtile < rendering_dist:
                    display.blit(tiles_img[17],(j*TILE_SIZE-scroll[0],i*TILE_SIZE-scroll[1]))
            if gamemap[i][j] == 'J':
                distancePtile=calc_distance(player_rect.x,j*TILE_SIZE,player_rect.y,i*TILE_SIZE)
                if distancePtile < rendering_dist:
                    display.blit(tiles_img[18],(j*TILE_SIZE-scroll[0],i*TILE_SIZE-scroll[1]))
            if gamemap[i][j] == '#':
                display.blit(tiles_img[4],(j*TILE_SIZE-scroll[0],i*TILE_SIZE-scroll[1]))
            if gamemap[i][j] == 'L':
                display.blit(tiles_img[20],(j*TILE_SIZE-scroll[0],i*TILE_SIZE-scroll[1]))
            if gamemap[i][j] not in COLLIDE_OFF:
                if pygame.Rect(j*TILE_SIZE,i*TILE_SIZE,TILE_SIZE,TILE_SIZE) not in tile_rects:
                    tile_rects.append(pygame.Rect(j*TILE_SIZE,i*TILE_SIZE,TILE_SIZE,TILE_SIZE))            
    draw_below(mapselection,scroll) #cenario
    
    #Mudanca no estado dos inimigos a cada certo tempo
    for i in range(len(zombies_changestate)):
        if zombies_health[i] == 0:
            if zombies_states[i] in ('walk_r','idle_r'):
                zombies_states[i] = 'dead_r'
                zombies_i[i]=0
                zombies_dead_positions[i][0]=zombies_rects[i].x
                zombies_dead_positions[i][1]=zombies_rects[i].y-3
            elif zombies_states[i] in ('walk_l','idle_l'):
                zombies_states[i] = 'dead_l'
                zombies_i[i]=0    
                zombies_dead_positions[i][0]=zombies_rects[i].x
                zombies_dead_positions[i][1]=zombies_rects[i].y-3
            zombies_rects[i].x=9999-i*77
            zombies_rects[i].y=-9999
            zombies_changestate[i]=0
        elif zombies_health[i] > 0:
            zombies_changestate[i]+=random.randint(0,1)
            if zombies_states[i] in ('walk_r','walk_l'):
                if zombies_changestate[i] == 30:
                    if zombies_states[i] == 'walk_r':
                        zombies_i[i]=0
                        zombies_states[i] = 'idle_r'
                        zombies_changestate[i]=0
                    elif zombies_states[i] == 'walk_l':
                        zombies_i[i]=0
                        zombies_states[i] = 'idle_l'
                        zombies_changestate[i]=0
            elif zombies_states[i] in ('idle_r','idle_l'):
                if zombies_changestate[i] == 10:
                    if zombies_states[i] == 'idle_r':
                        zombie_sortmovement=random.randint(0,1)
                        if zombie_sortmovement == 1:
                            zombies_i[i]=0
                            zombies_states[i] = 'walk_l'
                        zombies_changestate[i]=0
                    elif zombies_states[i] == 'idle_l':
                        zombie_sortmovement=random.randint(0,1)
                        if zombie_sortmovement == 1:
                            zombies_i[i]=0
                            zombies_states[i] = 'walk_r'
                        zombies_changestate[i]=0
   
    #Movimento e animacao dos inimigos 
    
    #Movimento
    for i in range(len(zombies_states)):
        if zombies_states[i] == 'idle_r' or zombies_states[i] == 'idle_l':
            zombies_movement[i] = [0,0]
            zombies_movement[i][1]+=0.2
            if zombies_movement[i][1] > 3:
                zombies_movement[i][1] = 3
            zombies_rects[i]=move(zombies_rects[i],zombies_movement[i],tile_rects)[0]
        elif zombies_states[i] == 'walk_r':
            zombies_movement[i] = [2,0]
            zombies_movement[i][1]+=0.2
            zombies_rects[i]=move(zombies_rects[i],zombies_movement[i],tile_rects)[0]
            if zombies_movement[i][1] > 3:
                zombies_movement[i][1] = 3
        elif zombies_states[i] == 'walk_l':
            zombies_movement[i] = [-2,0]
            zombies_movement[i][1]+=0.2
            zombies_rects[i]=move(zombies_rects[i],zombies_movement[i],tile_rects)[0]
            if zombies_movement[i][1] > 3:
                zombies_movement[i][1]=3
        elif zombies_states[i] in ('dead_r','dead_l'):
            zombies_movement[i] = [0,0]
    #Animacao
    for i in range(len(zombies_states)):
        if zombies_states[i] == 'idle_r':
            if zombies_i[i]<69:
                zombies_i[i]+=1
            else:
                zombies_i[i]=0
            display.blit(zombies_imgs_idle[i][zombies_i[i]//5],(zombies_rects[i].x-scroll[0],zombies_rects[i].y-scroll[1]))
        elif zombies_states[i] == 'idle_l':
            if zombies_i[i]<69:
                zombies_i[i]+=1
            else:
                zombies_i[i]=0
            display.blit(zombies_imgs_idle_flip[i][zombies_i[i]//5],(zombies_rects[i].x-scroll[0],zombies_rects[i].y-scroll[1]))
        elif zombies_states[i] == 'walk_r':
            if zombies_i[i]<49:
                zombies_i[i]+=1
            else:
                zombies_i[i]=0
            display.blit(zombies_imgs_walk[i][zombies_i[i]//5],(zombies_rects[i].x-scroll[0],zombies_rects[i].y-scroll[1]))
        elif zombies_states[i] == 'walk_l':
            if zombies_i[i]<49:
                zombies_i[i]+=1
            else:
                zombies_i[i]=0
            display.blit(zombies_imgs_walk_flip[i][zombies_i[i]//5],(zombies_rects[i].x-scroll[0],zombies_rects[i].y-scroll[1]))
        elif zombies_states[i] == 'dead_r': 
            if zombies_i[i]<48:
                zombies_i[i]+=1
            else:
                zombies_i[i]=48
            display.blit(zombies_imgs_dead[i][zombies_i[i]//4],(zombies_dead_positions[i][0]-scroll[0],zombies_dead_positions[i][1]-scroll[1]))
        elif zombies_states[i] == 'dead_l': 
            if zombies_i[i]<48:
                zombies_i[i]+=1
            else:
                zombies_i[i]=48
            display.blit(zombies_imgs_dead_flip[i][zombies_i[i]//4],(zombies_dead_positions[i][0]-scroll[0],zombies_dead_positions[i][1]-scroll[1]))
        
    #Movimento e animacao do jogador
    
    #Movimento
    player_movement=[0,0]
    if moving_right and not player_reset:
        if player_running:
            player_movement[0]+=4.5
        else:
            player_movement[0]+=3
        if flip_left:
            flip_left=False
            flip_right=True
            throwAnimation=False
    if moving_left and not player_reset:
        if player_running:
            player_movement[0]-=4.5
        else:
            player_movement[0]-=3
        if flip_right:
            flip_right=False
            flip_left=True
            throwAnimation=False
    if not player_reset:
        player_movement[1] += player_y_momentum #gravidade
    player_y_momentum += 0.2
    if player_y_momentum > 3:
        player_y_momentum = 3
    obtainsolidrects()
    player_rect,player_collisions=move(player_rect,player_movement,solid_rects)
    checkcollisionzombies()
    #print(f'player bottom {player_rect.bottom}')
    #print(f'player right {player_rect.right}')
    #print(f'player left {player_rect.left}')
    
    #Caso o jogador caia em algum lugar que nao pode
    for i in range(len(danger_tiles)):
        if player_rect.right > danger_tiles[i][0]+15 and player_rect.left < danger_tiles[i][0] +17 and player_rect.bottom >= danger_tiles[i][1] and player_rect.bottom < danger_tiles[i][1]+35:
            if not player_reset:
                if draw_player:
                    player_reset=True
                    player_running=False
                    draw_player=False
                    player_lives-=1
                    if player_lives == 0:
                        gameover=True
                        pygame.mixer.music.fadeout(200)
                        gameover_sound.play()
    
    #Corrigindo as variaveis de pulo
    if player_collisions['bottom']:
        player_y_momentum = 0
        air_timer = 0
    elif player_collisions['top']:
        player_y_momentum = 0
    else:
        air_timer += 1

    #Animacoes do jogador 
    
    if player_frame_i<=44:
        player_frame_i+=1
    elif player_frame_i == 45:
        if air_timer == 0:
            player_frame_i=0
        else:
            player_frame_i=45
    if draw_player:
        if moving_right:
            if air_timer <= 5:
                if flip_right:
                    display.blit(player_imgs_run[player_frame_i//5],(player_rect.x-scroll[0],player_rect.y-scroll[1]))
            elif air_timer > 5:
                if flip_right:
                    if throwAnimation and kunai_state and kunai_state_i<45:
                        display.blit(player_imgs_jump_throw[player_frame_i//5],(player_rect.x-scroll[0],player_rect.y-scroll[1]))
                    else:
                        display.blit(player_imgs_jump[player_frame_i//5],(player_rect.x-scroll[0],player_rect.y-scroll[1]))
        elif moving_left:
            if air_timer <= 5:
                if flip_left:
                    display.blit(player_imgs_run_flip[player_frame_i//5],(player_rect.x-scroll[0],player_rect.y-scroll[1]))
            elif air_timer > 5:
                if flip_left:
                    if throwAnimation and kunai_state and kunai_state_i <45: 
                        display.blit(player_imgs_jump_throw_flip[player_frame_i//5],(player_rect.x-scroll[0],player_rect.y-scroll[1]))
                    else:
                        display.blit(player_imgs_jump_flip[player_frame_i//5],(player_rect.x-scroll[0],player_rect.y-scroll[1]))
        else:
            if air_timer <= 5:
                if flip_right:
                    if throwAnimation and kunai_state and kunai_state_i< 45:
                        display.blit(player_imgs_throw[player_frame_i//5],(player_rect.x-scroll[0],player_rect.y-scroll[1]))
                    else:
                        display.blit(player_imgs_idle[player_frame_i//5],(player_rect.x-scroll[0],player_rect.y-scroll[1]))
                elif flip_left:
                    if throwAnimation and kunai_state and kunai_state_i< 45:
                        display.blit(player_imgs_throw_flip[player_frame_i//5],(player_rect.x-scroll[0],player_rect.y-scroll[1]))
                    else:
                        display.blit(player_imgs_idle_flip[player_frame_i//5],(player_rect.x-scroll[0],player_rect.y-scroll[1]))
            elif air_timer > 5:
                if flip_right:
                    if throwAnimation and kunai_state and kunai_state_i<45:
                        display.blit(player_imgs_jump_throw[player_frame_i//5],(player_rect.x-scroll[0],player_rect.y-scroll[1]))
                    else:
                        display.blit(player_imgs_jump[player_frame_i//5],(player_rect.x-scroll[0],player_rect.y-scroll[1]))
                elif flip_left:
                    if throwAnimation and kunai_state and kunai_state_i<45:
                        display.blit(player_imgs_jump_throw_flip[player_frame_i//5],(player_rect.x-scroll[0],player_rect.y-scroll[1]))
                    else:
                        display.blit(player_imgs_jump_flip[player_frame_i//5],(player_rect.x-scroll[0],player_rect.y-scroll[1]))
    
    #Movimento do kunai
    
    if kunai_state:
        checkcollisionkunaienemy()
        if kunai_state_i < 60:
            if kunai_right:
                kunai_rect,kunai_collisions=move(kunai_rect,kunai_movement,solid_rects)
                kunai_throw(kunai_rect.x-scroll[0],kunai_rect.y-scroll[1],kunai_img,display)
                if kunai_collisions['left'] or kunai_collisions['right'] or kunai_collisions['bottom']:
                    kunaistab_sound.play()
                    kunai_state_i=0
                    kunai_state=False
                    throwAnimation=False
                    kunai_rect=pygame.Rect(2000,2000,kunai_img.get_width(),kunai_img.get_height())
            elif kunai_left:
                kunai_rect,kunai_collisions=move(kunai_rect,kunai_movement,solid_rects)
                kunai_throw(kunai_rect.x-scroll[0],kunai_rect.y-scroll[1],kunai_img_flip,display)
                if kunai_collisions['left'] or kunai_collisions['right'] or kunai_collisions['bottom']:
                    kunai_state_i=0
                    kunai_state=False
                    throwAnimation=False
                    kunai_rect=pygame.Rect(2000,2000,kunai_img.get_width(),kunai_img.get_height())
            kunai_state_i+=1
        elif kunai_state_i == 60:
            kunai_state_i=0
            kunai_rect=pygame.Rect(2000,2000,kunai_img.get_width(),kunai_img.get_height())
            kunai_state=False
            throwAnimation=False
    
    #Recebe inputs do teclado
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN and not player_reset:
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
            if event.key == K_UP:
                if air_timer < 6:
                    player_y_momentum=-6
                    if throwAnimation:
                        throwAnimation=False
            if event.key == K_v and kunai_state == False and kunai_ammunition > 0:
                throwAnimation=True
                kunai_ammunition-=1
                kunaithrow_sound.play()
                kunai_rect.x=player_rect.right+5
                kunai_rect.y=player_rect.y+18
                if flip_right:
                    kunai_right=True
                    kunai_left=False
                    kunai_movement=[7,0]
                    kunai_throw(kunai_rect.x-scroll[0],kunai_rect.y-scroll[1],kunai_img,display) 
                elif flip_left:
                    kunai_left=True
                    kunai_right=False
                    kunai_movement =[-7,0]
                    kunai_throw(kunai_rect.x-scroll[0],kunai_rect.y-scroll[1],kunai_img_flip,display)
            if event.key == K_w:
                debug=True
            if event.key == K_LSHIFT and not player_running:
                player_running=True

        if event.type == KEYUP and not player_reset:
            if event.key == K_RIGHT:
                player_frame_i=0
                moving_right = False
            if event.key == K_LEFT:
                player_frame_i=0
                moving_left = False   
            if event.key == K_w:
                debug=False
            if event.key == K_LSHIFT and player_running:
                player_running=False

    #Evento de fadeout e HUD
    
    #Fadeout
    if player_reset:
        if FADEOUT and alphaF == 255:
            if not gameover:
                draw_player=True
                player_rect.x=checkpoint_x
                player_rect.y=checkpoint_y
                moving_right=False
                moving_left=False
                player_y_momentum=0
                air_timer=0
                flip_left=False
                flip_right=True
            else:
                blockfade=True
        elif FADEOUT and alphaF == 0:
            FADEOUT=False
            player_reset=False
            fade_event=False
        else:
            fade_event=True
    
    #HUD
    display.blit(hud_head,(0,0))
    display.blit(baby_font_render_lives,(60,20))
    display.blit(hud_kunai,(0,50))
    display.blit(baby_font_render_ammunition,(60,70))
    
    fade_out(blockfade)
    if blockfade and gameover:
        if alphaG < 255:
            alphaG+=1
        gameover_img.set_alpha(alphaG)
        display.blit(gameover_img,(60,100))
    
    #Atualizando a tela de jogo
    
    surface = pygame.transform.smoothscale(display,WINDOW_SIZE) # Aumenta o tamanho da superficie que estamos desenhando o jogo para o tamanho da janela
    screen.blit(surface,(0,0))
    pygame.display.update()
    if debug:
        clock.tick(10)
    else:
        clock.tick(70)
