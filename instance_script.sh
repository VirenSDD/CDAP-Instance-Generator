#!/bin/bash

trucks=(8 9 10 11 12 15 20 50)
doors=(4 5 6 7 10 30)
slackness=(5 10 15 20 30)
densities=(25 35 50 75)

mkdir -p ./instances

for truck in "${trucks[@]}"
do
  for door in "${doors[@]}"
  do 
    for slack in "${slackness[@]}"
    do 
      for density in "${densities[@]}"
      do
        for instance in {1..5}
        do
          python instance_generator.py --suppliers $truck --customers $truck --in_doors $door --out_doors $door --pallets_min 10 --pallets_max 50 --doors_distance_min 8 --density $density --slackness $slack -o instances/${truck}x${door}x${slack}x${density}_${instance}.json
        done
      done
    done
  done
done
