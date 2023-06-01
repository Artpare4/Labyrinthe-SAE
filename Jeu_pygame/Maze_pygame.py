import random
from random import *

import pygame.sprite


class Maze ():
    """
    Classe Labyrinthe
    Représentation sous forme de graphe non-orienté
    dont chaque sommet est une cellule (un tuple (l,c))
    et dont la structure est représentée par un dictionnaire
      - clés : sommets
      - valeurs : ensemble des sommets voisins accessibles
    """
    def __init__(self, height, width,empty=False):
        """
        Constructeur d'un labyrinthe de height cellules de haut
        et de width cellules de large
        Les voisinages sont initialisés à des ensembles vides
        Remarque : dans le labyrinthe créé, chaque cellule est complètement emmurée
        """
        self.height    = height
        self.width     = width

        self.neighbors = {(i, j): set() for i in range(height) for j in range(width)}

        #if empty==True:
        #    for elmt in self.neighbors:
        #        for i in range(elmt[0]-1,elmt[0]+1):
        #            print("Nouveau i", i)
        #            for j in range(elmt[1]-1,elmt[1]+2):
        #                print("Nouveau j",j)
        #                if i >= 0 and i <= self.height:
        #                    if j>=0 and j<=self.width:
        #                        print(i,j)
        #                        self.neighbors[elmt].add((i,j))

        if empty:
            for i in range(height-1):
                for j in range(width-1):
                    self.neighbors[(i,j)].add((i+1,j))
                    self.neighbors[(i,j)].add((i,j+1))
                    self.neighbors[(i+1, j)].add((i,j))
                    self.neighbors[(i,j+1)].add((i,j))
            for i in range(height-1):
                self.neighbors[(i,width-1)].add((i+1,width-1))
                self.neighbors[(i+1,width - 1)].add((i, width - 1))
            for j in range(width-1):
                self.neighbors[(height-1,j)].add((height-1,j+1))
                self.neighbors[(height-1,j+1)].add((height-1,j))

    def info(self):
        """
        **NE PAS MODIFIER CETTE MÉTHODE**
        Affichage des attributs d'un objet 'Maze' (fonction utile pour deboguer)
        Retour:
            chaîne (string): description textuelle des attributs de l'objet
        """
        txt = "**Informations sur le labyrinthe**\n"
        txt += f"- Dimensions de la grille : {self.height} x {self.width}\n"
        txt += "- Voisinages :\n"
        txt += str(self.neighbors)+"\n"
        valid = True
        for c1 in {(i, j) for i in range(self.height) for j in range(self.width)}:
            for c2 in self.neighbors[c1]:
                if c1 not in self.neighbors[c2]:
                    valid = False
                    break
            else:
                continue
            break
        txt += "- Structure cohérente\n" if valid else f"- Structure incohérente : {c1} X {c2}\n"
        return txt

    def __str__(self):
        """
        **NE PAS MODIFIER CETTE MÉTHODE**
        Représentation textuelle d'un objet Maze (en utilisant des caractères ascii)
        Retour:
             chaîne (str) : chaîne de caractères représentant le labyrinthe
        """
        txt = ""
        # Première ligne
        txt += "┏"
        for j in range(self.width-1):
            txt += "━━━┳"
        txt += "━━━┓\n"
        txt += "┃"
        for j in range(self.width-1):
            txt += "   ┃" if (0,j+1) not in self.neighbors[(0,j)] else "    "
        txt += "   ┃\n"
        # Lignes normales
        for i in range(self.height-1):
            txt += "┣"
            for j in range(self.width-1):
                txt += "━━━╋" if (i+1,j) not in self.neighbors[(i,j)] else "   ╋"
            txt += "━━━┫\n" if (i+1,self.width-1) not in self.neighbors[(i,self.width-1)] else "   ┫\n"
            txt += "┃"
            for j in range(self.width):
                txt += "   ┃" if (i+1,j+1) not in self.neighbors[(i+1,j)] else "    "
            txt += "\n"
        # Bas du tableau
        txt += "┗"
        for i in range(self.width-1):
            txt += "━━━┻"
        txt += "━━━┛\n"

        return txt

    def remove_wall(self, c1: tuple, c2: tuple) -> None:
        """
        Méthode d'instance qui supprime le mur du labyrinthe entre c1 et c2 si existant.
        Ajoute c1 aux voisins de c2 et inversement.
        Paramètre:
            c1 : cellule
            c2 : cellule voisine a c1

        """
        self.neighbors[c1].add(c2)
        self.neighbors[c2].add(c1)
        return None


    def get_cells(self):
        """
        Méthode d'instance qui renvoie l'entiereté des cellules du labyrinthe sous forme de liste
        Retour:
            listeCells (list) : la liste des cellules

        """
        listeCells = []
        for i in range(self.height):
            for j in range(self.width):
                listeCells.append((i, j))
        return listeCells

    def get_walls(self):
        """
        Méthode d'instance qui renvoie les couples de l'entièreté des cellules séparés par des murs en suivant le schéma suivant:
        [(cellule1,cellule2)] signifie qu'un mur se trouve entre les deux.
        Retour:
            listeWalls (list) : la liste des murs sous forme de couple (tuple) de cellule.
        """
        listeWalls = []
        listeCells = self.get_cells()
        for i in range(self.height):
            for j in range(self.width):
                if ((i + 1, j) not in self.neighbors[(i, j)]) and ((i + 1, j) in listeCells):
                    listeWalls.append(((i, j), (i + 1, j)))
                if ((i, j + 1) not in self.neighbors[(i, j)]) and ((i, j + 1) in listeCells):
                    listeWalls.append(((i, j), (i, j + 1)))
        return listeWalls

    def fill(self):
        """
        Méthode d'instance qui remplis le labyrinthe de mur. Supprime toutes les valeurs de self.neighbors.
        """
        listeCells = self.get_cells()
        for cells in listeCells:
            self.neighbors[cells] = set()
        return None

    def get_contiguous_cells(self, c:tuple)->list:
        """
        Méthode d'instance qui renvoie les cellules contigüe à la cellule entrée en paramètre (voisines avec ou sans présence d'un mur)
        Paramètre:
            c (tuple) : cellule ciblée
        Retour:
            res (list) : Liste des cellules contigüe à la cellule ciblée
        """
        res = []
        if c[0] - 1 >= 0:
            res.append((c[0] - 1, c[1]))
        if c[0] + 1 < self.height:
            res.append((c[0] + 1, c[1]))
        if c[1] - 1 >= 0:
            res.append((c[0], c[1] - 1))
        if c[1] + 1 < self.width:
            res.append((c[0], c[1] + 1))
        return res


    def add_wall(self, c1: tuple, c2: tuple):
        """
        Méthode d'instance qui permet d'ajouter un mur entre deux cellules entrées en paramètre (Les rends "non-voisines")
        Paramètre:
            c1 (tuple) : Cellule1
            c2 (tuple) : Cellule2
        """
        # Facultatif : on teste si les sommets sont bien dans le labyrinthe
        assert 0 <= c1[0] < self.height and \
               0 <= c1[1] < self.width and \
               0 <= c2[0] < self.height and \
               0 <= c2[1] < self.width, \
            f"Erreur lors de l'ajout d'un mur entre {c1} et {c2} : les coordonnées de sont pas compatibles avec les dimensions du labyrinthe"
        # Ajout du mur
        if c2 in self.neighbors[c1]:  # Si c2 est dans les voisines de c1
            self.neighbors[c1].remove(c2)  # on le retire
        if c1 in self.neighbors[c2]:  # Si c3 est dans les voisines de c2
            self.neighbors[c2].remove(c1)  # on le retire

    def get_reachable_cells(self, c: tuple) -> list:
        """
        Méthode d'instance qui renvoie les cellules voisines de la cellule entrée en paramètre si aucun mur ne se trouve entre-elles.
        Paramètre:
            c (tuple) : Cellule ciblée
        Retour:
            res (list) : Liste des cellules voisines de la cellule ciblée
        """
        res = []
        walls = self.get_walls()
        if c[0] - 1 >= 0 and ((c[0] - 1, c[1]), c) not in walls:
            res.append((c[0] - 1, c[1]))
        if c[0] + 1 < self.height and (c, (c[0] + 1, c[1])) not in walls:
            res.append((c[0] + 1, c[1]))
        if c[1] - 1 >= 0 and ((c[0], c[1] - 1), c) not in walls:
            res.append((c[0], c[1] - 1))
        if c[1] + 1 < self.width and (c, (c[0], c[1] + 1)) not in walls:
            res.append((c[0], c[1] + 1))
        return res

    def empty(self):
        """
        Méthode d'instance qui supprime tous les murs d'un labyrinthe.
        """
        for i in range(self.height - 1):
            for j in range(self.width - 1):
                self.neighbors[(i, j)].add((i + 1, j))
                self.neighbors[(i, j)].add((i, j + 1))
                self.neighbors[(i + 1, j)].add((i, j))
                self.neighbors[(i, j + 1)].add((i, j))
        for i in range(self.height - 1):
            self.neighbors[(i, self.width - 1)].add((i + 1, self.width - 1))
            self.neighbors[(i + 1, self.width - 1)].add((i, self.width - 1))
        for j in range(self.width - 1):
            self.neighbors[(self.height - 1, j)].add((self.height - 1, j + 1))
            self.neighbors[(self.height - 1, j + 1)].add((self.height - 1, j))

    @classmethod
    def gen_btree(cls, h: int, w: int):
        """
        Méthode de classe. Permet de générer un labyrinthe en suivant l'algorithme de construction par arbre binaire.
        Paramètre:
            h (int) : Hauteur du labyrinthe
            w (int) : Largeur du labyrinthe
        Retour:
            laby (Maze) : Un labyrinthe généré par l'algorithme
        """
        laby=Maze(h,w,False)
        for i in range(h):
            for j in range(w):
                if i==3 and (i,j)!=(3,3):
                    laby.remove_wall((i,j),(i,j+1))
                elif j==3 and (i,j)!=(3,3):
                    laby.remove_wall((i, j), ((i + 1, j)))
                else:
                    if ((i,j),(i+1,j)) not in laby.neighbors and (i,j)!=(3,3):
                        if ((i, j), (i, j + 1)) not in laby.neighbors and(i,j)!=(3,3):
                            suppr_mur=randint(0,1)
                            if suppr_mur==1: ## si c'est égale à 1 on supprime le mur Sud
                             laby.remove_wall((i,j),((i+1,j)))

                            elif suppr_mur==0: ## si c'est égale à 1 on supprime le mur Est
                                laby.remove_wall((i,j),(i,j+1))

                        else:
                            laby.remove_wall((i, j), (i + 1, j))
                    else:
                        if ((i, j), (i, j + 1)) not in laby.neighbors and(i,j)!=(3,3):
                            laby.remove_wall((i, j), (i, j + 1))
        return laby

    @classmethod
    def gen_fusion(cls, h: int, w: int):
        """
        Méthode de classe. Permet de générer un labyrinthe en suivant l'algorithme de construction par fusion.
        Paramètre:
            h (int) : Hauteur du labyrinthe
            w (int) : Largeur du labyrinthe
        Retour:
            laby (Maze) : Un labyrinthe généré par l'algorithme
        """
        laby=Maze(h,w,False)
        label={}
        walls=laby.get_walls()
        shuffle(walls)
        valLabel = 0
        for i in range(h):
            for j in range(w):
                    label.update({(i,j):valLabel})
                    valLabel+=1
        for murs in walls:
            if label[murs[0]]!=label[murs[1]]:
                laby.remove_wall(murs[0],murs[1])
                val=label[murs[1]] #valeur du label que l'on veut remplacer
                for i in range(h):
                    for j in range(w):
                        if (label[(i,j)]==val):
                            label[(i,j)]=label[murs[0]]

        return laby


    @classmethod
    def gen_sidewinder(cls, h: int, w: int):
        """
        Méthode de classe. Permet de générer un labyrinthe en suivant l'algorithme de construction Sidewinder.
        Paramètre:
            h (int) : Hauteur du labyrinthe
            w (int) : Largeur du labyrinthe
        Retour:
            laby (Maze) : Un labyrinthe généré par l'algorithme
        """
        laby = Maze(h,w,False)
        for i in range(0,h-1):
            seq = []
            for j in range(0, w-1):
                seq.append((i,j))
                PoF = randint(0,1)
                if PoF == 0:
                    laby.remove_wall((i,j),(i,j+1))
                else:
                    celluleChoisie = randint(0,len(seq)-1)
                    laby.remove_wall(seq[celluleChoisie],(i+1,seq[celluleChoisie][1]))
                    seq = []
            seq.append((i,w))
            celluleChoisie = randint(0,len(seq)-1)
            laby.remove_wall(seq[celluleChoisie],(seq[celluleChoisie][0]+1,seq[celluleChoisie][1]))
        for i in range(0,w-1):
            laby.remove_wall((h-1,i),(h-1,i+1))
        return laby


    @classmethod
    def gen_exploration(cls, h: int, w: int):
        """
        Méthode de classe. Permet de générer un labyrinthe en suivant l'algorithme de construction par exploration.
        Paramètre:
            h (int) : Hauteur du labyrinthe
            w (int) : Largeur du labyrinthe
        Retour:
            laby (Maze) : Un labyrinthe généré par l'algorithme
        """
        laby = Maze(h,w,False)
        cellulesAll = laby.get_cells()
        visited = dict((elt,False) for elt in cellulesAll)
        celluleRandom = cellulesAll[randint(0,len(cellulesAll)-1)]
        pile = [celluleRandom]
        visited[celluleRandom] = True
        while len(pile)>0:
            cell = pile.pop()
            voisins = [elt for elt in laby.get_contiguous_cells(cell) if not visited[elt]]
            if len(voisins)>0:
                pile.append(cell)
                randomVoisin = voisins[randint(0,len(voisins)-1)]
                laby.remove_wall(cell,randomVoisin)
                visited[randomVoisin] = True
                pile.append(randomVoisin)
        return laby


    @classmethod
    def gen_wilson(cls, h: int, w: int):
        """
        Méthode de classe. Permet de générer un labyrinthe en suivant l'algorithme de construction par l'agorithme de Wilson.
        Paramètre:
            h (int) : Hauteur du labyrinthe
            w (int) : Largeur du labyrinthe
        Retour:
            laby (Maze) : Un labyrinthe généré par l'algorithme
        """
        laby=Maze(h,w,False)
        cellules=laby.get_cells()
        marque={} ## toutes les cellules  sont initialisé à None (non marqué)
        for cell in cellules:
            marque.update({cell: None})

        cellules_non_marqué = [elmt for elmt in marque if marque[elmt] == None]  ## toutes les cellules non marqué (utiliser pour savoir leurs nombres restants)
        ## première cellules marqué aléatoire
        première_cellule_marqué = choice(cellules_non_marqué) ## première cellule marqué de la grille
        marque[première_cellule_marqué] = True


        cellules_non_marqué = [elmt for elmt in marque if marque[elmt] == None]
        while len(cellules_non_marqué)!=0:


            parcours=[] ## parcours actuelle


            if len(cellules_non_marqué)==1:
                cellule_parcours=cellules_non_marqué[0]
            else:
            #initialisation de la première cellule du parcours
                cellule_parcours=choice(cellules_non_marqué)
            parcours.append(cellule_parcours)

            test_parcours=True


            while test_parcours==True:  ## tant que on parcours

                    cellule_suivantes_possibles=[cell for cell in laby.get_contiguous_cells(cellule_parcours)]
                    cellule_parcours=choice(cellule_suivantes_possibles)


                    if marque[cellule_parcours]==True:
                        parcours.append(cellule_parcours)
                        test_parcours=False
                    elif cellule_parcours in parcours:
                        if cellule_parcours==parcours[len(parcours)-2]:
                            del parcours[len(parcours)-1]

                        else:
                            del parcours[parcours.index(cellule_parcours)+1:len(parcours)]

                    else:
                        parcours.append(cellule_parcours)


            for cell in parcours:
                marque[cell] = True

            for i in range(len(parcours)-1):
                laby.remove_wall(parcours[i],parcours[i+1])

            cellules_non_marqué = [elmt for elmt in marque if marque[elmt] == None]
        return laby

    def overlay(self, content=None):
        """
        Rendu en mode texte, sur la sortie standard, \
        d'un labyrinthe avec du contenu dans les cellules
        Argument:
            content (dict) : dictionnaire tq content[cell] contient le caractère à afficher au milieu de la cellule
        Retour:
            string
        """
        if content is None:
            content = {(i, j): ' ' for i in range(self.height) for j in range(self.width)}
        else:
            # Python >=3.9
            # content = content | {(i, j): ' ' for i in range(
            #    self.height) for j in range(self.width) if (i,j) not in content}
            # Python <3.9
            new_content = {(i, j): ' ' for i in range(self.height) for j in range(self.width) if (i, j) not in content}
            content = {**content, **new_content}
        txt = r""
        # Première ligne
        txt += "┏"
        for j in range(self.width - 1):
            txt += "━━━┳"
        txt += "━━━┓\n"
        txt += "┃"
        for j in range(self.width - 1):
            txt += " " + content[(0, j)] + " ┃" if (0, j + 1) not in self.neighbors[(0, j)] else " " + content[
                (0, j)] + "  "
        txt += " " + content[(0, self.width - 1)] + " ┃\n"
        # Lignes normales
        for i in range(self.height - 1):
            txt += "┣"
            for j in range(self.width - 1):
                txt += "━━━╋" if (i + 1, j) not in self.neighbors[(i, j)] else "   ╋"
            txt += "━━━┫\n" if (i + 1, self.width - 1) not in self.neighbors[(i, self.width - 1)] else "   ┫\n"
            txt += "┃"
            for j in range(self.width):
                txt += " " + content[(i + 1, j)] + " ┃" if (i + 1, j + 1) not in self.neighbors[(i + 1, j)] else " " + \
                                                                                                                 content[
                                                                                                                     (
                                                                                                                     i + 1,
                                                                                                                     j)] + "  "
            txt += "\n"
        # Bas du tableau
        txt += "┗"
        for i in range(self.width - 1):
            txt += "━━━┻"
        txt += "━━━┛\n"
        return txt


    def solve_dfs(self, start: tuple, stop: tuple) -> list:
        """
        Méthode d'instance de classe. Trouve le chemin le plus cours entre deux cellules grâce à un algorithme
        de résolution d'arbre binaire en longueur.
        Paramètre:
            start (tuple) : Cellule de départ
            stop (tuple) : Cellule de sortie
        Retour:
            chemin (list) : Chemin le plus court pour arriver à la sortie.
        """
        attente = [start]
        pred = {start:start}
        marquage = {cellules:False for cellules in self.get_cells()}
        marquage[start] = True
        end = False
        while False in marquage.values() and not end:
            c = attente.pop()
            if c == stop:
                end = True
            else:
                for voisins in self.get_reachable_cells(c):
                    if not marquage[voisins]:
                        marquage[voisins] = True
                        attente.append(voisins)
                        pred[voisins] = c
        chemin = []
        c = stop
        while c != start:
            chemin.append(c)
            c = pred[c]
        chemin.append(start)
        chemin.reverse()
        return chemin

    def solve_bfs(self, start: tuple, stop: tuple) -> list:
        """
        Méthode d'instance de classe. Trouve le chemin le plus cours entre deux cellules grâce à un algorithme
        de résolution d'arbre binaire en largeur.
        Paramètre:
            start (tuple) : Cellule de départ
            stop (tuple) : Cellule de sortie
        Retour:
            chemin (list) : Chemin le plus court pour arriver à la sortie.
        """
        attente = [start]
        pred = {start:start}
        marquage = {cellules:False for cellules in self.get_cells()}
        marquage[start] = True
        end = False
        while False in marquage.values() and not end:
            c = attente.pop(0)
            if c == stop:
                end = True
            else:
                for voisins in self.get_reachable_cells(c):
                    if not marquage[voisins]:
                        marquage[voisins] = True
                        attente.append(voisins)
                        pred[voisins] = c
        chemin = []
        c = stop
        while c != start:
            chemin.append(c)
            c = pred[c]
        chemin.append(start)
        chemin.reverse()
        return chemin


    def solve_rhr(self, start: tuple, stop: tuple) -> list:
        """
        Méthode d'instance de classe. Trouve un chemin de résolution du labyrinthe à l'aide de la technique de la main
        droite. Colle le mur de droite jusqu'à la sortie.
        Paramètre:
            start (tuple) : Cellule de départ
            stop (tuple) : Cellule de sortie
        Retour:
            chemin (list) : Chemin le plus court pour arriver à la sortie.
        """


        parcours=[]
        parcours.append(start)
        cellule_parcours=start
        vision =0  ## 0=:On regarde en haut 1= On regarde en bas 2=On regarde à gauche 3=On regarde à droite
        wall=self.get_walls()
        cellules=self.get_cells()
        print(wall)
        i=0
        while cellule_parcours!=stop:
            print(parcours)
            if  vision == 0: ## vision en bas
                if (((cellule_parcours[0],cellule_parcours[1]-1),cellule_parcours) not in wall)   and   (cellule_parcours[0],cellule_parcours[1]-1) in cellules: ## si pas de mur à gauche
                        print(1)
                        cellule_parcours=(cellule_parcours[0],cellule_parcours[1]-1)
                        parcours.append(cellule_parcours)
                        vision=2

                else:
                    if ((cellule_parcours,(cellule_parcours[0]+1,cellule_parcours[1])) not in wall) and   (cellule_parcours[0]+1,cellule_parcours[1]) in cellules :## si pas de mur en sud (en face)
                        print(2)
                        cellule_parcours=(cellule_parcours[0]+1,cellule_parcours[1])
                        parcours.append(cellule_parcours)
                        vision=0

                    else: ## présence de murs en face + gauche
                        if ((cellule_parcours,(cellule_parcours[0],cellule_parcours[1]+1)) not in wall)   and   (cellule_parcours[0],cellule_parcours[1]+1) in cellules:
                            print(3)
                            cellule_parcours=(cellule_parcours[0],cellule_parcours[1]+1)
                            parcours.append(cellule_parcours)
                            vision=3
                        else:
                            vision=1

            elif vision==1:
                if ((cellule_parcours,(cellule_parcours[0],cellule_parcours[1]+1)) not in wall)   and   (cellule_parcours[0],cellule_parcours[1]+1) in cellules: ## si pas de mur à droite
                    print(4)
                    cellule_parcours=(cellule_parcours[0], cellule_parcours[1] + 1)
                    parcours.append(cellule_parcours)
                    vision=3
                else:
                    if (((cellule_parcours[0]-1,cellule_parcours[1]),cellule_parcours) not in wall)   and   (cellule_parcours[0]-1,cellule_parcours[1]) in cellules : ## si pas de mur au nord
                        print(5)
                        cellule_parcours=(cellule_parcours[0]-1,cellule_parcours[1])
                        parcours.append(cellule_parcours)
                        vision=1
                    else : ## présence d'un mur au nord et à droite
                        if (((cellule_parcours[0],cellule_parcours[1]-1),cellule_parcours) not in wall)   and   (cellule_parcours[0],cellule_parcours[1]-1) in cellules : ## si il y a pas de  mur à gauche
                            print(6)
                            cellule_parcours=(cellule_parcours[0],cellule_parcours[1]-1)
                            parcours.append(cellule_parcours)
                            vision=2
                        else:
                            vision=0

            elif vision==2:
                if (((cellule_parcours[0]-1,cellule_parcours[1]),cellule_parcours) not in wall)   and   (cellule_parcours[0]-1,cellule_parcours[1]) in cellules: ## pas de mur au nord
                    print(7)
                    cellule_parcours= (cellule_parcours[0]-1,cellule_parcours[1])
                    parcours.append(cellule_parcours)
                    vision=1
                else:
                    if (((cellule_parcours[0],cellule_parcours[1]-1),cellule_parcours) not in wall)   and   (cellule_parcours[0],cellule_parcours[1]-1) in cellules : ## pas de mur vers la gauche (en face)
                        print(8)
                        cellule_parcours=(cellule_parcours[0],cellule_parcours[1]-1)
                        parcours.append(cellule_parcours)
                        vision=2
                    else:
                        if ((cellule_parcours,(cellule_parcours[0]+1,cellule_parcours[1]) )not in wall) and   (cellule_parcours[0]+1,cellule_parcours[1]) in cellules : ## pas de mur au sud
                            print(9)
                            cellule_parcours=(cellule_parcours[0]+1,cellule_parcours[1])
                            parcours.append(cellule_parcours)
                            vision=0
                        else:
                            vision=3

            elif vision==3:
                if ((cellule_parcours,(cellule_parcours[0]+1,cellule_parcours[1]) )not in wall) and   (cellule_parcours[0]+1,cellule_parcours[1]) in cellules : ## pas de mur au sud
                    print(10)
                    cellule_parcours=(cellule_parcours[0]+1,cellule_parcours[1])
                    parcours.append(cellule_parcours)
                    vision=0
                else:
                    if ((cellule_parcours,(cellule_parcours[0],cellule_parcours[1]+1)) not in wall)   and   (cellule_parcours[0],cellule_parcours[1]+1) in cellules: ## si pas de mur à droite
                        print(11)
                        cellule_parcours= (cellule_parcours[0],cellule_parcours[1]+1)
                        parcours.append(cellule_parcours)
                        vision=3
                    else:
                        if (((cellule_parcours[0]-1,cellule_parcours[1]),cellule_parcours) not in wall)   and   (cellule_parcours[0]-1,cellule_parcours[1]) in cellules: ## pas de mur au nord
                            print(12)
                            cellule_parcours=(cellule_parcours[0]-1,cellule_parcours[1])
                            parcours.append(cellule_parcours)
                            vision=1
                        else:
                            vision=2
            i+=1
        return parcours

    def distance_geo(self, c1: tuple, c2: tuple) -> int:
        """
        Méthode d'instance. Calcul la distance géodésique entre deux cellules
        Paramètre:
            c1 (tuple) : Cellule de départ
            c2 (tuple) : Cellule d'arrivé
        Retour:
            len (int) : La distance sans compter l'arrivé et le départ
        """
        return len(self.solve_bfs(c1, c2)) - 2

    def distance_man(self, c1: tuple, c2: tuple) -> int:
        """
        Méthode d'instance. Calcul la distance de Manhattan entre deux cellules
        Paramètre:
            c1 (tuple) : Cellule de départ
            c2 (tuple) : Cellule d'arrivé
        Retour:
            len (int) : La distance sans compter l'arrivé et le départ
        """
        return abs(c1[0]-c2[0]) + abs(c1[1]-c2[1])