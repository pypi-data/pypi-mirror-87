
# cette fonction permet de vérifier si une année est bissextile ou pas


def annee_bissextile (annee):
    return annee % 4 == 0 and (annee % 100 != 0 or annee % 400 == 0)