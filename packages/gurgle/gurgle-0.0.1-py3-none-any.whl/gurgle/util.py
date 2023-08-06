import numpy as np


def row_euclidean_distance(A, B):
    """Euclidean distance between aligned rows of A. An array of length len(A) (==len(B)).

    >>> import numpy as np
    >>> A = np.arange(5 * 16).reshape((5, 16))
    >>> B = 1 + A

    >>> assert all(row_euclidean_distance(A, A) == np.zeros(5))
    >>> assert all(row_euclidean_distance(A, B) == np.array([4., 4., 4., 4., 4.]))

    Note: Not to be confused with the matrix of distances of all pairs of rows. Here, equivalent to the latter diagnonal (see below).

    ```
    from  sklearn.metrics.pairwise import euclidean_distances
    A = np.random.rand(5, 7)
    B = np.random.rand(5, 7)
    assert all(np.diag(euclidean_distances(A, B)) == row_euclidean_distance(A, B))
    ```

    """
    return np.sqrt(((A - B) ** 2).sum(axis=1))
