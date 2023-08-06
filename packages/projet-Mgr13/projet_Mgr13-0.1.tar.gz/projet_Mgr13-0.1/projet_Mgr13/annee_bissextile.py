def is_bissextile(annee):
    """Définition d'une année bissextile"""
    bissextile = False
    if (annee % 4 == 0 and annee % 100 != 0 or annee % 400 == 0):
        bissextile = True
    return bissextile


