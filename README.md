<p align="center">
                                   <b>**ATOM OVERLAP CHECKER README**</b>
</p>
If you are using this script please acknowledge me (Dr Owen Vickery) and cite the following DOI.

DOI: xxx

<p align="center">
                                   <b>**ATOM OVERLAP CHECKER, SCRIPT OVERVIEW**</b>
</p>

This script finds and atoms which are within a set distance and will move them until they are beyond the cutoff.

<p align="center">
                                   <b>**REQUIREMENTS**</b>
</p>
                                     
Software:

- Python v3 or higher

Non standard python modules:

- Numpy
- Scipy

Standard modules included in base python install (ubuntu 18):

- os
- sys
- itertools

<p align="center">
                                   <b>**FLAGS**</b>
</p>
                                        

REQUIRED
- -f      input    (pdb)
- -o      output    (pdb)
- -overlap    (float)

The script only works with pdb files.

using the flag -f for the input file -o for the output file.
The flag -cutoff overwrites the default 0.4 A cutoff.
<pre>
python check_atom_overlap.py -f input.pdb -o ouput.pdb -cutoff 0.5
</pre>

The above command will fix any overlaps within 0.5 A.
