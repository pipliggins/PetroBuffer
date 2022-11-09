# test_with_pytest.py

import petrobuffer as pb
import pytest

@pytest.fixture
def test_composition_wt():
    return {
            'sio2' : 44.71,
            'tio2' : 0.13,
            'al2o3': 1.33,
            'feo'  : 8.06,
            'mno'  : 0.13,
            'mgo'  : 38.73,
            'cao'  : 3.17,
            'na2o' : 0.13,
            'k2o'  : 0.006,
            'p2o5' : 0.019
        }

@pytest.fixture
def test_composition_mol():
    return {
            'sio2' : 0.3931,
            'tio2' : 0.00086,
            'al2o3': 0.006889,
            'feo'  : 0.059312,
            'mno'  : 0.000967,
            'mgo'  : 0.50777,
            'cao'  : 0.029856,
            'na2o' : 0.001108,
            'k2o'  : 0.000034,
            'p2o5' : 0.000071
        }

def test_wtOxtoMolOx_return_sumToOne(test_composition_wt):
    assert sum(pb.core.wtOxides_to_molOxides(test_composition_wt).values()) == pytest.approx(1,1e-10)

def test_wtOxtoMolOx_convertsCorrectly(test_composition_wt, test_composition_mol):
    assert pb.core.wtOxides_to_molOxides(test_composition_wt) == pytest.approx(test_composition_mol, 0.02)

def test_wtOxtoMolOx_where_speciesWithoutMassListed_throwException():
    test_composition_unknown_species = {            
                                        'sio2' : 44.71,
                                        'tio2' : 0.13,
                                        'al2o3': 1.33,
                                        'feo'  : 8.06,
                                        'mno'  : 0.13,
                                        'unkow3n'  : 38.73
                                        }
    with pytest.raises(KeyError) as exc:
        pb.core.wtOxides_to_molOxides(test_composition_unknown_species)
    assert "Sorry, I don't know the mass of" in str(exc.value)

def test_wtOxtoMolOx_where_inputCapitalisation_matchesOutputCapitalisation():
    test_composition_capitalized_species = {            
                                        'sio2' : 44.71,
                                        'TiO2' : 0.13,
                                        'al2o3': 1.33,
                                        'FeO'  : 8.06,
                                        'mno'  : 0.13,
                                        'MgO'  : 38.73
                                        }
    assert pb.core.wtOxides_to_molOxides(test_composition_capitalized_species).keys() == test_composition_capitalized_species.keys()
    
def test_molOxtoWtOx_return_sumToHundred(test_composition_mol):
    assert sum(pb.core.molOxides_to_wtOxides(test_composition_mol).values()) == pytest.approx(100,1e-10)

def test_molOxtoWtOx_convertsCorrectly(test_composition_wt):
    converted_mols = pb.core.wtOxides_to_molOxides(test_composition_wt)
    assert pb.core.molOxides_to_wtOxides(converted_mols) == pytest.approx(test_composition_wt, 0.001)

def test_molOxtoWtOx_where_speciesWithoutMassListed_throwException():
    test_composition_unknown_species = {            
                                        'sio2' : 0.3931,
                                        'tio2' : 0.00086,
                                        'al2o3': 0.006889,
                                        'feo'  : 0.059312,
                                        'mno'  : 0.000967,
                                        'unkow3n'  : 0.2
                                        }
    with pytest.raises(KeyError) as exc:
        pb.core.molOxides_to_wtOxides(test_composition_unknown_species)
    assert "Sorry, I don't know the mass of" in str(exc.value)

def test_molOxtoWtOx_where_inputCapitalisation_matchesOutputCapitalisation():
    test_composition_capitalized_species = {            
                                        'sio2' : 0.3931,
                                        'TiO2' : 0.00086,
                                        'al2o3': 0.006889,
                                        'FeO'  : 0.59312,
                                        'MnO'  : 0.000967,
                                        'MgO'  : 0.5
                                        }
    assert pb.core.molOxides_to_wtOxides(test_composition_capitalized_species).keys() == test_composition_capitalized_species.keys()