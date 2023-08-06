"""
Table de Multiplication

"""

def table(base):
    if(base>0):
        print("\n")
        for n in range(1,base+1):
            print("--------------------------------------")
            print(f"la table de multiplication de: {n} est : ")
            for i in range(1,13):
                print(f"{n} * {i} = {i*n}")
            print("--------------------------------------\n")
    else:
        print(f"Erreur de saisi {base} n'est pas un entier positif")


