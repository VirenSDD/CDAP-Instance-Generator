# Instance Generator for the Cross Docking Assignment Problem (CDAP) <!-- omit in toc -->

In this directory we can find: 
- `instance_generator.py` Code that generates an instance given certain parameters in the command line.
- `instance_script.sh` Script that creates a directory `instances` and generates 4800 instances combining different values of trucks, doors, slackness and densities.


# Table of contents <!-- omit in toc -->
- [instance_generator.py](#instance_generatorpy)
  - [instance_generator.py help](#instance_generatorpy-help)
  - [Output Example](#output-example)
- [instance_script.sh](#instance_scriptsh)

## instance_generator.py

You need to install python and execute the following command in a terminal to know which parameters can be used:

```
python instance_generator.py --help
```

The output will be a JSON file with the instance generated, which contains the number of `customers`, an array of `suppliers`, where each one contains the deliveries to the corresponding clients, and a `crossdocking_center` object with the inbound and outbound doors with their corresponding capacities and the distances between doors.

This code was developed for Python 3.9.9.

### instance_generator.py help

```
usage: instance_generator.py [-h] --suppliers SUPPLIERS --in_doors IN_DOORS --out_doors OUT_DOORS --customers CUSTOMERS [--pallets_min PALLETS_MIN] [--pallets_max PALLETS_MAX]
                             [--in_doors_min IN_DOORS_MIN] [--in_doors_max IN_DOORS_MAX] [--out_doors_min OUT_DOORS_MIN] [--out_doors_max OUT_DOORS_MAX]
                             [--doors_distance_min DOORS_DISTANCE_MIN] [--density DENSITY] [--slackness SLACKNESS] -o OUTPUT

Instance generator for the Cross-Docking Assignment Problem

optional arguments:
  -h, --help            show this help message and exit
  --pallets_min PALLETS_MIN
                        Minimum number of pallets to be moved from supplier to client (default: 10)
  --pallets_max PALLETS_MAX
                        Maximum number of pallets to be moved from supplier to client (default: 50)
  --in_doors_min IN_DOORS_MIN
                        Minimum capacity of the inbound doors (default: 10)
  --in_doors_max IN_DOORS_MAX
                        Maximum capacity of the inbound doors (default: 80)
  --out_doors_min OUT_DOORS_MIN
                        Minimum capacity of the outbound doors (default: 10)
  --out_doors_max OUT_DOORS_MAX
                        Maximum capacity of the outbound doors (default: 80)
  --doors_distance_min DOORS_DISTANCE_MIN
                        Minimum distance from an inbound door to an outbound door (default: 8)
  --density DENSITY     Density of the matrix that contains the pallets from suppliers to clients (default: 25)
  --slackness SLACKNESS
                        Capacity slackness associated to the doors

required named arguments:
  --suppliers SUPPLIERS
                        Number of incoming trucks
  --in_doors IN_DOORS   Number of inbound doors
  --out_doors OUT_DOORS
                        Number of outbound doors
  --customers CUSTOMERS
                        Number of outgoing trucks
  -o OUTPUT, --output OUTPUT
                        Name of the output JSON file
```


### Output Example

Input

```
python instance_generator.py --suppliers 8 --in_doors 4 --out_doors 4 --customers 8 --pallets_min 10 --pallets_max 50 --in_doors_min 100 --in_doors_max 200 --out_doors_min 100 --out_doors_max 200 --doors_distance_min 8 --density 25 --slackness 5 -o exit.json
```

Output

```json
{
  "customers": 8,
  "suppliers": [
    {
      "id": 0,
      "deliveries": [
        {
          "id": 4,
          "pallets": 28
        }
      ]
    },
    {
      "id": 1,
      "deliveries": [
        {
          "id": 3,
          "pallets": 37
        }
      ]
    },
    {
      "id": 2,
      "deliveries": [
        {
          "id": 2,
          "pallets": 38
        },
        {
          "id": 4,
          "pallets": 50
        },
        {
          "id": 7,
          "pallets": 24
        }
      ]
    },
    {
      "id": 3,
      "deliveries": [
        {
          "id": 7,
          "pallets": 35
        },
        {
          "id": 0,
          "pallets": 23
        },
        {
          "id": 5,
          "pallets": 38
        },
        {
          "id": 1,
          "pallets": 20
        }
      ]
    },
    {
      "id": 4,
      "deliveries": [
        {
          "id": 6,
          "pallets": 29
        },
        {
          "id": 4,
          "pallets": 19
        }
      ]
    },
    {
      "id": 5,
      "deliveries": [
        {
          "id": 1,
          "pallets": 17
        },
        {
          "id": 6,
          "pallets": 28
        }
      ]
    },
    {
      "id": 6,
      "deliveries": [
        {
          "id": 0,
          "pallets": 42
        }
      ]
    },
    {
      "id": 7,
      "deliveries": [
        {
          "id": 5,
          "pallets": 28
        },
        {
          "id": 7,
          "pallets": 17
        }
      ]
    }
  ],
  "crossdocking_center": {
    "in_doors": [
      {
        "id": 0,
        "capacity": 124
      },
      {
        "id": 1,
        "capacity": 124
      },
      {
        "id": 2,
        "capacity": 124
      },
      {
        "id": 3,
        "capacity": 124
      }
    ],
    "out_doors": [
      {
        "id": 0,
        "capacity": 124
      },
      {
        "id": 1,
        "capacity": 124
      },
      {
        "id": 2,
        "capacity": 124
      },
      {
        "id": 3,
        "capacity": 124
      }
    ],
    "door_distances": [
      {
        "in_door": 0,
        "out_door": 0,
        "distance": 8
      },
      {
        "in_door": 0,
        "out_door": 1,
        "distance": 9
      },
      {
        "in_door": 0,
        "out_door": 2,
        "distance": 10
      },
      {
        "in_door": 0,
        "out_door": 3,
        "distance": 11
      },
      {
        "in_door": 1,
        "out_door": 0,
        "distance": 9
      },
      {
        "in_door": 1,
        "out_door": 1,
        "distance": 8
      },
      {
        "in_door": 1,
        "out_door": 2,
        "distance": 9
      },
      {
        "in_door": 1,
        "out_door": 3,
        "distance": 10
      },
      {
        "in_door": 2,
        "out_door": 0,
        "distance": 10
      },
      {
        "in_door": 2,
        "out_door": 1,
        "distance": 9
      },
      {
        "in_door": 2,
        "out_door": 2,
        "distance": 8
      },
      {
        "in_door": 2,
        "out_door": 3,
        "distance": 9
      },
      {
        "in_door": 3,
        "out_door": 0,
        "distance": 11
      },
      {
        "in_door": 3,
        "out_door": 1,
        "distance": 10
      },
      {
        "in_door": 3,
        "out_door": 2,
        "distance": 9
      },
      {
        "in_door": 3,
        "out_door": 3,
        "distance": 8
      }
    ]
  }
}
```

## instance_script.sh

Script that generates every combination of trucks, doors, slackness and densities of the following sets, creating 5 instances per combination:

- Trucks: {8, 9, 10, 11, 12, 15, 20, 50}
- Doors: {4, 5, 6, 7, 10, 30}
- Slackness: {5, 10, 15, 20, 30}
- Densities: {25, 35, 50, 75}

The script will create a directory (if it does not exist) named `instances`, where the JSON files of each instance will be stored. The naming consists of 5 digits and has the following format: `TrucksxDoorsxSlackxDensity_Instance`.

To execute it, be sure that you have execution permissions on the file (`chmod +x instance_script.sh`) and simply type:

```
./instance_script.sh
```

The instances will be generated automatically.