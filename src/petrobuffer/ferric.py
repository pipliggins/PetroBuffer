import numpy as np

def fo2_to_iron_kc91(C,T,P,lnfo2):
    """
    Calculates the Fe2O3/FeO mole ratio of a melt where the fO2 is known.

    Parameters
    ----------
    C : dictionary
        Major element composition of the silicate melt as MOLE FRACTIONS
        Required species: Al2O3, FeOt, CaO,  Na2O, K2O    
    T : float
        Temperature in degrees K    
    P : float
        Pressure in pascals (Pa)    
    lnfo2 : float
        ln(fO2)

    Returns
    -------
    float
        Fe2O3/FeO mole ratio

    References
    ----------
    Kress and Carmichael (1991) The compressibility of silicate liquids
    containing Fe2O3 and the effect of composition, temperature, oxygen 
    fugacity and pressure on their redox states
    
    Notes
    -----------------------
    ln(X_Fe2O3/X_FeO) = a*FO2 + b/T + c + sum(d_i*X_i) + e*[1-T0/T-ln(T/T0)]
                         + f*P/T + g*[(T-T0)*P]/T + h*P^2/T
    
    a = 0.196
    b = 1.1492e4                K
    c = -6.675
    dal2o3 = -2.243
    dfeo = -1.828
    dcao = 3.201
    dna2o = 5.854
    dk2o = 6.215
    e = -3.36
    f = -7.01e-7                K/Pa
    g = -1.54e-10               /Pa
    h = 3.85e-17                K/Pa^2        
    """

    dal2o3 = -2.243
    dfeo = -1.828
    dcao = 3.201
    dna2o = 5.854
    dk2o = 6.215

    T0 = 1673.0                 # K

    F = np.exp(0.196*lnfo2 + 1.1492e4/T -6.675 + dal2o3*C['al2o3'] + dfeo*C['feo']
        + dcao*C['cao'] + dna2o*C['na2o'] + dk2o*C['k2o'] - 3.36*(1.0 - T0/T
        - np.log(T/T0)) - 7.01e-7*P/T - 1.54e-10*(T-T0)*P/T + 3.85e-17*P**2/T)

    return F

def iron_to_fo2_kc91(C,T,P):
    """
    Calculates the oxygen fugacity (fO2) of a melt given where the ferric/
    ferrous ratio is known. 

    Parameters
    ----------
    C : dictionary
        Major element composition of the silicate melt as mole fractions
        Required species: Al2O3, FeO, Fe2O3, CaO,  Na2O, K2O    
    T : float
        Temperature in degrees K    
    P : float
        Pressure in pascals (Pa)

    Returns
    -------
    float
        ln(fO2)
    
    References
    ----------
    Kress and Carmichael (1991) The compressibility of silicate liquids
    containing Fe2O3 and the effect of composition, temperature, oxygen
    fugacity and pressure on their redox states
    
    Notes
    -----------------------  
    ln(fO2) = [ln(X_Fe2O3/X_FeO) - b/T - c - sum(d_i*X_i) 
            - e*[1-T0/T-ln(T/T0)] - f*P/T - g*[(T-T0)*P]/T - h*P^2/T]/a
    
    a = 0.196
    b = 1.1492e4                K
    c = -6.675
    dal2o3 = -2.243
    dfeo = -1.828
    dcao = 3.201
    dna2o = 5.854
    dk2o = 6.215
    e = -3.36
    f = -7.01e-7                K/Pa
    g = -1.54e-10               /Pa
    h = 3.85e-17                K/Pa^2        
    """

    dal2o3 = -2.243
    dfeo = -1.828
    dcao = 3.201
    dna2o = 5.854
    dk2o = 6.215

    T0 = 1673.0  # K
    FeOt = C['feo'] + C['fe2o3']*0.8998 # total iron as a mole fraction

    FO2 = (np.log(C['fe2o3']/C['feo']) - 1.1492e4/T + 6.675 - dal2o3*C['al2o3']
        - dfeo*(FeOt) - dcao*C['cao'] - dna2o*C['na2o'] - dk2o*C['k2o'] + 3.36*(1.0 - T0/T
        - np.log(T/T0)) + 7.01e-7*(P/T) + 1.54e-10*(T-T0)*P/T - 3.85e-17*P**2/T)/0.196

    return FO2

def fo2_to_iron_r13(C, T, P, lnfo2):
    """
    Calculates the Fe2O3/FeO mole ratio of an FeOt>15 wt% melt where the
    fO2 is known.   

    Parameters
    ----------
    C : dictionary
        Major element composition of the silicate melt as mole fractions
        Required species: Al2O3, FeOt, CaO, Na2O, K2O, P2O5    
    T : float
        Temperature in degrees K    
    P : float
        Pressure in gigapascals (GPa)    
    lnfo2 : float
        ln(fO2)

    Returns
    -------
    float
        Fe2O3/FeO mole ratio
    
    References
    ----------
    Righter et al. (2013) Redox systematics of martian magmas with
    implications for magnetite stability.
    """
    a = 0.22
    b = 3800
    c = -370
    dfeo = -6.6
    dal2o3 = 7.3
    dcao = 17.3
    dna2o = 132.3
    dk2o = -147.8
    dp2o5 = 0.6
    j = -4.26       
    

    F = np.exp(a*lnfo2 + b/T + c*(P/T) + dfeo*C['feo'] + dal2o3*C['al2o3']
        + dcao*C['cao'] + dna2o*C['na2o'] + dk2o*C['k2o'] + dp2o5*C['p2o5'] + j)
    
    return F

def iron_to_fo2_r13(C, T, P):
    """
    Calculates the oxygen fugacity (fO2) of an FeOt>15 wt% melt given
    where the ferric/ferrous ratio is known.

    Parameters
    ----------
    C : dictionary
        Major element composition of the silicate melt as mole fractions
        Required species: Al2O3, FeOt, CaO, Na2O, K2O, P2O5    
    T : float
        Temperature in degrees K    
    P : float
        Pressure in gigapascals (GPa)

    Returns
    -------
    float
        ln(fO2)

    References
    ----------
    Righter et al. (2013) Redox systematics of martian magmas with 
    implications for magnetite stability.
    """
    a = 0.22
    b = 3800
    c = -370
    dfeo = -6.6
    dal2o3 = 7.3
    dcao = 17.3
    dna2o = 132.3
    dk2o = -147.8
    dp2o5 = 0.6
    j = -4.26       
    

    FeOt = C['feo'] + C['fe2o3']*0.8998     # total iron mole fraction

    lnfo2 = (np.log(C['fe2o3']/C['feo']) - (b/T + c*(P/T) + dfeo*(FeOt)
            + dal2o3*C['al2o3']  + dcao*C['cao'] + dna2o*C['na2o'] + dk2o*C['k2o']
            + dp2o5*C['p2o5'] + j))/a
    
    return lnfo2