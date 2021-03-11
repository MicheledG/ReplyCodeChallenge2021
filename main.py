"""
Usage: python main.py <path_to>/<input_file_name>

Note: python3
"""
import json
import sys
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logging.basicConfig()

INPUT_FOLDER = 'input_file'
OUTPUT_FOLDER = 'output_file'


def main(argv):
    filename = argv[1]
    logger.info(f'reading input file {filename}')
    width, height, buildings, antennas, reward = read_input_file(filename)
    logger.info('input file successfully read')
    logger.info('computing scores of all antennas over all buildings')
    all_antennas_scores = dict()
    for antenna in antennas:
        antenna_scores = dict()
        for building in buildings:
            reachable_buildings = find_reachable_buildings(
                antenna_x=building[0],
                antenna_y=building[1],
                antenna_range=antenna[0],
                buildings=buildings
            )
            score = compute_score_per_all_reachable_buildings(
                antenna=antenna,
                antenna_x=building[0],
                antenna_y=building[1],
                reachable_buildings=reachable_buildings,
            )
            antenna_scores[building[4]] = score
        all_antennas_scores[antenna[2]] = antenna_scores
    logger.info(f'computed antennas scores:\n{json.dumps(all_antennas_scores, indent=2)}')
    create_output_file(filename, all_antennas_scores, buildings)
    logger.info('end')


def read_input_file(filename):
    """
    File structure:
    - first line: W(idth) H(eight)
    - second line: N(buildings) M(antennas) R(eward)
    - N lines - parameters of buildings: Bx By Bl Bc
    - M lines - parameters of antennas: Ar Ac
    :param filename:
    """
    with open(f'{INPUT_FOLDER}/{filename}', 'r') as input_file:
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


def compute_score_per_all_reachable_buildings(antenna, antenna_x, antenna_y, reachable_buildings):
    score = 0
    for building in reachable_buildings:
        building_score = compute_score_per_building_antenna(building, antenna, antenna_x, antenna_y)
        logger.debug(f'score for building:{building} and antenna: {antenna}')
        score += building_score
    logger.debug(f'all scores for antenna {antenna} placed in ({antenna_x, antenna_y})')
    return score


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


def find_reachable_buildings(antenna_x, antenna_y, antenna_range, buildings):
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
    logger.debug(f'found {len(buildings_in_range)} reachable buildings')
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


def create_output_file(filename, all_antennas_scores, buildings):
    antennas_chosen_building = list()
    buildings_availability = dict()
    for antenna_index in all_antennas_scores.keys():
        antenna_scores = all_antennas_scores[antenna_index]
        best_building_index = -1
        best_building_score = -1
        for building_index in antenna_scores.keys():
            building_score = antenna_scores[building_index]
            if building_score > best_building_score and buildings_availability.get(building_index, True):
                best_building_index = building_index
                best_building_score = building_score
        buildings_availability[best_building_index] = False
        antennas_chosen_building.append(best_building_index)
        logger.debug(f'antenna with index {antenna_index} placed on building {best_building_index}')
    number_of_antennas = len(antennas_chosen_building)
    with open(f'{OUTPUT_FOLDER}/{filename}', 'w') as output_file:
        output_file.write(f'{number_of_antennas}\n')
        for index, antenna_chosen_building in enumerate(antennas_chosen_building):
            building_index = antenna_chosen_building
            output_file.write(
                f'{index} {buildings[building_index][0]} {buildings[building_index][1]}\n'
            )


if __name__ == '__main__':
    try:
        main(sys.argv)
    except Exception as e:
        logger.exception('exception executing your script')
