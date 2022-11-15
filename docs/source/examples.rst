Examples
========

Convert from one *f* O2 buffer to another
*****************************************
.. code-block:: python

    """This example demonstrates a simple case of converting the fO2 from one rock buffer (FMQ) to another (NNO).
    """

    import petrobuffer as pb

    current_dfo2 = -2
    current_buffer = 'FMQ'
    new_buffer = 'NNO'
    T = 1473 #Kelvin
    P = 10 #bar

    new_dfo2 = pb.convert_buffer(current_dfo2, current_buffer, new_buffer, T, P)