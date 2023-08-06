__version__ = "1.0.4"

def alea(a, b):
    """Retourne un entier aléatoire dans l'intervalle [a, b]"""
    from random import randint
    return randint(a, b)


def arrondi(x):
    """Retourne l'entier le plus proche de x"""
    ex = int(x)
    dx = x - ex
    if abs(x - ex) >= 0.5:
        return ex + (1 if dx > 0 else -1)
    return ex


def racine(x):
    """Retourne la racine carré de x"""
    return x ** 0.5


def ent(x):
    """Retourne la partie entière de x"""
    if type(x) == float:
        return int(x)
    elif type(x) == int:
        return x
    raise TypeError(f"x possède un type invalide.")


def long(ch):
    """Retourne la longueur de la chaine ch"""
    if type(ch) == str:
        return len(ch)
    raise TypeError(f"ch doit être de type str")


def pos(ch1, ch2):
    """Retourne la première position de ch1 dans ch, -1 sinon."""
    if type(ch1) == str and type(ch2) == str:
        return ch2.find(ch1)
    raise TypeError(f"ch1 et ch2 doivent être de type str")


def convch(x):
    """Convertit un nombre en une chaine de caractères"""
    if type(x) == float or type(x) == int:
        return str(x)
    raise TypeError(f"x doivent être de type int ou float")


def estnum(ch):
    """Retourne True si ch contient une valeur numérique, False sinon"""
    return ch.isnumeric()


def valeur(ch):
    """Convertit une chaine de caractères en une valeur numérique"""
    try:
        return int(ch)
    except Exception:
        pass
    return float(ch)


def sous_chaine(ch, d=None, f=None):
    """Retourne une sous chaine de ch à partir de l'indice d (inclus) jusqu'à l'indice f exclus."""
    if type(ch) == str:
        if d is None and f is None:
            return ch[:]
        elif d is None:
            return ch[:f]
        elif f is None:
            return ch[d:]
        return ch[d:f]
    raise TypeError("ch doit être de type str")

def effacer(ch, d=None, f=None):
    """Efface les caractères à partir de l'indice d (inclus) jusqu'à l'indice f exclus."""
    if type(ch) == str:
        if d is None and f is None:
            return ""
        elif d is None:
            return ch[f:]
        elif f is None:
            return ch[:d]
        if f > d:
            return ch[:d] + ch[f:]
        return ch
    raise TypeError("ch doit être de type str")


def majus(ch):
    """Convertit ch en majuscules"""
    if type(ch) == str:
        return ch.upper()
    raise TypeError("ch doit être de type str")
