
# cette fonction permet d'afficher la table de multiplication
# d'un nombre donné

def multiplication(nombre):
    for n in range(11) :
        print ("{:d} * {:d} = {:d}".format(nombre,n,nombre*n))