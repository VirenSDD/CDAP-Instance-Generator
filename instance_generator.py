#!/usr/bin/env python

__author__ = "Viren S. Dhanwani"

import argparse
import json
import random
import numpy as np


def check_JSON_format(filename):
    '''
    Checks whether the given filename is in JSON format (.json)

    Parameters:
      filename (str): Name of the file that must be in JSON format
    '''

    if '.' not in filename or filename.split('.')[-1] != 'json':
        raise ValueError('JSON file must be specified')


def add_arguments():
    '''
    Generates a dictionary with an instance of a Cross Docking Assignment Problem specified in the command line

    Returns:
      dict: Arguments with the key and its corresponding values
    '''

    parser = argparse.ArgumentParser(
        description='Instance generator for the Cross-Docking Assignment Problem')
    requiredNamed = parser.add_argument_group('required named arguments')

    requiredNamed.add_argument(
        '--suppliers', nargs=1, type=int, help='Number of incoming trucks', required=True)
    requiredNamed.add_argument(
        '--in_doors', nargs=1, type=int, help='Number of inbound doors', required=True)
    requiredNamed.add_argument(
        '--out_doors', nargs=1, type=int, help='Number of outbound doors', required=True)
    requiredNamed.add_argument(
        '--customers', nargs=1, type=int, help='Number of outgoing trucks', required=True)
    parser.add_argument('--pallets_min', nargs=1, type=int,
                        help='Minimum number of pallets to be moved from supplier to client (default: 10)', default=[10])
    parser.add_argument('--pallets_max', nargs=1, type=int,
                        help='Maximum number of pallets to be moved from supplier to client (default: 50)', default=[50])
    parser.add_argument('--in_doors_min', nargs=1, type=int,
                        help='Minimum capacity of the inbound doors (default: 10)', default=[10])
    parser.add_argument('--in_doors_max', nargs=1, type=int,
                        help='Maximum capacity of the inbound doors (default: 80)', default=[80])
    parser.add_argument('--out_doors_min', nargs=1, type=int,
                        help='Minimum capacity of the outbound doors (default: 10)', default=[10])
    parser.add_argument('--out_doors_max', nargs=1, type=int,
                        help='Maximum capacity of the outbound doors (default: 80)', default=[80])
    parser.add_argument('--doors_distance_min', nargs=1, type=int,
                        help='Minimum distance from an inbound door to an outbound door (default: 8)', default=[8])
    parser.add_argument('--density', nargs=1, type=float,
                        help='Density of the matrix that contains the pallets from suppliers to clients (default: 25)', default=[25])
    parser.add_argument('--slackness', nargs=1, type=float,
                        help='Capacity slackness associated to the doors')
    requiredNamed.add_argument('-o', '--output', nargs=1, type=str,
                               help='Name of the output JSON file', required=True)

    return parser.parse_args().__dict__


def generate_doors(number, minimum, maximum):
    id = 0
    result = []

    for i in range(number):
        result.append(
            dict([('id', id), ('capacity', random.randint(minimum, maximum))]))
        id += 1

    return result


def sum_suppliers_capacities(suppliers):
    result = 0
    for supplier in suppliers:
        for delivery in supplier['deliveries']:
            result += delivery['pallets']

    return result


def generate_doors_with_slackness(number, capacity, slackness):
    id = 0
    result = []

    final_capacity = round(capacity * (1 + slackness))

    for i in range(number):
        result.append(dict([('id', id), ('capacity', final_capacity)]))
        id += 1

    return result


def generate_distances(in_doors, out_doors, minimum):
    result = []
    for i in range(in_doors):
        for j in range(out_doors):
            result.append(
                dict([('in_door', i), ('out_door', j), ('distance', abs(j - i) + minimum), ]))

    return result


def element_in_list(element, list):
    for i in list:
        if i['id'] == element:
            return True

    return False


def generate_suppliers(suppliers, clients, minimum, maximum, density):
    result = []
    filled = 0
    max_elements = suppliers * clients * density / 100
    # Randomizing the list of clients
    clients_random = list(np.random.permutation(np.arange(0, clients)))
    for i in range(suppliers):
        result.append(dict([('id', i), ('deliveries', [])]))
        if len(clients_random) == 0:
            clients_random.append(random.randint(0, clients - 1))
        assigned_client = clients_random.pop()
        num_pallets = random.randint(minimum, maximum)
        if num_pallets > 0:
            result[i]['deliveries'].append(
                dict([('id', int(assigned_client)), ('pallets', num_pallets)]))
            filled += 1
            if (filled > max_elements):
                raise ValueError(
                    'Density must be higher to generate the instance')
    # Assigning remaining clients
    for i in clients_random:
        assigned_supplier = random.randint(0, suppliers - 1)
        num_pallets = random.randint(minimum, maximum)
        if num_pallets > 0:
            result[assigned_supplier]['deliveries'].append(
                dict([('id', int(i)), ('pallets', num_pallets)]))
            filled += 1
            if (filled > max_elements):
                raise ValueError(
                    'Density must be higher to generate the instance')
    # Filling the rest of the matrix according to the density
    while (filled < max_elements):
        assigned_supplier = random.randint(0, suppliers - 1)
        assigned_client = random.randint(0, clients - 1)
        num_pallets = random.randint(minimum, maximum)
        supplier_deliveries = result[assigned_supplier]['deliveries']
        if num_pallets > 0 and not element_in_list(assigned_client, supplier_deliveries):
            supplier_deliveries.append(
                dict([('id', assigned_client), ('pallets', num_pallets)]))
            filled += 1

    return result


def main():
    args = add_arguments()
    output_file = args['output'][0]
    check_JSON_format(output_file)
    data = {}
    instance = {}

    for k in args:
        if k != 'output' and args[k] is not None and 'min' not in k and 'max' not in k:
            if args[k][0] < 0:
                raise ValueError('There cannot be negative parameters')
            data[k] = args[k][0]

    # Error handling
    if data['density'] > 100:
        raise ValueError('Density cannot be higher than 100')

    in_doors_number = data['in_doors']
    out_doors_number = data['out_doors']

    instance['customers'] = data['customers']
    door_distances = generate_distances(
        in_doors_number, out_doors_number, args['doors_distance_min'][0])
    instance['suppliers'] = generate_suppliers(
        data['suppliers'], data['customers'], args['pallets_min'][0], args['pallets_max'][0], data['density'])

    if 'slackness' in data:
        capacity = sum_suppliers_capacities(
            instance['suppliers']) / in_doors_number
        data['in_doors'] = generate_doors_with_slackness(
            in_doors_number, capacity, data['slackness'] / 100)
        data['out_doors'] = generate_doors_with_slackness(
            out_doors_number, capacity, data['slackness'] / 100)
    else:
        data['in_doors'] = generate_doors(
            in_doors_number, args['in_doors_min'][0], args['in_doors_max'][0])
        data['out_doors'] = generate_doors(
            out_doors_number, args['out_doors_min'][0], args['out_doors_max'][0])

    instance['crossdocking_center'] = {'in_doors': data['in_doors'],
                                       'out_doors': data['out_doors'], 'door_distances': door_distances}

    with open(output_file, 'w') as outfile:
        json.dump(instance, outfile, indent=2)


if __name__ == '__main__':
    try:
        main()
    except ValueError as e:
        print('[Value Error]: ' + str(e))

# Example:
# python instance_generator.py --suppliers 8 --in_doors 4 --out_doors 4 --customers 8 --pallets_min 10 --pallets_max 50 --in_doors_min 100 --in_doors_max 200 --out_doors_min 100 --out_doors_max 200 --doors_distance_min 8 --density 25 --slackness 5 -o exit.json
