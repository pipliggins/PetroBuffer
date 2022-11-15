# PL add warning about T/P limits
from typing import Union
import numpy as np
from petrobuffer import core
from petrobuffer import buffers
from petrobuffer import ferric

# ------------------- FO2 BUFFERS ------------------------

def get_relative_fo2(fO2, buffer, T, P, celsius=False):
    """
    Main function to calculate fO2 in terms of a given buffer.

    Parameters
    ----------
    fO2 : float
        absolute fO2, as log10(fO2)
    buffer : str
        name of the buffer to give fO2 as relative to.
        one from: QIF, IW, WM, IM, CoCoO, FMQ, NNO, MH.    
    T : float
        Temperature in degrees K        
    P : float
        Pressure in bar
    celsius : bool, default=False
        Whether temperatures are in Kelvin (`False`) or celsius (`True`)

    Returns
    -------
    float
        fO2 relative to the specified buffer, given as log10(fO2)
    """

    if celsius == True:
        T += 273.15    # convert temperature to K

    if buffer == 'CoCoO':
        pass
    elif buffer == 'cocoo':
        buffer = 'CoCoO'
    else:
        buffer = buffer.upper()

    return fO2 - buffers.calcBuffer(buffer, T, P)

def get_absolute_fo2(fO2, buffer, T, P, celsius=False):
    """
    Main function to calculate fO2 in terms of a given buffer.

    Parameters
    ----------
    fO2 : float
        fO2 relative to `buffer`
    buffer : str
        name of the buffer to give fO2 as relative to.
        one from: QIF, IW, WM, IM, CoCoO, FMQ, NNO, MH.    
    T : float
        Temperature in degrees K        
    P : float
        Pressure in bar
    celsius : bool, default=False
        Whether temperatures are in Kelvin (`False`) or celsius (`True`)
        
    Returns
    -------
    float
        fO2 relative to the specified buffer, given as log10(fO2)
    """

    if celsius == True:
        T += 273.15    # convert temperature to K

    if buffer == 'CoCoO':
        pass
    elif buffer == 'cocoo':
        buffer = 'CoCoO'
    else:
        buffer = buffer.upper()

    return fO2 + buffers.calcBuffer(buffer, T, P)

def convert_buffer(fO2:Union[float, int], old_buffer:str, new_buffer:str, T:Union[float,
                    int], P:Union[float, int], celsius:bool=False)->float:
    """
    Translate an fO2 value from one relative buffer to another.

    Parameters
    ----------
    fO2 : float or int
        The current fO2, relative to `old_buffer`.
    old_buffer : str
        Name of the original buffer the `fO2` is relative to.\
        One from: QIF, IW, WM, IM, CoCoO, FMQ, NNO, MH.
    new_buffer : str
        Name of the new buffer the fO2 should be relative to.\
        One from: QIF, IW, WM, IM, CoCoO, FMQ, NNO, MH.
    T : float or int
        Temperature in degrees K
    P : float or int
        Pressure in bar
    celsius : bool, default=False
        Whether temperatures are in Kelvin (`False`) or celsius (`True`)

    Returns
    -------
    float
        fO2 relative to the new buffer, given as log10(fO2)
    """

    if celsius == True:
        T += 273.15    # convert temperature to K
    
    bfs = [old_buffer, new_buffer]
    for idx, buffer in enumerate(bfs):
        if buffer == 'CoCoO':
            pass
        elif buffer == 'cocoo':
            bfs[idx] = 'CoCoO'
        else:
            bfs[idx] = buffer.upper()

    old_buffer, new_buffer = bfs
    
    absolute_fo2 = fO2 + buffers.calcBuffer(old_buffer, T, P)

    new_fo2 = absolute_fo2 - buffers.calcBuffer(new_buffer, T, P)

    return new_fo2

# ---------------------- FO2 <-> FERRIC/FERROUS CONVERSIONS ------------------

def get_ironOxide(C:dict, fO2:Union[float, int], T:Union[float, int], 
                P:Union[float, int], celsius=False, normalised_comp=True,
                buffer:str = None, force_model:str = None) -> float: 
    """
    Returns the ferric/ferrous (Fe2O3/FeO) mole ratio of a melt given fO2.

    Parameters
    ----------
    C : dict
        Major element composition of the silicate melt as weight percents.
        Required species: Al2O3, FeOt, CaO, Na2O (+ K2O if using r2013)    
    fO2 : float or int
        fO2 as either an absolute value given as log10(fO2), or relative
        to a buffer if one is specified in the `buffer` argument.    
    T : float
        Temperature in degrees K    
    P : float
        Pressure in bar    
    celsius : bool, default=False
        If true, `T` can be given in Celsius rather than degrees Kelvin.
    normalised_comp : bool, default=True
        Selects whether the composition being returned is normalised, or
        if only the Fe2O3 and FeO is recalculated.
    buffer : str, optional
        The buffer `fO2` is relative to if it is not an absolute value.
        One of QIF, IW, WM, IM, CoCoO, FMQ, NNO, MH.
    force_model : str, optional
        Forces the model used, rather than allowing selection based on
        total FeO content. One from `kc1991` (Kress & Carmichael 1991)
        or `r2013` (Righter et.al., 2013).
    
    Returns
    -------
    float
        Fe2O3/FeO mole ratio
    dict
        New melt major oxide composition as wt%
    """
    
    force_options = ['kc1991', 'r2013']
    if force_model is not None and force_model not in force_options:
        raise core.InputError(f"Invalid model option. Expected either {None} or one of:\
             {force_options}")

    buffer_options = ['QIF', 'IW', 'WM', 'IM', 'CoCoO', 'FMQ', 'NNO', 'MH']
    if buffer is not None and buffer not in buffer_options:
        raise core.InputError(f"Invalid buffer. Expected either {None} or one of:\
             {buffer_options}")
    
    if celsius == True:
        T += 273.15    # convert degrees C to K
        
    C_lower = dict((k.lower(), v) for k,v in C.items())
    original_sum = sum(C.values())

    feot_options_set = set(['feot', 'feo_t', 'feo(t)'])    
    C_set=set(C_lower)
    match_feo_name = feot_options_set.intersection(C_set)

    # check iron is present in the composition dict, + ensure it's in the correct form
    if 'feo' in C_lower and 'fe2o3' in C_lower:
        C_lower['feo'] = (C_lower['feo'] + 0.8998*C_lower['fe2o3'])*100/original_sum
        C_lower.pop('fe2o3')
    elif 'fe2o3' in C_lower and 'feo' not in C_lower:
        C_lower['feo'] = (0.8998*C_lower['fe2o3'])*100/original_sum
        C_lower.pop('fe2o3')
    elif match_feo_name:
        # rename to call total FeO, just FeO
        C_lower['feo'] = C_lower[match_feo_name[0]]
        C_lower.pop(match_feo_name[0])  
    elif not C_lower['feo']:
        raise core.InputError("Composition is missing total FeO. Please add as 'feo'.")
    
    # check the total iron content and pick an appropriate model   
    
    if force_model == None:
        if C_lower['feo'] < 15.0:
            force_model = 'kc1991'
        else:
            force_model = 'r2013'
    
    required_species = ['al2o3', 'feo', 'cao', 'na2o', 'k2o']
    if force_model=='r2013': required_species.append('p2o5')

    check = all(item in C_lower.keys() for item in required_species)
    if check == False:
        raise core.InputError(f"Some of the required species for calculating the ferric\
            /ferrous ratio are missing. Include all of {required_species}, where FeO is\
                total iron.")

    oxide_mf = core.wtOxides_to_molOxides(C_lower.copy())

    # convert fO2 to ln(fO2)
    if isinstance(buffer, str):
        lnfO2 = np.log(10**(get_absolute_fo2(fO2, buffer, T, P)))
    else:
        lnfO2 = np.log(10**(fO2))
    
    if force_model == 'kc1991':
        F = ferric.fo2_to_iron_kc91(oxide_mf, T, core.bar_to_pa(P), lnfO2)
    elif force_model == 'r2013':
        F = ferric.fo2_to_iron_r13(oxide_mf, T, core.bar_to_gpa(P), lnfO2)

    oxide_mf['feo'] = oxide_mf['feo']/(2*F + 1)
    oxide_mf['fe2o3'] = oxide_mf['feo']*F

    # calculate the new composition holding the mole fraction of total Fe
    # constant and recalculating XFeO and XFe2O3.
    oxide_mf_X_mw = {}
    for ele in oxide_mf:
        oxide_mf_X_mw[ele] = oxide_mf[ele]*core.oxideMass[ele]
    total = sum(oxide_mf_X_mw.values())
    C_lower['feo'] = oxide_mf_X_mw['feo']*100/total
    C_lower['fe2o3'] = oxide_mf_X_mw['fe2o3']*100/total

    if normalised_comp == False:
        for sp in C:
            C_lower[sp] = C_lower.pop(sp.lower())
        C_lower['Fe2O3'] = C_lower.pop('fe2o3')
        return F, C_lower
    else:
        C_new = core.molOxides_to_wtOxides(oxide_mf.copy())
        for sp in C:
            C_new[sp] = C_new.pop(sp.lower())
        C_new['Fe2O3'] = C_new.pop('fe2o3')
        return F, C_new
    

def get_meltfO2(C:dict, T:Union[float, int], P:Union[float, int], celsius=False,
                buffer:str = None, force_model:str = None) -> float:
    """
    Returns the fO2 of a melt, given the FeO and Fe2O3 content.

    Parameters
    ----------
    C : dict
        Major element composition of the silicate melt as weight percents.
        Required species: Al2O3, FeOt, CaO, Na2O (+ K2O if using r2013)
    T : float
        Temperature in degrees K    
    P : float
        Pressure in bar    
    celsius : bool, default=False
        If true, `T` can be given in Celsius rather than degrees Kelvin.
    buffer : str, optional
        The buffer the returned fO2 should be is relative to. If None, fO2
        is returned as an absolute value (log10(fO2)).
        One of QIF, IW, WM, IM, CoCoO, FMQ, NNO, MH.
    force_model : str, optional
        Forces the model used, rather than allowing selection based on
        total FeO content. One from `kc1991` (Kress & Carmichael 1991)
        or `r2013` (Righter et.al., 2013).
    
    Returns
    -------
    float
        fO2 as log10(fO2)
    str
        buffer fO2 is relative to, set with `buffer`, otherwise 'absolute'.
    """

    force_options = ['kc1991', 'r2013']
    if force_model is not None and force_model not in force_options:
        raise core.InputError(f"Invalid model option. Expected either {None} or one of:\
             {force_options}")

    buffer_options = ['QIF', 'IW', 'WM', 'IM', 'CoCoO', 'FMQ', 'NNO', 'MH']
    if buffer is not None and buffer not in buffer_options:
        raise core.InputError(f"Invalid buffer. Expected either {None} or one of:\
             {buffer_options}")
    
    if celsius == True:
        T = core.C2K(T)    # convert degrees C to K
        
    C_lower = dict((k.lower(), v) for k,v in C.items())

    if 'feo' not in C_lower.keys() or 'fe2o3' not in C_lower.keys():
        raise core.InputError("Composition is missing an iron species. Please include\
             both FeO and Fe2O3.")

    feo_total = C_lower['feo'] + (C_lower['fe2o3']/core.oxideMass['fe2o3'])*2*core.oxideMass['feo']
    
    if force_model == None:
        if feo_total < 15.0:
            force_model = 'kc1991'
        else:
            force_model = 'r2013'
    
    required_species = ['al2o3', 'feo', 'fe2o3', 'cao', 'na2o', 'k2o']
    if force_model=='r2013': required_species.append('p2o5')

    check = all(item in C_lower.keys() for item in required_species)
    if check == False:
        raise core.InputError(f"Some of the required species for calculating the ferric\
            /ferrous ratio are missing. Include all of {required_species}.")

    oxide_mf = core.wtOxides_to_molOxides(C_lower.copy())
    
    if force_model == 'kc1991':
        absolute_fo2 = np.log10(np.exp(ferric.iron_to_fo2_kc91(oxide_mf, T,
         core.bar_to_pa(P))))
    elif force_model == 'r2013':
        absolute_fo2 = np.log10(np.exp(ferric.iron_to_fo2_r13(oxide_mf, T,
         core.bar_to_gpa(P)))) 

    if isinstance(buffer, str):
        return get_relative_fo2(absolute_fo2, buffer, T, P), buffer

    else:
        return absolute_fo2, None