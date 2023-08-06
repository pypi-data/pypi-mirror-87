from .cisu_enum import CisuEnum

class Severity(CisuEnum):
    """
    Précise l'urgence de l'affaire :
        EXTREME : Menace extrême pour la vie ou les biens
        SEVERE : Menace importante pour la vie ou les biens
        MODERATE - Menace possible pour la vie ou les biens
        MINOR : Peu ou pas de menace connue pour la vie ou les biens
        UNKNOWN : Niveau de menace inconnu
    """
    EXTREME = 4
    SEVERE = 3
    MODERATE = 2
    MINOR = 1
    UNKNOWN = 0

