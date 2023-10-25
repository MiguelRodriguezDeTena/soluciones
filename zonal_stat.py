import numpy as np


def read_data(fname: str, tipo: type) -> np.ndarray:
    """
    Returns an np.ndarray object from a .txt file, with the type provided 
    on the second argument.
    Examples:
    --------
    >>> read_data("test.txt",int)
    array([0, 1, 2, 3, 4, 5])
    >>> read_data("test2.txt",int)
    array([[ 0,  1,  2,  3,  4,  5],
           [ 6,  7,  8,  9, 10, 11]])
    >>> read_data("test.txt",float)
    array([0., 1., 2., 3., 4., 5.])
    """
    return np.loadtxt(fname, dtype = tipo)



def set_of_areas(zonas: np.ndarray)-> set[int]:
    """
    Returns a set of unique values if the array was made of integers, otherwise
    returns an TypeError.

    Examples:
    --------
    >>> set_of_areas(np.arange(10).reshape(5, 2))
    {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
    >>> set_of_areas(np.zeros(10, dtype=np.int_).reshape(5, 2))
    {0}
    >>> set_of_areas(np.array([2, 3, 4, 2, 3, 4], dtype=np.int_).reshape(3, 2))
    {2, 3, 4}
    >>> set_of_areas(np.zeros(3, dtype=np.float_))
    Traceback (most recent call last):
        ...
    TypeError: The elements type must be int, not float64
    """
    # Escribe aquí tu código
    # No olvides documentar la función
    if not np.issubdtype(zonas.dtype,np.integer):
        raise TypeError(f"The elements type must be int, not {zonas.dtype}")
    else:    
        return set(zonas.flatten())



def mean_areas(zonas: np.ndarray, temperaturas: np.ndarray) -> np.ndarray:
    """ Checks if zones and temperatures arrays have the same shape, then calculate the mean
    temperature for each zone and returns an array with the same shape with the zones replaced
    with the mean temperature value.

    Examples:
    --------
    >>> mean_areas(np.array([[0,0,0,0],[1,1,1,1],[2,2,2,2]]),np.arange(12).reshape(3, 4))
    array([[1, 1, 1, 1],
           [5, 5, 5, 5],
           [9, 9, 9, 9]])

    >>> mean_areas(np.array([[0,0,0,0],[1,1,1,1],[1,1,1,1],[2,2,2,2]]),np.arange(12).reshape(3, 4))
    Traceback (most recent call last):
        ...
    IndexError: Arrays don't have the same shape
    """
    if zonas.shape != temperaturas.shape:
        raise IndexError("Arrays don't have the same shape")
    else:   
        unique_zonas = set_of_areas(zonas)
        for i in unique_zonas:
            mask = (zonas == i)
            my_mean = round(np.mean(temperaturas[mask]),1)
            temperaturas[mask] = my_mean

    return temperaturas      




# ------------ test  --------#
import doctest

def test_doc()-> None:
    """
    The following instructions are to execute the tests of same functions
    If any test is fail, we will receive the notice when executing
    :return: None
    """
    doctest.run_docstring_examples(read_data, globals(), verbose=True)  # vemos los resultados de los test que fallan
    doctest.run_docstring_examples(set_of_areas, globals(), verbose=True)  # vemos los resultados de los test que fallan
    doctest.run_docstring_examples(mean_areas, globals(), verbose=True)  # vemos los resultados de los test que fallan


if __name__ == "__main__":
    test_doc()   # executing tests
    zonas = read_data("datos/zonas.txt",int)
    temperaturas = read_data("datos/valores.txt",float)
    print(set_of_areas(zonas))
    print(mean_areas(zonas,temperaturas))
