grille_9x9 = [
    [0, 0, 0,  0, 0, 1,  3, 0, 0],
    [7, 6, 0,  4, 0, 0,  1, 0, 0],
    [0, 0, 5,  0, 7, 0,  0, 6, 0],

    [6, 0, 0,  0, 0, 0,  0, 3, 0],
    [0, 0, 0,  0, 0, 7,  0, 4, 9],
    [5, 0, 0,  0, 1, 0,  0, 0, 0],

    [0, 0, 0,  0, 3, 2,  0, 0, 0],
    [0, 9, 0,  0, 0, 0,  0, 0, 0],
    [0, 8, 4,  0, 0, 0,  0, 0, 8]
]
color_red = "\033[91m"
color_end = "\033[0m"

grille_4x4 = [
    [1, 0, 0, 4],
    [0, 0, 0, 0],
    [0, 0, 0, 1],
    [3, 0, 0, 2]
]


class list_solutions:
    def __init__(self, taille):
        self.possibilites = list(range(1, taille + 1, 1))
    
    def contains(self, valeur):
        for poss in self.possibilites:
            if(poss == valeur):
                return True
        return False

    def print (self):
        print(self.possibilites)


class placement:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class list_placements:

    def __init__(self, valeur):
        self.valeur = valeur
        self.placements = []

    def ajouter(self, x, y, valeur):
        if(valeur == self.valeur):
            self.placements.append(placement(x, y))
    
    def try_get_placement(self):
        if(len(self.placements) == 1):
            return self.placements[0]
        else:
            return None
    
    def print(self):
        for placement in self.placements:
            print("x: ", placement.x, " y: ", placement.y, " valeur: ", placement.valeur)
    


class sudoku:
    def __init__(self, taille):
        self.racine = taille
        self.taille = taille * taille
        self.grille = [[0 for i in range(self.taille)] for j in range(self.taille)]
        self.solutions = [[list_solutions(self.taille) for i in range(self.taille)] for j in range(self.taille)]


    def sub_matrice_to_position(self, nmatrice, i):
        x = (nmatrice % self.racine) * self.racine + (i % self.racine)
        y = (nmatrice // self.racine) * self.racine + (i // self.racine)
        return x, y

    def find_matrice(self, x, y):
        return (x // self.racine) + (y // self.racine) * self.racine

    def supprimer_impossibilites(self, x, y):
        flag = False
        list_solution = self.solutions[y][x]
        for valeur in self.solutions[y][x].possibilites.copy():
            for i in range(self.taille):
                x1, y1 = self.sub_matrice_to_position(self.find_matrice(x,y), i)
                if(self.grille[i][x] == valeur or self.grille[y][i] == valeur or self.grille[y1][x1] == valeur):
                    list_solution.possibilites.remove(valeur)
                    flag = True
                    break
        return flag
    
    def verifie_emplacement(self):
        flag_modification = False
        nb_apparitions = 0
        for valeur in list(range(1, self.taille + 1, 1)):
            for entite in range(self.taille):
                # for type_entite in range(3):
                type_entite = 0
                nb_apparitions = 0
                x_mem, y_mem = 0, 0
                for emplacement in range(self.taille):

                    if(type_entite == 0):
                        x, y = self.sub_matrice_to_position(entite, emplacement)
                    elif(type_entite == 1):
                        x, y = entite, emplacement
                    else:
                        x, y = emplacement, entite
                    liste_solutions1 = self.solutions[y][x]
                    if(liste_solutions1.contains(valeur)):
                        nb_apparitions = nb_apparitions + 1
                        x_mem, y_mem = x, y

                if(nb_apparitions == 1):
                    self.grille[y_mem][x_mem] = valeur
                    self.solutions[y_mem][x_mem].possibilites = []
                    flag_modification = True
                    self.affiche(x_mem, y_mem)

        return flag_modification

    def etape_resolution(self):
        modif = False
        for y in range(self.taille):
            for x in range(self.taille):
                if(self.grille[y][x] == 0):
                    if(self.supprimer_impossibilites(x, y)) :
                        modif = True

        if(self.verifie_emplacement() == True):
            modif = True

        for x in range(self.taille):
            for y in range(self.taille):
                    if(len(self.solutions[y][x].possibilites) == 1):
                        self.grille[y][x] = self.solutions[y][x].possibilites[0]
                        self.solutions[y][x].possibilites = []
                        self.affiche(x, y)
                        modif = True
        return modif
        

    def load_grille(self, grille):
        if(len(grille) != self.taille):
            print("Erreur: grille de taille incorrecte")
            return
        for i in range(self.taille):
            if(len(grille[i]) != self.taille):
                print("Erreur: grille de taille incorrecte")
                return
            for j in range(self.taille):
                self.grille[i][j] = grille[i][j]
                if(grille[i][j] != 0):
                    self.solutions[i][j].possibilites = []

    def affiche(self, x=-1, y=-1):
        for i in range(self.taille):
            if(i % self.racine == 0):
                for j in range(self.taille + self.racine + 1 ):
                    print("-", end=" ")
                print()
            for j in range(self.taille):
                if(j % self.racine == 0 ):
                    print("|", end=" ")
                if(self.grille[i][j] != 0):
                    if(x == j and y == i):
                        print(f"{color_red}{self.grille[i][j]}{color_end}", end=" ")
                    else:
                        print(self.grille[i][j], end=" ")
                else:
                    print(" ", end=" ")
            print("|")
        for j in range(self.taille + self.racine + 1 ):
                print("-", end=" ")
        print()
        print()
        
sudoku_solver = sudoku(3)
sudoku_solver.load_grille(grille_9x9)
sudoku_solver.affiche()

while sudoku_solver.etape_resolution():
    pass