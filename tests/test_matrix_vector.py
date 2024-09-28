import pytest
from math import isclose, sqrt

from project.matrix_vector import Matrix, Vector


class TestMatrixOperations:
    def test_matrix_init(self) -> None:
        # Valid matrix
        matrix = Matrix([[1, 2], [3, 4]])
        assert matrix.matrix == [[1, 2], [3, 4]]

        # Invalid matrix (jagged)
        with pytest.raises(TypeError):
            Matrix([[1, 2], [3]])

        # Empty matrix
        with pytest.raises(TypeError):
            Matrix([])

        # Matrix with empty row
        with pytest.raises(TypeError):
            Matrix([[], [1, 2]])

    def test_matrix_addition(self) -> None:
        matrix1 = Matrix([[1, 2], [3, 4]])
        matrix2 = Matrix([[5, 6], [7, 8]])
        result = matrix1 + matrix2
        assert result.matrix == [[6, 8], [10, 12]]

        # Matrices with different dimensions
        matrix1 = Matrix([[1, 2], [3, 4]])
        matrix2 = Matrix([[5, 6, 7], [8, 9, 10]])
        with pytest.raises(ValueError):
            matrix1 + matrix2

    def test_matrix_inplace_addition(self) -> None:
        matrix1 = Matrix([[1, 2], [3, 4]])
        matrix2 = Matrix([[5, 6], [7, 8]])
        matrix1 += matrix2
        assert matrix1.matrix == [[6, 8], [10, 12]]

    def test_matrix_multiplication(self) -> None:
        matrix1 = Matrix([[1, 2], [3, 4]])
        matrix2 = Matrix([[2, 0], [1, 2]])
        result = matrix1 * matrix2
        assert result.matrix == [[4, 4], [10, 8]]

        # Test with large matrices
        matrix1 = Matrix([[i for i in range(100)] for _ in range(100)])
        matrix2 = Matrix([[i for i in range(100)] for _ in range(100)])
        result = matrix1 * matrix2
        assert len(result.matrix) == 100
        assert len(result.matrix[0]) == 100

        # Matrices with incompatible dimensions for multiplication
        matrix1 = Matrix([[1, 2]])
        matrix2 = Matrix([[3, 4], [5, 6], [7, 8]])
        with pytest.raises(ValueError):
            matrix1 * matrix2

    def test_matrix_transpose(self) -> None:
        matrix = Matrix([[1, 2], [3, 4], [5, 6]])
        transposed = matrix.transpose()
        assert transposed.matrix == [[1, 3, 5], [2, 4, 6]]

    def test_singleton_matrix(self) -> None:
        # 1x1 matrix (singleton)
        matrix1 = Matrix([[3]])
        matrix2 = Matrix([[4]])

        result_add = matrix1 + matrix2
        result_mul = matrix1 * matrix2

        assert result_add.matrix == [[7]]
        assert result_mul.matrix == [[12]]


class TestVectorOperations:
    def test_vector_init(self) -> None:
        # Valid vector (1xN)
        vector = Vector([1, 2, 3])
        assert vector.vec == [1, 2, 3]

        # Empty vector
        with pytest.raises(TypeError):
            Vector([])

    def test_vector_length(self) -> None:
        vector = Vector([3, 4])
        assert vector.len() == 5

        # Very large vector
        large_vector = Vector([i for i in range(1000)])
        length = large_vector.len()
        expected_length = sqrt(sum(i**2 for i in range(1000)))
        assert isclose(length, expected_length)

    def test_vector_dot_product(self) -> None:
        vector1 = Vector([1, 2, 3])
        vector2 = Vector([4, 5, 6])
        dot = Vector.dot_product(vector1, vector2)
        assert dot == 32

        # Vectors with incompatible dimensions for dot product
        vector1 = Vector([1, 2])
        vector2 = Vector([3, 4, 5])
        with pytest.raises(ValueError):
            Vector.dot_product(vector1, vector2)

    def test_vector_angle(self) -> None:
        vector1 = Vector([1, 0])
        vector2 = Vector([0, 1])
        angle = Vector.angle_between_vectors(vector1, vector2)
        assert isclose(angle, 1.5708, abs_tol=1e-4)  # Pi/2 radians

    def test_singleton_vector(self) -> None:
        # 1x1 vector (a single value)
        vector = Vector([5])
        assert isclose(vector.len(), 5)
