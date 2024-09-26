import math
from typing import List


class Matrix:
    """
    A class to represent a mathematical matrix and perform operations such as
    addition, multiplication, and transposition.

    Methods:
    -------
    `transpose() -> "Matrix"`:
        Returns the transpose of the matrix.

    `__add__(other_matrix: "Matrix") -> "Matrix"`:
        Performs matrix addition and returns a new matrix.

    `__mul__(other_matrix: "Matrix") -> "Matrix"`:
        Performs matrix multiplication and returns a new matrix.

    `is_matrix(list_of_lists: List[List[float]]) -> bool`:
        Static method to check if a 2D list is a valid matrix.

    `get() -> List[List[float]]`:
        Returns a list representation of the matrix.
    """

    def __init__(self, matrix: List[List[float]]):
        """
        Initializes a Matrix object.
        """

        if not Matrix.is_matrix(matrix):
            raise TypeError("Input must be a valid matrix.")

        self.matrix = matrix

    def __add__(self, other_matrix: "Matrix") -> "Matrix":
        """
        Adds two matrices and returns a new matrix.
        """

        count_rows = len(self.matrix)
        count_columns = len(self.matrix[0])
        add_matrix = [
            [0.0 for _ in range(count_columns)] for _ in range(count_rows)
        ]

        if count_rows != len(other_matrix.matrix) or count_columns != len(
            other_matrix.matrix[0]
        ):
            raise ValueError("Matrix 'other_matrix' has wrong dimension.")

        for row_num in range(count_rows):
            for column_num in range(count_columns):
                add_matrix[row_num][column_num] = (
                    self.matrix[row_num][column_num]
                    + other_matrix.matrix[row_num][column_num]
                )
        return Matrix(add_matrix)

    def transpose(self) -> "Matrix":
        """
        Transposes the matrix (flips rows and columns).
        """

        count_rows = len(self.matrix)
        count_columns = len(self.matrix[0])
        transposed = [
            [0.0 for _ in range(count_rows)] for _ in range(count_columns)
        ]

        for i in range(count_rows):
            for j in range(count_columns):
                transposed[j][i] = self.matrix[i][j]
        return Matrix(transposed)

    def __mul__(self, other_matrix: "Matrix") -> "Matrix":
        """
        Multiplies two matrices and returns a new matrix.
        """

        count_rows_left = len(self.matrix)
        count_rows_right = len(other_matrix.matrix)
        count_columns_left = len(self.matrix[0])
        count_columns_right = len(other_matrix.matrix[0])
        if count_columns_left != count_rows_right:
            raise ValueError(f"Matrices can't be multiplied.")
        multi_matrix = [
            [0.0 for _ in range(count_columns_right)]
            for _ in range(count_rows_left)
        ]
        for m in range(count_rows_left):
            for n in range(count_columns_right):
                for o in range(count_columns_left):
                    multi_matrix[m][n] += (
                        self.matrix[m][o] * other_matrix.matrix[o][n]
                    )
        return Matrix(multi_matrix)

    def get(self) -> List[List[float]]:
        """
        Returns a list representation of the matrix.
        """

        return self.matrix

    @staticmethod
    def is_matrix(list_of_lists: List[List[float]]) -> bool:
        """
        Checks if the input is a valid matrix (a 2D list with equal-length rows).
        """

        if not list_of_lists or not list_of_lists[0]:
            return False

        return all(len(row) == len(list_of_lists[0]) for row in list_of_lists)


class Vector:
    """
    A class to represent a vector.
    It provides functionality to vectors, such as calculating
    the vector's magnitude, dot product.

    Methods:
    -------
    `len() -> float`:
        Returns the magnitude (length) of the vector.

    `__add__(other_vector: "Vector") -> "Vector"`:
        Performs matrix addition and returns a new matrix.

    `dot_product(vec_1: "Vector", vec_2: "Vector") -> float`:
        Static method to calculate the dot product of two vectors.

    `angle_between_vectors(vec_1: "Vector", vec_2: "Vector") -> float`:
        Static method to calculate the angle (in radians) between two vectors.
    """

    def __init__(self, vector: List[float]) -> None:
        """
        Initializes a Vector object.
        """

        if len(vector) == 0:
            raise TypeError("Input must be a valid vector.")
        self.vec = vector

    def __add__(self, other_vector: "Vector") -> "Vector":
        """
        Adds two vectors and returns a new vector.
        """

        if len(self.vec) != len(other_vector.vec):
            raise ValueError("Vector 'other_vector' has wrong dimension.")
        new_vec = [0.0 for _ in range(len(self.vec))]
        for i in range(len(self.vec)):
            new_vec[i] = self.vec[i] + other_vector.vec[i]

        return Vector(new_vec)

    def len(self) -> float:
        """
        Returns the magnitude (length) of the vector.
        """

        return math.sqrt(Vector.dot_product(self, self))

    @staticmethod
    def dot_product(vec_1: "Vector", vec_2: "Vector") -> float:
        """
        Calculates the dot product of two vectors.
        """

        if len(vec_1.vec) != len(vec_2.vec):
            raise ValueError("Vectors have incompatible dimension.")
        result = 0.0
        for i in range(len(vec_1.vec)):
            result += vec_1.vec[i] * vec_2.vec[i]
        return result

    @staticmethod
    def angle_between_vectors(vec_1: "Vector", vec_2: "Vector") -> float:
        """
        Calculates the angle (in radians) between two vectors.
        """

        cos_a = Vector.dot_product(vec_1, vec_2) / (vec_1.len() * vec_2.len())
        return math.acos(cos_a)
