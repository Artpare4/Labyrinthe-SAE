import pygame
import Maze_pygame
import pygame.freetype
class game:
    def __init__(self,largeur,hauteur):
        ##écran du jeu
        self.taille=(800,600)
        self.surf=pygame.display.set_mode(self.taille)
        self.run=True
        ## dimention du labyrinthe
        if largeur!=hauteur :
            self.largeur=largeur
            self.hauteur=largeur
        elif largeur>9:
            self.largeur = 9
            self.hauteur = 9
        else:
            self.largeur=largeur
            self.hauteur=hauteur
        ##création du labyrinthe
        self.laby=Maze_pygame.Maze.gen_wilson(self.largeur,self.hauteur)
        self.wall=pygame.transform.scale(pygame.image.load("Jeu_pygame/wall.png"),(30,30))

        self.all_walls=self.laby.get_walls()
        self.all_cell=self.laby.get_cells()
        self.create_laby=0 ## initialisation du labyrinthe

        ##création du rectangle de fin
        self.x_fin=(self.hauteur*2*30)-30
        self.y_fin=(self.largeur*2*30)-30
        self.rect_fin = pygame.Rect(((self.x_fin,self.y_fin), (30, 30))) ## rectangle
        self.color_fin = (255, 255,255) ## couleur de rectangle

        ##création du recangle du joueur
        self.position_x_joueur=30
        self.position_y_joueur=30
        self.color_joueur=(255,0,0)
        self.rect_joueur=pygame.Rect((self.position_x_joueur,self.position_y_joueur), (30, 30)) ## rectangle

        ## message de fin
        self.font = pygame.freetype.Font("Jeu_pygame/Roboto-Black.ttf", 36)
        self.txtsurf1 = "Vous avez gagné "
        self.txtsurf2="Relancez le jeu pour rejouer"
    def afficher_bordure(self):
        """
        Méthode qui créer les murs du contour du labyrinthe.
        :return: None
        """
        x1=0
        x2=(self.largeur*2*30)
        y1=0
        y2=(self.hauteur*2*30)

        for i in range((self.hauteur*2)+1):
            self.surf.blit(self.wall,(x1,y1))
            x1+=30
        x1=0
        for i in range((self.hauteur*2)+1):
            self.surf.blit(self.wall,(x1,y1))
            self.surf.blit(self.wall,(x2,y1))
            y1+=30

        for i in range((self.hauteur*2)+1):
            self.surf.blit(self.wall,(x1,y2))
            x1+=30

    def remplir_laby(self):
        """
        Méthode qui ajoute les murs intérieurs du labyrinthe
        :return:
        """
        walls=[((1,2),(1,3))]
        all_walls=self.all_walls
        for wall in all_walls:
            if wall[0][1]<wall[1][1] and wall[0][0]==wall[1][0]: ## horizontale
                if wall[1][0]==0:
                    xwall=((wall[1][1]*2)*30)
                    ywall=30
                    self.surf.blit(self.wall,(xwall,ywall))

                else: ## validé
                    xwall = ((wall[1][1]*2)*30)
                    ywall = (((wall[1][0] * 2)+1) * 30)
                    self.surf.blit(self.wall, (xwall, ywall))


            elif wall[0][0]<wall[1][0] and wall[0][1]==wall[1][1]: ##vertical
                if wall[1][1]==0:
                    xwall = 30
                    ywall = ((wall[1][0] * 2) * 30)
                    self.surf.blit(self.wall, (xwall, ywall))

                else:
                    xwall = (((wall[1][1] * 2)+1) * 30)

                    ywall = ((wall[1][0] * 2) * 30)
                    self.surf.blit(self.wall, (xwall, ywall))
    def remplir_angles(self):
        """
        Méthode qui affiche les angles centraux du labyrinthe (exemple dans un carré de 6*6 , cela va afficher le carré du centre)
        :return:
        """
        for i in range(self.largeur):
            for j in range(self.hauteur):
                self.surf.blit(self.wall,(60*i,60*j))

    def ajouter_rectangle_fin(self):
        """
        Méthode qui dessine et positionne le rectangle indiquant la fin
        :return:
        """
        pygame.draw.rect(self.surf,self.color_fin,self.rect_fin)

    def afficher_joueur(self):
        """
        Méthode qui permet l'affichage du joueur
        :return:
        """
        pygame.draw.rect(self.surf,self.color_joueur,self.rect_joueur)
    def convertion_wall_pixel(self):
        """
        Méthode qui convertis les indices les coordonnées des murs en pixel.
        :return:
        """
        res=[]
        all_walls = self.all_walls
        for wall in all_walls:
            if wall[0][1] < wall[1][1] and wall[0][0] == wall[1][0]:  ## horizontale
                if wall[1][0] == 0:
                    xwall = ((wall[1][1] * 2) * 30)
                    ywall = 30
                    res.append(((xwall-30,ywall),(xwall+30,ywall)))
                else:  ## validé
                    xwall = ((wall[1][1] * 2) * 30)
                    ywall = (((wall[1][0] * 2) + 1) * 30)
                    res.append(((xwall-30,ywall),(xwall+30,ywall)))


            elif wall[0][0] < wall[1][0] and wall[0][1] == wall[1][1]:  ##vertical
                if wall[1][1] == 0:
                    xwall = 30
                    ywall = ((wall[1][0] * 2) * 30)
                    res.append(((xwall,ywall-30),(xwall,ywall+30)))

                else:
                    xwall = (((wall[1][1] * 2) + 1) * 30)

                    ywall = ((wall[1][0] * 2) * 30)
                    res.append(((xwall,ywall-30),(xwall,ywall+30)))

        for i in range(1,self.largeur+1):
           for j in range(1,self.hauteur+1):
                res.append((((60*i)-30,60*j),((60*i)+30,60*j)))
                res.append((((60 * i), (60 * j)- 30), ((60 * i), (60 * j)+30)))
        return res
    def mouvement_haut(self):
        """
        Méthode qui permet de déplacer vers le haut le personnage if il n'y a pas de mur.
        :return:
        """
        wall=self.convertion_wall_pixel()
        if ((self.position_x_joueur , self.position_y_joueur-60),(self.position_x_joueur,self.position_y_joueur))  not in wall :
            if (self.position_y_joueur-30)>=30:
                self.position_y_joueur=self.position_y_joueur-30
                self.rect_joueur=pygame.Rect((self.position_x_joueur,self.position_y_joueur), (30, 30))
                pygame.draw.rect(self.surf, self.color_joueur, self.rect_joueur)
    def mouvement_bas(self):
        """
        Méthode qui permet de déplacer vers le bas le personnage if il n'y a pas de mur.
        :return:
        """
        wall=self.convertion_wall_pixel()
        if ((self.position_x_joueur,self.position_y_joueur),(self.position_x_joueur , self.position_y_joueur+60)) not in wall:
            if (self.position_y_joueur+30)<((self.hauteur*2)*30):
                self.position_y_joueur = self.position_y_joueur + 30
                self.rect_joueur = pygame.Rect((self.position_x_joueur, self.position_y_joueur), (30, 30))
                pygame.draw.rect(self.surf, self.color_joueur, self.rect_joueur)

    def mouvement_gauche(self):
        """
        Méthode qui permet de déplacer vers la gauche le personnage if il n'y a pas de mur.
        :return:
        """
        wall=self.convertion_wall_pixel()
        if ((self.position_x_joueur-60, self.position_y_joueur),(self.position_x_joueur,self.position_y_joueur)) not in wall:
            if (self.position_x_joueur-30)>=30:
                self.position_x_joueur = self.position_x_joueur - 30
                self.rect_joueur = pygame.Rect((self.position_x_joueur, self.position_y_joueur), (30, 30))
                pygame.draw.rect(self.surf, self.color_joueur, self.rect_joueur)

    def mouvement_droite(self):
        """
        Méthode qui permet de déplacer vers la droite le personnage if il n'y a pas de mur.
        :return:
        """
        wall=self.convertion_wall_pixel()
        if((self.position_x_joueur,self.position_y_joueur),(self.position_x_joueur +60, self.position_y_joueur)) not in wall :
            if (self.position_x_joueur + 30)<((self.largeur*2)*30):
                self.position_x_joueur = self.position_x_joueur + 30
                self.rect_joueur = pygame.Rect((self.position_x_joueur, self.position_y_joueur), (30, 30))
                pygame.draw.rect(self.surf, self.color_joueur, self.rect_joueur)

    def fin_jeu(self):
        """
        Méthode qui permet de définir la fin du jeu.
        :return:
        """
        res=True
        if self.position_x_joueur==self.x_fin:
            if self.position_y_joueur==self.y_fin:
                res=False
        return res
    def Main(self):
        """
        Méthode qui permet de jouer au jeu.
        :return:
        """
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_z:
                        self.mouvement_haut()
                        self.surf.fill((0, 0, 0))
                        self.create_laby = 0
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.mouvement_bas()
                        self.surf.fill((0, 0, 0))
                        self.create_laby = 0
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_q:
                        self.mouvement_gauche()
                        self.surf.fill((0, 0, 0))
                        self.create_laby = 0
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.mouvement_droite()
                        self.surf.fill((0, 0, 0))
                        self.create_laby=0

            if self.create_laby==0: ## affichage du labyrinthe
                self.afficher_bordure()
                self.remplir_laby()
                self.remplir_angles()
                self.ajouter_rectangle_fin()
                self.afficher_joueur()
                self.create_laby=1


            if self.fin_jeu()==False:
                self.surf.fill((0, 0, 0))
                ##self.surf.blit(self.txtsurf,(400,600))
                self.font.render_to(self.surf,(250,300),self.txtsurf1,self.color_fin)
                self.font.render_to(self.surf, (200, 350), self.txtsurf2, self.color_fin)
                pygame.display.update()
            pygame.display.flip()

## lancement du jeu
pygame.font.init()
pygame.init()
jeu=game(4,4)
jeu.Main()
pygame.quit()