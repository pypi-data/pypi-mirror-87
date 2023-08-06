"""
bisextiles

"""
def annee_bissextile(annee):
    return (( annee % 400 ==0 ) or (annee % 4 ==0 and annee % 100 !=0))
