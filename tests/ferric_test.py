import petrobuffer as pb
import pytest

def test_fo2ToIronKc91_where_correctInput_gives_appropriateValue():
    test_composition = {'sio2' : 0.3931, # mole fractions
                    'tio2' : 0.0009,
                    'al2o3': 0.0069,
                    'feo'  : 0.0593,
                    'mno'  : 0.001,
                    'mgo'  : 0.5078,
                    'cao'  : 0.0299,
                    'na2o' : 0.0011,
                    'k2o'  : 0.000034,
                    'p2o5' : 0.0001}    
    assert pb.ferric.fo2_to_iron_kc91(test_composition, 1473.15, 1, -21.415901) == pytest.approx(0.0467, 0.001)

def test_IronToFo2Kc91_where_correctInput_gives_appropriateValue():
    test_composition = {'sio2' : 0.8257, # mole fractions
                    'tio2' : 0.0019,
                    'al2o3': 0.0607,
                    'fe2o3': 0.0167,
                    'feo'  : 0.0143,
                    'mno'  : 0.0024,
                    'mgo'  : 0.0,
                    'cao'  : 0.0024,
                    'na2o' : 0.0455,
                    'k2o'  : 0.0302,
                    'p2o5' : 0.0}    
    assert pb.ferric.iron_to_fo2_kc91(test_composition, 1473.15, 1) == pytest.approx(-6.4952, 0.01)

def test_Fo2ToIronR2013_where_correctInput_gives_appropriateValue():
    test_composition = {'sio2' : 0.5771, # mole fractions
                    'tio2' : 0.0102,
                    'al2o3': 0.0262,
                    'feo'  : 0.1685,
                    'mno'  : 0.0023,
                    'mgo'  : 0.0785,
                    'cao'  : 0.1155,
                    'na2o' : 0.0183,
                    'k2o'  : 0.00173,
                    'p2o5' : 0.0016}    
    assert pb.ferric.fo2_to_iron_r13(test_composition, 1473.15, 1, -19.6967) == pytest.approx(0.048762, 0.001)

def test_IronToFo2R2013_where_correctInput_gives_appropriateValue():
    test_composition = {'sio2' : 0.5771, # mole fractions
                    'tio2' : 0.0102,
                    'al2o3': 0.0262,
                    'fe2o3': 0.04,
                    'feo'  : 0.1285,
                    'mno'  : 0.0023,
                    'mgo'  : 0.0785,
                    'cao'  : 0.1155,
                    'na2o' : 0.0183,
                    'k2o'  : 0.00173,
                    'p2o5' : 0.0016}    
    assert pb.ferric.iron_to_fo2_r13(test_composition, 1473.15, 1) == pytest.approx(-11.3887, 0.001)