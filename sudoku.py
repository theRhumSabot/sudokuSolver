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
        self.confirmations_chiffres = []

    def sub_matrice_to_position(self, nmatrice, i):
        x = (nmatrice % self.racine) * self.racine + (i % self.racine)
        y = (nmatrice // self.racine) * self.racine + (i // self.racine)
        return x, y

    def find_matrice(self, x, y):
        return (x // self.racine) + (y // self.racine) * self.racine
    
    def get_position_from_entite_type(self, entite_type, entite, emplacement):
        if(entite_type == 0):
            return self.sub_matrice_to_position(entite, emplacement)
        elif(entite_type == 1):
            return entite, emplacement
        else:
            return emplacement, entite

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
                for type_entite in range(3):
                    nb_apparitions = 0
                    list_positions = []
                    for emplacement in range(self.taille):
                        x,y = self.get_position_from_entite_type(type_entite, entite, emplacement)
                        liste_solutions1 = self.solutions[y][x]
                        if(liste_solutions1.contains(valeur)):
                            nb_apparitions = nb_apparitions + 1
                            list_positions.append([x, y])

                    if(nb_apparitions == 1):
                        [x,y] = list_positions[0]
                        self.confirmer_chiffre(x,y,valeur)
                        flag_modification = True

                    elif (False and type_entite == 0 and
                        nb_apparitions <= self.racine and nb_apparitions != 0) :
                        # si les valeurs sont alignées dans une matrice alors on supprime les possibilités dans la ligne
                        if(all(pos[0] == list_positions[0][0] for pos in list_positions)):
                            for y_position in range(self.taille):
                                x_position = list_positions[0][0]
                                if(self.find_matrice(x_position, y_position) != entite):
                                    try:
                                        self.solutions[y_position][x_position].possibilites.remove(valeur)
                                    except:
                                        pass

                        elif all(pos[1] == list_positions[0][1] for pos in list_positions):
                            for x_position in range(self.taille):
                                y_position = list_positions[0][1]
                                if(self.find_matrice(x_position, y_position) != entite):
                                    try:
                                        self.solutions[y_position][x_position].possibilites.remove(valeur)
                                    except:
                                        pass
        return flag_modification
    
    def confirmer_chiffre(self, x, y, valeur):
        self.confirmations_chiffres.append([x,y,valeur])

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
                        self.confirmer_chiffre(x,y,self.solutions[y][x].possibilites[0])
                        modif = True
        
        for confs in self.confirmations_chiffres:
            x,y,val = confs
            self.grille[y][x] = val
            self.solutions[y][x].possibilities = []
            self.affiche(x,y)
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
        
sudoku_solver = sudoku(2)
#sudoku_solver.load_grille(grille_9x9)
sudoku_solver.load_grille(grille_4x4)
sudoku_solver.affiche()

while sudoku_solver.etape_resolution():
    pass