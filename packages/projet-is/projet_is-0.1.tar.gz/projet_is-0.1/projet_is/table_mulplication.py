def table(nombre):
    """Définition d'une année bissextile"""
    print("La table de multiplication de : ", nombre, " est :")
    for i in range(1, 11):
        print(i, " x ", nombre, " = ", i * nombre)
