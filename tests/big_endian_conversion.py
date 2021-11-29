from typing import NamedTuple
import pytest
from starkware.starknet.testing.contract import StarknetContract
from starkware.starknet.testing.starknet import Starknet

class TestsDeps(NamedTuple):
    starknet: Starknet
    converter: StarknetContract


def byteswap_64bit_word(word: int):
    swapped_bytes = ((word & 0xFF00FF00FF00FF00) >> 8) | ((word & 0x00FF00FF00FF00FF) << 8)
    swapped_2byte_pair = ((swapped_bytes & 0xFFFF0000FFFF0000) >> 16) | ((swapped_bytes & 0x0000FFFF0000FFFF) << 16)
    swapped_4byte_pair = (swapped_2byte_pair >> 32) | ((swapped_2byte_pair << 32) % 2**64)

    # Some Shiva-inspired code here
    if (word >= 2**56): return swapped_4byte_pair
    if (word >= 2**48): return swapped_4byte_pair >> 8
    if (word >= 2**40): return swapped_4byte_pair >> 16
    if (word >= 2**32): return swapped_4byte_pair >> 24
    if (word >= 2**24): return swapped_4byte_pair >> 32
    if (word >= 2**16): return swapped_4byte_pair >> 40
    if (word >= 2**8): return swapped_4byte_pair >> 48
    return swapped_4byte_pair >> 56

async def setup():
    starknet = await Starknet.empty()
    converter = await starknet.deploy("contracts/starknet/test/TestToBigEndian.cairo", cairo_path=["contracts"])
    return TestsDeps(starknet=starknet, converter=converter)

# @pytest.mark.asyncio
# async def test_swap_endianness_full_word():
#     starknet, converter = await setup()

#     input_str = 'f90218a089abcdef'
#     print("Input hex: ", input_str)

#     input_as_big_endian = int.from_bytes(bytearray.fromhex(input_str), 'big')
#     print("input as big endian:", input_as_big_endian, hex(input_as_big_endian))

#     input_as_little_endian = int.from_bytes(bytearray.fromhex(input_str), 'little')
#     print("input as little endian:", input_as_little_endian, hex(input_as_little_endian))

#     big_to_little_python = byteswap_64bit_word(input_as_big_endian)
#     print("big to little python:", big_to_little_python, hex(big_to_little_python))

#     assert big_to_little_python == input_as_little_endian

#     convert_call = await converter.test_to_big_endian(input_as_big_endian).call()
#     big_to_little_cairo = convert_call.result.res

#     print("big to little cairo:", big_to_little_cairo, hex(big_to_little_cairo))

#     assert big_to_little_python == big_to_little_cairo

#     little_to_big_python = byteswap_64bit_word(input_as_little_endian)
#     print("little to big python:", little_to_big_python, hex(little_to_big_python))

#     assert little_to_big_python == input_as_big_endian

#     convert_call = await converter.test_to_big_endian(input_as_little_endian).call()
#     little_to_big_cairo = convert_call.result.res

#     print("little to big cairo:", little_to_big_cairo, hex(little_to_big_cairo))

#     assert little_to_big_python == little_to_big_cairo


@pytest.mark.asyncio
async def test_swap_endianness_small_words():
    starknet, converter = await setup()
    print("\n")

    for i in range(8):
        input_str = 'f90218a089abcdef'[0:16-(i*2)]
        print("Input hex: ", input_str)
        input_as_big_endian = int.from_bytes(bytearray.fromhex(input_str), 'big')
        input_as_little_endian = int.from_bytes(bytearray.fromhex(input_str), 'little')
        big_to_little_python = byteswap_64bit_word(input_as_big_endian)
        assert big_to_little_python == input_as_little_endian
        convert_call = await converter.test_to_big_endian(input_as_big_endian).call()
        big_to_little_cairo = convert_call.result.res
        # print("python little:", hex(big_to_little_python))
        # print("cairo little:", hex(big_to_little_cairo))
        assert big_to_little_python == big_to_little_cairo

# @pytest.mark.asyncio
# async def test_swap_endianness_small_word():
#     starknet, converter = await setup()

#     input_str = 'f90218'
#     print("Input hex: ", input_str)

#     input_as_big_endian = int.from_bytes(bytearray.fromhex(input_str), 'big')
#     print("input as big endian:", input_as_big_endian, hex(input_as_big_endian))

#     input_as_little_endian = int.from_bytes(bytearray.fromhex(input_str), 'little')
#     print("input as little endian:", input_as_little_endian, hex(input_as_little_endian))

#     big_to_little_python = byteswap_64bit_word(input_as_big_endian)
#     print("big to little python:", big_to_little_python, hex(big_to_little_python))

#     assert big_to_little_python == input_as_little_endian

#     convert_call = await converter.test_to_big_endian(input_as_big_endian).call()
#     big_to_little_cairo = convert_call.result.res

#     print("big to little cairo:", big_to_little_cairo, hex(big_to_little_cairo))

#     assert big_to_little_python == big_to_little_cairo

#     little_to_big_python = byteswap_64bit_word(input_as_little_endian)
#     print("little to big python:", little_to_big_python, hex(little_to_big_python))

#     assert little_to_big_python == input_as_big_endian

#     convert_call = await converter.test_to_big_endian(input_as_little_endian).call()
#     little_to_big_cairo = convert_call.result.res

#     print("little to big cairo:", little_to_big_cairo, hex(little_to_big_cairo))

#     assert little_to_big_python == little_to_big_cairo

# @pytest.mark.asyncio
# async def test_to_little_endian():
#     starknet, converter = await setup()

#     input_str = 'f90218'#a089abcdef'
#     # print("Input hex: ", input_str)

#     big_endian_input = int.from_bytes(bytearray.fromhex(input_str), 'big')

#     little_swapped = byteswap_64bit_word(big_endian_input)

#     convert_call = await converter.test_to_big_endian(big_endian_input).call()
#     output = convert_call.result.res

#     assert output == little_swapped

@pytest.mark.asyncio
async def test_revert_word_size_above_64bit():
    starknet, converter = await setup()
    with pytest.raises(Exception):
        max_word = 2 ** 64 + 1
        await converter.test_to_big_endian(max_word).call()