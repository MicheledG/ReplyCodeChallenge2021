import os
import sys
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logging.basicConfig()


def main(argv):
    filename = argv[1]
    logger.info(f'reading input file {filename}')
    read_input_file(filename)
    logger.info('input file successfully read')


def read_input_file(filename):
    """
    File structure:
    - first line: W(idth) H(eight)
    - second line: N(buildings) M(antennas) R(eward)
    - N lines - parameters of buildings: Bx By Bl Bc
    - M lines - parameters of antennas: Ar Ac
    :param filename:
    """
    with open(filename, 'r') as input_file:
        # read grid dimensions
        [width, height] = [int(x) for x in input_file.readline().split(' ')]
        # read buildings and antennas numbers
        [buildings_number, antennas_number, reward] = [int(x) for x in input_file.readline().split(' ')]
        # read all buildings info
        buildings = list()
        for building_index in range(buildings_number):
            building_info = [int(x) for x in input_file.readline().split(' ')]
            buildings.append(building_info)
        if len(buildings) != buildings_number:
            Exception(
                f'error reading buildings: expected buildings {buildings_number}, extracted buildings {len(buildings)}'
            )
        # read all antennas info
        antennas = list()
        for antenna_index in range(antennas_number):
            antenna_info = [int(x) for x in input_file.readline().split(' ')]
            antennas.append(antenna_info)
        if len(antennas) != antennas_number:
            Exception(
                f'error reading antennas: expected antennas {antennas_number}, extracted antennas {len(antennas)}'
            )
        logger.info(
            f'Read info:\n'
            f'width: {width} - height: {height}\n'
            f'number of buildings: {buildings_number}\n'
            f'number of antennas: {antennas_number}\n'
            f'reward: {reward}'
        )
    return width, height, buildings, antennas, reward


if __name__ == '__main__':
    try:
        main(sys.argv)
    except Exception as e:
        logger.exception('exception executing your script')
