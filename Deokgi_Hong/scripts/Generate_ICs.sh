#!/bin/bash

seed_list=()  
echo "  IC      Seed  " >> "IC_List.txt"
for sim in {2..32}
do
        while : 
        do
                seed=$((40 + RANDOM % 99999))
                # Check if the seed is already in the list
                if [[ ! " ${seed_list[@]} " =~ " ${seed} " ]]; then
                seed_list+=("$seed")  # Add the unique seed to the list
                break
                fi
        done

        echo "Generating ICs" ${sim}
        echo "Current Seed Number:" ${seed}
        printf "%6d %8d\n" "$sim" "$seed">> "IC_List.txt"	
        mkdir -p "$sim" 
        cd "$sim" || exit 1
        cp ../1/{geometry.xyz,hessian.hdf5,INPORB,start.py} .		
        sed -i "s/seed=6029/seed=${seed}/" start.py
        cd ..
        echo ""
done
