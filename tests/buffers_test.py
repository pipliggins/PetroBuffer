# test_with_pytest.py

import petrobuffer as pb
import pytest

def test_calcBuffer_when_bufferUnrecognised_throwException():
    with pytest.raises(Exception):
        pb.buffers.calcBuffer('BIF', 1473.15, 1)

def test_calcBuffer_when_IW_highP_return_correctValue():
    assert pb.buffers.calcBuffer('IW', 1200, 110000) == pytest.approx(-12.019336)

def test_calcBuffer_when_NNO_highP_return_correctValue():
    assert pb.buffers.calcBuffer('NNO', 1200, 110000) == pytest.approx(-7.3025206)

def test_calcBuffer_when_FMQ_lowT_return_correctValue():
    assert pb.buffers.calcBuffer('FMQ', 800, 1) == pytest.approx(-22.725125)

@pytest.mark.parametrize("test_buffer, expected_value", [
    ("QIF", -17.108667),
    ("IW", -16.2055),
    ("WM", -14.327167),
    ("IM", -15.778833),
    ("CoCoO", -12.982167),
    ("FMQ", -12.178583),
    ("NNO", -11.415),
    ("MH", -6.8591667)
])
def test_calcBuffer_with_highT_returns_correctValue(test_buffer, expected_value):
    assert pb.buffers.calcBuffer(test_buffer, 1200, 1) == pytest.approx(expected_value)

@pytest.mark.parametrize("lowT_test_buffer, expected_value", [
    ("QIF", -28.368825),
    ("FMQ", -21.7951),
    ("MH", -16.645521)
])
def test_calcBuffer_with_lowT_returns_correctValue(lowT_test_buffer, expected_value):
    assert pb.buffers.calcBuffer(lowT_test_buffer, 823.15, 1) == pytest.approx(expected_value)


