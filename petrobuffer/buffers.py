from petrobuffer import core

def calcBuffer(name, T, P):
    """
    Main function to calculate the fO2 of a given buffer under specified
    T P conditions.

    Parameters
    ----------
    buffer_name: string
        Possible buffers are: QIF, IW, WM, IM, CoCoO, FMQ, NNO, MH.    
    T: float
        Temperature in degrees K    
    P: float
        Pressure in bar

    Returns
    -------
    float
        absolute fO2, as log10(fO2)
    """

    if name == 'QIF':
        if T < 573+273.15:
            return frost1991('QIF_lowT', T, P)
        else:
            return frost1991('QIF_highT', T, P)
    elif name == 'IW':
        if core.bar_to_gpa(P) > 10:
            return calc_iw_highp(core.bar_to_gpa(P), T)
        else:
            return frost1991('IW', T, P)
    elif name == 'WM':
        return frost1991('WM', T, P)
    elif name == 'IM':
        return frost1991('IM', T, P)
    elif name == 'CoCoO':
        return frost1991('CoCoO', T, P)
    elif name == 'FMQ':
        if T < 573+273.15:
            return frost1991('FMQ_lowT', T, P)
        else:
            return frost1991('FMQ_highT', T, P)
    elif name == 'NNO':
        if core.bar_to_gpa(P) > 10:
            return calc_nno_highp(core.bar_to_gpa(P), T)
        else:
            return frost1991('NNO', T, P)
    elif name == 'MH':
        if T < 573+273.15:
            return frost1991('MH_lowT', T, P)
        elif T < 682+273.15:
            return frost1991('MH_midT', T, P)
        else:
            return frost1991('MH_highT', T, P)
    else:
        raise core.InputError(f"'{name}' not recognized as a buffer.")

# --------------------- DEFINE BUFFER EQUATIONS ------------------------ #

def frost1991(buffer_name, T, P):
    """
    Calculate mineral buffer at given T and P as listed in Frost 1991

    Parameters
    ----------
    buffer_name : string
        Possible buffers are: QIF_highT, QIF_lowT, IW, WM, IM, CoCoO,
                       FMQ_highT, FMQ_lowT, NNO, MH_highT, MH_midT, MH_lowT.    
    T : float
        Temperature in degrees K    
    P : float
        Pressure in bar

    Returns
    -------
    float
        log10(fO2)

    References
    ----------
    Frost (1991) Mineralogical Society of America "Reviews in Mineralogy",
    Volume 25

    Polynomial coefficients
    -----------------------  
    log10(fO2) = a/T + b + c*(P-1)/T

    buffer: (a, b, c)
    """

    coefficients = {'QIF_lowT':  (-29435.7,  7.391, 0.044),
                    'QIF_highT': (-29520.8,  7.492, 0.050),
                    'IW':        (-27489.0,  6.702, 0.055),
                    'WM':        (-32807.0, 13.012, 0.083),
                    'IM':        (-28690.6,  8.130, 0.056),
                    'CoCoO':     (-24332.6,  7.295, 0.052),
                    'FMQ_lowT':  (-26455.3, 10.344, 0.092),
                    'FMQ_highT': (-25096.3,  8.735, 0.110),
                    'NNO':       (-24930.0,  9.360, 0.046),
                    'MH_lowT':   (-25497.5, 14.330, 0.019),
                    'MH_midT':   (-26452.6, 15.455, 0.019),
                    'MH_highT':  (-25700.6, 14.558, 0.019)
                    }

    a, b, c = coefficients[buffer_name]

    return a/T + b + c*(P-1)/T

def calc_iw_highp(P, T):
	""" 
	Define IW buffer value at P, T at high pressure.

	Parameters
	----------
	P : float
		Pressure in GPa
	T : float
		Temperature in degrees K

	Returns
	-------
	float
		log10(fO2)

    References
    ----------
	Campbell et al. (2009) High-pressure effects on the iron-iron oxide and
    nickel-nickel oxide oxygen fugacity buffers - Table S4

    Polynomial coefficients
    -----------------------
    log10 fO2  =  (a0 + a1*P) + (b0 + b1*P + b2*P^2 + b3*P^3)/T

	a0: 6.54106
	a1: 0.0012324
	b0: -28163.6
	b1: 546.32
	b2: -1.13412
	b3: 0.0019274                            
	"""
	log_fO2 = (6.54106 + 0.0012324*P) + (-28163.6 + 546.32*P - 1.13412*P**2 +
                 0.0019274*P**3)/T

	return log_fO2

def calc_nno_highp(P, T):
	""" 
	Define NNO buffer value at P, T at high pressure.

	Parameters
    ----------
    P: float
		Pressure in GPa
	T: float
		Temperature in degrees K
    
    Returns
    -------
    float
	    log10(fO2)

	References
	----------
	Campbell et al. (2009) High-pressure effects on the iron-iron oxide and
    nickel-nickel oxide oxygen fugacity buffers - Table S5
    
    Polynomial coefficients
    -----------------------
    log10 fO2 = (a0 + a1*P + a2*P^2 + a3*P^3 + a4*P^4) + (b0 + b1*P + b2*P^2 + b3*P^3)/T

	a0: 8.699
	a1: 0.01642
	a2: -0.0002755
	a3: 0.000002683
	a4: -1.015E-08
	b0: -24205
	b1: 444.73
	b2: -0.59288
	b3: 0.0015292                            
	"""
	log_fO2 = (8.699 + 0.01642*P -0.0002755*P**2 + 2.683e-6*P**3 - 1.015e-8*P**4) + (
            -24205 + 444.73*P - 0.59288*P**2 + 0.0015292*P**3)/T

	return log_fO2