import pygame as pg
import random
import sys
from pygame.math import Vector2 as vector



class Cobra:
    def __init__(self):
        self.add=False
        self.ponto=any
        
        self.corpo=[vector(13,20),vector(15,20),vector(12,20)]
        self.direcao=vector(1,0)
        
        
    def desenhar(self):
        primeiro=True      
        for forma in self.corpo:
            forma=pg.Rect(forma.x*size,forma.y*size,size,size)
            
            pg.draw.rect(view,(0,0,0),forma)
            if(primeiro):
                self.ponto=forma
                primeiro=False

                
    def movimentacao(self):
        if self.add:
            corpo=self.corpo[:]
            corpo.insert(0,corpo[0]+self.direcao)
            self.corpo=corpo[:]
            self.add=False


        else:    
            corpo=self.corpo[:-1]
            corpo.insert(0,corpo[0]+self.direcao)
            self.corpo=corpo[:]
        

rs=[]
def bordas():
    r1=pg.Rect(0,0,10,grid*size)
    pg.draw.rect(view,(0,0,0),r1)
    r2=pg.Rect(0,0,grid*size,10)
    pg.draw.rect(view,(0,0,0),r2)
    r3=pg.Rect(0,(grid-1)*size,grid*size,10)
    pg.draw.rect(view,(0,0,0),r3)
    r4=pg.Rect((grid-1)*size,0,10,grid*size)
    pg.draw.rect(view,(0,0,0),r4)
    rs.append(r1)
    rs.append(r2)
    rs.append(r3)
    rs.append(r4)
rl=[]
def linhas():
    r1=pg.Rect(50,50,100,10)
    pg.draw.rect(view,(0,0,0),r1)
    r2=pg.Rect(150,150,100,10)
    pg.draw.rect(view,(0,0,0),r2)
    r3=pg.Rect(250,250,100,10)
    pg.draw.rect(view,(0,0,0),r3)
    
    rl.append(r1)
    rl.append(r2)
    rl.append(r3)
        
    
imac=pg.image.load("cob.png")
class Cob(pg.sprite.Sprite):

    def __init__(self):

         pg.sprite.Sprite.__init__(self)
         self.sprites=[]
         self.index=0
         
         for i in range(10):
             
             self.sprites.append(imac.subsurface((i*64,0),(64,64)))

         self.image=self.sprites[0]
         self.rect=self.image.get_rect()
         self.rect.center=(200,100)

    def update(self):

        
        if self.index>9:
            self.index=0
        self.image=self.sprites[int(self.index)]
        self.index+=0.25 

imagem=pg.image.load("coin_gold.png")
class Moeda(pg.sprite.Sprite):

    def __init__(self):

         pg.sprite.Sprite.__init__(self)
         self.sprites=[]
         self.index=0
         self.x=random.randint(3,grid-3)
         self.y=random.randint(3,grid-3)
         self.posicao=vector(self.x,self.y) 
         for i in range(8):
             
             self.sprites.append(imagem.subsurface((i*32,0),(32,32)))

         self.image=self.sprites[5]
         self.rect=self.image.get_rect()
         self.rect.center=(self.posicao.x*size,self.posicao.y*size)

    def update(self):

        
        if self.index>7:
            self.index=0
        self.image=self.sprites[int(self.index)]
        self.index+=0.25


       
            
pg.init()

grid=40
size=10
view_size=(grid*size,grid*size)
view=pg.display.set_mode(view_size)
pg.display.set_caption("meu jogo")
clock=pg.time.Clock()



c=Cobra()
#add evento para movimentação
MOVI_C=pg.USEREVENT
pg.time.set_timer(MOVI_C,200)

#texto do contador
font = pg.font.SysFont("monospace", 15)
font2 = pg.font.SysFont("monospace", 20)
pontos=0
texto= font.render(f"PONTO:{pontos}", 1, (0,0,0))

infor1= font2.render(f"comandos ->,<-,|+^,|+v", 1, (255,0,0))
infor2= font2.render(f"enter para o inicio", 1, (255,0,0))
infor3= font2.render(f"zero=0 atlho", 1, (255,0,0))
#musica

#pg.mixer.init()
#pg.mixer.music.load("bit.ogg")
#pg.mixer.music.play(-1)
#pg.event.wait()

  
grupo=pg.sprite.Group()
m=Moeda()
grupo.add(m)

grupo2=pg.sprite.Group()
cob=Cob()
grupo2.add(cob)
fase1=False
fase2=False
while True :
    view.fill([255,255,255])
    bordas()
    
        
    for event in pg.event.get():
        if event.type==pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type==MOVI_C:
            if  fase1:
                c.movimentacao()
        if event.type==pg.KEYDOWN:
            if event.key==pg.K_UP:
                c.direcao=vector(0,-1)
            if event.key==pg.K_LEFT:
                c.direcao=vector(-1,0)
            if event.key==pg.K_RIGHT:
                c.direcao=vector(1,0)    
            if event.key==pg.K_DOWN:
                c.direcao=vector(0,1)
            if event.key==pg.K_RETURN:
                
                fase1=True
            if event.key==pg.K_0:
                pontos=3
                
                

    if  fase1:
        c.desenhar()
        #colisao com o corpo
        for parte in c.corpo[1:]:
            if c.corpo[0]== parte:
               pg.quit()
               sys.exit()
        if fase2:
           c.corpo=[vector(13,20),vector(15,20),vector(12,20)]
           c.direcao=vector(0,1)
           fase2=False
        if pontos>=3:
            linhas()
            #colisao com as linhas
            if c.ponto.collidelistall(rl):
                pg.quit()
                sys.exit()        
        #colisao com a moeda
        if c.ponto.colliderect(m):
            pontos+=1
            c.add=True
            if pontos==3:
                fase2=True
            texto= font.render(f"PONTO:{pontos}", 1, (0,0,0))
            m.rect.x=random.randint(3,grid-3)*size
            m.rect.y=random.randint(3,grid-3)*size
        #colisao com as bordas
        if c.ponto.collidelistall(rs):
            pg.quit()
            sys.exit()

    
        grupo.draw(view)
        grupo.update()
        grupo2.draw(view)
        grupo2.update()

   
    view.blit(texto, (10, 10))
    if fase1 :
        grupo2.remove(cob)
    if(fase1==False):
        grupo2.draw(view)
        grupo2.update()
        if fase1 :
            grupo2.clear(view,cob)
        view.blit(infor1, (10, 110))
        view.blit(infor2, (10, 140))
        view.blit(infor3, (10, 170))
    clock.tick(60)
    pg.display.flip()
    


