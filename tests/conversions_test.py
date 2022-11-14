# test_with_pytest.py

import petrobuffer as pb
import pytest

from petrobuffer.core import InputError

def test_getRelativefO2_where_BufferNameUnrecognised_raiseException():
    with pytest.raises(InputError) as exc:
        pb.get_relative_fo2(-2, 'BIF', 1473.15, 10)
    assert "not recognized as a buffer" in str(exc.value)

@pytest.mark.parametrize("buffer_cases", [
    'iw', 'fmq', 'cocoo', 'CoCoO', 'MH'])
def test_getRelativefO2_robustTo_BufferNameLowercase(buffer_cases):
    try:
        pb.get_relative_fo2(-2, buffer_cases, 1473.15, 10)
    except InputError as exc:
        assert False, f"'{buffer_cases}' raised an exception {exc}"

def test_getRelativefO2_where_CelsiusT_matches_KelvinT_result():
    assert pb.get_relative_fo2(-2, 'FMQ', 1473.15, 10) == pb.get_relative_fo2(-2, 'FMQ'
                                                            , 1200, 10, celsius=True)

def test_getRelativefO2_where_valueMatchesExpected():
    assert pb.get_relative_fo2(-4.95224, 'FMQ', 1473.15, 10) == pytest.approx(+3.3479,
                                                                             0.001)

def test_getAbsolutefO2_where_valueMatchesExpected():
    assert pb.get_absolute_fo2(+3.3479, 'FMQ', 1473.15, 10) == pytest.approx(-4.95224,
                                                                             0.001)

@pytest.mark.parametrize("buffer_cases", [
    'iw', 'fmq', 'cocoo', 'CoCoO', 'MH'])
def test_getAbsolutefO2_robustTo_BufferNameLowercase(buffer_cases):
    try:
        pb.get_absolute_fo2(+3.3479, buffer_cases, 1473.15, 10)
    except InputError as exc:
        assert False, f"'{buffer_cases}' raised an exception {exc}"

def test_convertBuffer_where_valueMatchesExpected():
    assert pb.convert_buffer(-2, 'FMQ', 'IW', 1473.15, 10) == pytest.approx(1.6575,
                                                                             0.001)

@pytest.mark.parametrize("buffer_cases_start, buffer_cases_end, final_value", [
    ("IW", "qif", 0.5893),
    ("WM", "im", 2.0879),
    ("cocoo", "CoCoO", 0),
    ("FMQ", "nno", -0.7375)
])
def test_convertBuffer_robustTo_BufferNameLowercase(buffer_cases_start, buffer_cases_end, final_value):
    try:
        pb.convert_buffer(0, buffer_cases_start, buffer_cases_end, 1473.15, 10) == pytest.approx(final_value)
    except Exception as exc:
        assert False, f"'{buffer_cases_start}' to '{buffer_cases_end}' raised an exception {exc}"

@pytest.fixture
def standard_comp_lowIron():
    return {
            'SiO2' : 44.71,
            'TiO2' : 0.13,
            'Al2O3': 1.33,
            'FeO'  : 8.06,
            'MnO'  : 0.13,
            'MgO'  : 38.73,
            'CaO'  : 3.17,
            'Na2O' : 0.13,
            'K2O'  : 0.006,
            'P2O5' : 0.019
        }

@pytest.fixture
def standard_comp_highIron():
    return {
            'SiO2' : 46.72,
            'TiO2' : 0.47,
            'Al2O3': 9.99,
            # 'FeO'  : 20.91,
            'FeO'  : 21.09,
            'MnO'  : 0.32,
            'MgO'  : 10.36,
            'CaO'  : 7.51,
            'Na2O' : 2.53,
            'K2O'  : 0.14,
            'P2O5' : 0.44
        } # 20.81, 0.72, 1.2gpa, 1406 celsius, fmq-4.68

@pytest.fixture
def standard_comp_fe2o3_lowIron():
    return {
            'SiO2' : 44.71,
            'TiO2' : 0.13,
            'Al2O3': 1.33,
            'Fe2O3': 0.521,
            'FeO'  : 7.887,
            'MnO'  : 0.13,
            'MgO'  : 38.73,
            'CaO'  : 3.17,
            'Na2O' : 0.13,
            'K2O'  : 0.006,
            'P2O5' : 0.019
        }

@pytest.fixture
def standard_comp_fe2o3_highIron():
    return {
            'SiO2' : 46.711,
            'TiO2' : 0.4699,
            'Al2O3': 9.9882,
            'Fe2O3': 4.4724,
            'FeO'  : 17.0621,
            'MnO'  : 0.3199,
            'MgO'  : 10.3581,
            'CaO'  : 7.5086,
            'Na2O' : 2.5295,
            'K2O'  : 0.14,
            'P2O5' : 0.4399
        } # 20.81, 0.72, 1.2gpa, 1406 celsius, fmq-4.68

def test_getIronOxide_with_standardInput_returns_ExpectedRatio(standard_comp_lowIron):
    assert pb.get_ironOxide(standard_comp_lowIron, -2, 1473.15, 10, buffer='FMQ')[0] == pytest.approx(0.02971, 0.001)

def test_getIronOxide_with_standardInput_returns_ExpectedComposition(standard_comp_lowIron):
    standard_normalised_comp_return = {            
                                        'SiO2' : 46.3482,
                                        'TiO2' : 0.135,
                                        'Al2O3': 1.379,
                                        'Fe2O3': 0.521,
                                        'FeO'  : 7.887,
                                        'MnO'  : 0.135,
                                        'MgO'  : 40.149,
                                        'CaO'  : 3.286,
                                        'Na2O' : 0.135,
                                        'K2O'  : 0.0062,
                                        'P2O5' : 0.0197}
    assert pb.get_ironOxide(standard_comp_lowIron, -2, 1473.15, 10, buffer='FMQ')[1] == pytest.approx(standard_normalised_comp_return, 0.005)

def test_getIronOxide_with_standardInput_returns_ExpectedNonNormalisedComposition(standard_comp_lowIron):
    standard_normalised_comp_return = {            
                                        'SiO2' : 44.71,
                                        'TiO2' : 0.13,
                                        'Al2O3': 1.33,
                                        'Fe2O3': 0.5209,
                                        'FeO'  : 7.8867,
                                        'MnO'  : 0.13,
                                        'MgO'  : 38.73,
                                        'CaO'  : 3.18,
                                        'Na2O' : 0.13,
                                        'K2O'  : 0.006,
                                        'P2O5' : 0.019}
    assert pb.get_ironOxide(standard_comp_lowIron, -2, 1473.15, 10, buffer='FMQ',
     normalised_comp=False)[1] == pytest.approx(standard_normalised_comp_return, 0.005)

def test_getIronOxide_with_highFeOInput_returns_ExpectedComposition(standard_comp_highIron):
    assert pb.get_ironOxide(standard_comp_highIron, -2, 1406, pb.core.gpa_to_bar(1.2), 
                    celsius=True, buffer='FMQ')[0] == pytest.approx(0.117923975, 0.001)

def test_getIronOxide_with_highFeOInput_returns_ExpectedNormalisedComposition(standard_comp_highIron, standard_comp_fe2o3_highIron):
    assert pb.get_ironOxide(standard_comp_highIron, -2, 1406, pb.core.gpa_to_bar(1.2), 
                    celsius=True, buffer='FMQ')[1] == pytest.approx(standard_comp_fe2o3_highIron, 0.001)

def test_getMeltfO2_with_lowFeOInput_returns_ExpectedRatio(standard_comp_fe2o3_lowIron):
    assert pb.get_meltfO2(standard_comp_fe2o3_lowIron, 1473.15, 10, buffer='FMQ')[0] == pytest.approx(-2, 0.001)