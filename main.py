"""
Usage: python main.py <path_to>/<input_file_name>

Note: python3
"""

import sys
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logging.basicConfig()


def main(argv):
    filename = argv[1]
    logger.info(f'reading input file {filename}')
    width, height, buildings, antennas, reward = read_input_file(filename)
    logger.info('input file successfully read')
    compute_score_per_building_antenna()


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
            building_info.append(building_index)
            buildings.append(building_info)
        if len(buildings) != buildings_number:
            Exception(
                f'error reading buildings: expected buildings {buildings_number}, extracted buildings {len(buildings)}'
            )
        # read all antennas info
        antennas = list()
        for antenna_index in range(antennas_number):
            antenna_info = [int(x) for x in input_file.readline().split(' ')]
            antenna_info.append(antenna_index)
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


def compute_score_per_building_antenna(building, antenna, antenna_x, antenna_y):
    logger.debug(
        f'input to compute the score:\n'
        f'building: {building}\n'
        f'antenna: {antenna}\n'
        f'antenna position: x={antenna_x}, y={antenna_y}'
    )
    score = building[3] * antenna[1] - building[2] * manhattan_distance(
        building[0],
        building[1],
        antenna_x,
        antenna_y
    )
    logger.debug(f'computed score: {score}')
    return score


def reachable_buildings(antenna_x, antenna_y, antenna_range, buildings):
    """
    Given a point in grid (x,y) and its range,
    return the list of buildings reachable by that point

    :param antenna_x:
    :param antenna_y:
    :param antenna_range:
    :param buildings:
    """
    logger.debug(f'provided antenna info: x={antenna_x}, y={antenna_y}, range={antenna_range}')
    buildings_in_range = list()
    for building in buildings:
        logger.debug(f'building position: x={building[0]}, y={building[1]}')
        distance = manhattan_distance(antenna_x, antenna_y, building[0], building[1])
        if distance <= antenna_range:
            buildings_in_range.append(building)
            logger.debug('building is reachable')
        else:
            logger.debug('building is not reachable by the provided point with the provide range')
    logger.info(f'found {len(buildings_in_range)} reachable buildings')
    return buildings_in_range


def manhattan_distance(ix, iy, jx, jy):
    """
    Compute manhattan distance between i and j point

    :param ix:
    :param iy:
    :param jx:
    :param jy:
    """
    x_distance = abs(ix - jx)
    y_distance = abs(iy - jy)
    distance = x_distance + y_distance
    logger.debug(f'i point: x={ix}, y={iy}; j point: x={jx}, y={jy}; distance={distance}')
    return distance


def sort_antennas_by_connection_speed(antennas):
    logger.debug(f'original list of antennas:\n{antennas}')
    sorted_antennas = sorted(
        antennas, key=lambda antenna: antenna[1], reverse=True  # antenna[1] is the antenna connection speed parameter
    )
    logger.debug(f'sorted antennas by connection speed:\n{sorted_antennas}')
    return sorted_antennas


def sort_antennas_by_range(antennas):
    logger.debug(f'original list of antennas:\n{antennas}')
    sorted_antennas = sorted(
        antennas, key=lambda antenna: antenna[0], reverse=True  # antenna[0] is the antenna range parameter
    )
    logger.debug(f'sorted antennas by range speed:\n{sorted_antennas}')
    return sorted_antennas


if __name__ == '__main__':
    try:
        main(sys.argv)
    except Exception as e:
        logger.exception('exception executing your script')
