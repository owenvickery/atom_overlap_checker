#!/usr/bin/env python3

import os, sys
import numpy as np
import itertools
from scipy.spatial import cKDTree
import argparse

parser = argparse.ArgumentParser(description='checks for atom overlap', prog='CG2AT', epilog='Enjoy the program and best of luck!\n', allow_abbrev=True)

parser.add_argument('-f', help='pdb file',metavar='input.pdb',type=str)
parser.add_argument('-o', help='output file',metavar='checked.pdb',type=str)
parser.add_argument('-overlap', help='overlap cutoff default = 0.4 A',metavar='0.4',type=float, default=0.4)


args = parser.parse_args()
options = vars(args)


pdbline = "ATOM  %5d %4s %4s%1s%4d    %8.3f%8.3f%8.3f%6.2f%6.2f"

def read_in_merged_pdbs(merge, merge_coords, location):
    header=''
    if os.path.exists(location):
    #### opens pdb files and writes straight to merged_cg2at pdb
        with open(location, 'r') as pdb_input:
            for line in pdb_input.readlines():
                if line.startswith('ATOM'):
                    line_sep = pdbatom(line)
                    merge.append(line_sep)
                    merge_coords.append([line_sep['x'],line_sep['y'],line_sep['z']])
                if line.startswith('CRYST'):
                    header=line
        return merge, merge_coords, header
    else:
        sys.exit('cannot find minimised residue: \n'+ location) 

def check_atom_overlap(coordinates):
#### creates tree of atom coordinates
    tree = cKDTree(coordinates)
    overlapped = overlapping_atoms(tree)
    if len(overlapped)>15:
        print('you have '+str(len(overlapped))+' overlapping atoms, this script will probably struggle!\n')  
    print(overlapped)
#### runs through overlapping atoms and moves atom in a random diection until it is no longer overlapping
    while len(overlapped) > 0:
        for ndx in overlapped:
            xyz_check = np.array([coordinates[ndx[0]][0]+np.random.uniform(-0.2, 0.2), coordinates[ndx[0]][1]+np.random.uniform(-0.2, 0.2),coordinates[ndx[0]][2]+np.random.uniform(-0.2, 0.2)])
            while len(tree.query_ball_point(xyz_check, r=args.overlap)) > 1:
                xyz_check = np.array([coordinates[ndx[0]][0]+np.random.uniform(-0.2, 0.2), coordinates[ndx[0]][1]+np.random.uniform(-0.2, 0.2),coordinates[ndx[0]][2]+np.random.uniform(-0.2, 0.2)])
            coordinates[ndx[0]]=xyz_check
            tree = cKDTree(coordinates)
        overlapped = overlapping_atoms(tree)
    return coordinates

def overlapping_atoms(tree):
    overlapped_ndx = tree.query_ball_tree(tree, r=args.overlap)
    overlapped_cut = [ndx for ndx in overlapped_ndx if len(ndx) >1]
    overlapped_cut.sort()
    overlapped=list(overlapped_cut for overlapped_cut,_ in itertools.groupby(overlapped_cut))
    print('There are: '+str(len(overlapped))+' overlapping atoms')
    return overlapped

def create_pdb(file_name, box_vec):
    pdb_output = open(file_name, 'w')
    pdb_output.write('TITLE     GENERATED BY CG2AT\nREMARK    Please don\'t explode\nREMARK    Good luck\n'+box_vec+'MODEL        1\n')
    return pdb_output

def pdbatom(line):
### get information from pdb file
### atom number, atom name, residue name,chain, resid,  x, y, z, backbone (for fragment), connect(for fragment)
    try:
        return dict([('atom_number',int(line[7:11].replace(" ", ""))),('atom_name',str(line[12:16]).replace(" ", "")),('residue_name',str(line[17:21]).replace(" ", "")),\
            ('chain',line[21]),('residue_id',int(line[22:26])), ('x',float(line[30:38])),('y',float(line[38:46])),('z',float(line[46:54]))])
    except:
        sys.exit('\npdb line is wrong:\t'+line)


lines, coords, header = read_in_merged_pdbs([], [], args.f)
updated_coords = check_atom_overlap(coords)
pdb_output=create_pdb(args.o, header) 

for line_val, line in enumerate(lines):
    pdb_output.write(pdbline%((int(line['atom_number']), line['atom_name'], line['residue_name'],' ',line['residue_id'],\
                    updated_coords[line_val][0],updated_coords[line_val][1],updated_coords[line_val][2],1,0))+'\n')

