
# --------- DEFINE SOME CONSTANTS & CONVERSIONS -----------#

oxideMass = {'sio2':  60.083,
             'mgo':   40.304,
             'feo':   71.844,
             'cao':   56.077,
             'al2o3': 101.961,
             'na2o':  61.979,
             'k2o':   94.195,
             'mno':   70.937,
             'tio2':  79.867,
             'p2o5':  141.943,
             'cr2o3': 151.992,
             'nio':   74.692,
             'coo':   44.01,    #CoO
             'fe2o3': 159.687}

# -------------CORE DEFINITIONS------------- #
class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class InputError(Error):
    """
    Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message

# ------------TEMPERATURE CONVERSIONS----------- #

def C2K(T):
    """Convert temperatures in degrees Celsius to Kelvin"""
    return T + 273.15

# -------------PRESSURE CONVERSIONS------------- #

def bar_to_pa(P):
    """Convert pressure from bar -> pascal (Pa)."""
    return P*1e5

def bar_to_gpa(P):
    """Convert pressure from bar -> gigapascal (GPa)."""
    return P*1e-4

def pa_to_bar(P):
    """Convert pressure from pascal (Pa) -> bar."""
    return P*1e-5

def gpa_to_bar(P):
    """Convert pressure from gigapascal (GPa) -> bar."""
    return P*1e4

# -------------- OXIDE CONVERSIONS --------------- #

def wtOxides_to_molOxides(C:dict)->dict:
    """
    Converts units of a major element composition from wt % to mole frac.

    Parameters
    ----------
    C : dict
        Major element composition of the silicate melt as weight percents.
    
    Returns
    -------
    dict
        major element composition as mole fractions
    """

    # Normalise the weight percent to 100
    original_sum = sum(C.values())

    for ele, wt in C.items():
        C[ele] = (wt*100)/original_sum

    # convert
    C_mol = {}
    sm = 0

    for ele in C:
        if ele.lower() not in oxideMass:
            raise KeyError(f"Sorry, I don't know the mass of '{ele}'.")
        C_mol[ele] = C[ele] / oxideMass[ele.lower()]
        sm += C[ele] / oxideMass[ele.lower()]

    for ele in C:
        C_mol[ele] = C_mol[ele] / sm

    return C_mol
        
def molOxides_to_wtOxides(Cmol:dict)->dict:
    """Converts major element composition from mol frac to normalised wt%"""

    Cwt = {}
    sm = 0

    for ele in Cmol:
        if ele.lower() not in oxideMass:
            raise KeyError(f"Sorry, I don't know the mass of '{ele}'.")
        Cwt[ele] = Cmol[ele] * oxideMass[ele.lower()]
        sm += Cmol[ele] * oxideMass[ele.lower()]

    for ele in Cmol:
        Cwt[ele] = Cwt[ele]*100 / sm

    return Cwt

