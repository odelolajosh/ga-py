import pytest
from genetic_algorithm.chromosome_decoder import BinaryChromosomeDecoder, DenaryChromosomeDecoder

@pytest.mark.parametrize("x,value", [
    ([[1, 0, 0, 1, 0, 1], [1, 1, 1, 0, 1, 0]], [4.35, 3.60]),
    ([[0, 1, 1, 1, 0, 0], [0, 1, 0, 1, 0, 1]], [3.78, 0.67]),
    ([[0, 1, 0, 0, 1, 1], [1, 0, 1, 0, 0, 1]], [3.21, 2.25])
])
def test_binary_chromosome_encoding_with_6_bytes(x, value):
    bin_encoding = BinaryChromosomeDecoder(
        number_of_bytes=6,
        number_of_decision_variables=2,
        lower_bounds=[2, -1],
        upper_bounds=[6, 4]
    )
    decoded_value = bin_encoding.decode(x)
    assert [round(x, 2) for x in decoded_value] == value
    assert bin_encoding.encode(decoded_value) == x


@pytest.mark.parametrize("x,value", [
    ([[1, 0, 1, 1, 0], [0, 1, 0, 1, 0], [1, 1, 0, 1, 0]], [2.84, 2.97, 2.35]),
])
def test_binary_chromosome_encoding_with_5_bytes(x, value):
    bin_encoding = BinaryChromosomeDecoder(
        number_of_bytes=5,
        number_of_decision_variables=3,
        lower_bounds=[0, 2, -1],
        upper_bounds=[4, 5, 3]
    )
    decoded_value = bin_encoding.decode(x)
    assert [round(x, 2) for x in decoded_value] == value
    assert bin_encoding.encode(decoded_value) == x

@pytest.mark.parametrize("x,value", [
    ([[0, 2, 4, 5, 5], [0, 3, 2, 0, 1], [0, 1, 3, 0, 0]], [2.455, 3.201, 1.300]),
    ([[0, 2, 4, 5, 5], [0, 3, 2, 0, 1], [1, 1, 5, 2, 7]], [2.455, 3.201, -1.527]),
    # when a given value exceeds the upper boundary, it should encode to the upper bound
    ([[0, 0, 9, 9, 0], [0, 5, 0, 0, 1], [0, 4, 3, 1, 9]], [0.990, 5.000, 4.319]),
    # when a given value is out by the lower boundary, it should encode to the lower bound
    ([[0, 0, 9, 9, 0], [0, 5, 0, 0, 1], [1, 4, 3, 1, 9]], [0.990, 5.000, -2.000]),
])
def test_denary_chromosome_decoding_with_1_integer_3_dp(x, value):
    dec_encoding = DenaryChromosomeDecoder(
        number_of_bytes=4,
        number_of_decision_variables=3,
        lower_bounds=[0, 1, -2],
        upper_bounds=[3, 5, 6],
        dp=3
    )
    decoded_value = dec_encoding.decode(x)
    assert [round(x, 3) for x in decoded_value] == value


@pytest.mark.parametrize("x,value", [
    ([3.4323, 11.2343], [[0, 0, 3, 4, 3, 2, 3], [0, 1, 1, 2, 3, 4, 3]])
])
def test_denary_chromosome_decoding_with_1_integer_3_dp(x, value):
    dec_encoding = DenaryChromosomeDecoder(
        number_of_bytes=6,
        number_of_decision_variables=2,
        lower_bounds=[-11, 8],
        upper_bounds=[5, 23],
        dp=4
    )
    assert dec_encoding.encode(x) == value
