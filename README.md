# ifs-perturb

Create an ensemble of IFS initial conditions from an existing initial state by chaning
a random mode of a variable at a certain level with a certain amount. By default the temperature for a random mode at level 30 is changed by 0.1K.

``` bash
$ ./ifs_perturb.py --help                              
usage: ifs_perturb.py [-h] -i INITIALSTATE -e EXPERIMENT -o
                           OUTPUTDIR [-m MEMBERS] [-s SEED] [-f]
                           [-v VARIABLE] [-l LEVEL] [-p PERTURBATION]

optional arguments:
  -h, --help            show this help message and exit
  -i INITIALSTATE, --initialstate INITIALSTATE
                        Directory containing initial state to perturb
  -e EXPERIMENT, --experiment EXPERIMENT
                        Experiment name of initial state to perturb
  -o OUTPUTDIR, --outputdir OUTPUTDIR
                        Output directory
  -m MEMBERS, --members MEMBERS
                        Number of initial states to create
  -s SEED, --seed SEED  Random seed
  -f, --force           force overwriting existing files
  -v VARIABLE, --variable VARIABLE
                        variable name
  -l LEVEL, --level LEVEL
                        model level
  -p PERTURBATION, --perturbation PERTURBATION
                        perturbation amount
```

## example
The following example provides more insight in how to use the script. First let's find out what are directory structure looks like (where path in the following example is used just as a substitute for the actual basepath to the init directory):
``` bash
[]$ find {path}/init
{path}/init
{path}/init/ECE3
{path}/init/ECE3/ICMGGECE3INIT
{path}/init/ECE3/ICMSHECE3INIT
{path}/init/ECE3/ICMGGECE3INIUA
```
Okay, so the `{path}/init` directory contains initial conditions for an ec-earth experiment called `ECE3`. Let's create a perturbed ensemble from this initial conditions with 10 members and save it in the same init directory. We use a random seed to allow for replication of the results by using the same random seed. We can do so with the following command:
```bash
./ifs_perturb.py -i {path}/init/ECE3 -e ECE3 -o {path}/init -m 10 -s 3
```
During the process the following output (or similar) is printed to the screen:
```
Perturbed ensemble ITNV, variable t, mode 87520, level 30, by amount -0.1. 

Perturbed ensemble WCA4, variable t, mode 77486, level 30, by amount 0.1. 

Perturbed ensemble JI9Q, variable t, mode 256808, level 30, by amount 0.1. 

Perturbed ensemble 4RXF, variable t, mode 52684, level 30, by amount -0.1. 

Perturbed ensemble W5S0, variable t, mode 75746, level 30, by amount -0.1. 

Perturbed ensemble YC1V, variable t, mode 109472, level 30, by amount -0.1. 

Perturbed ensemble KB5R, variable t, mode 115342, level 30, by amount 0.1. 

Perturbed ensemble Z5Z7, variable t, mode 87138, level 30, by amount -0.1. 

Perturbed ensemble O2Q7, variable t, mode 70918, level 30, by amount 0.1. 

Perturbed ensemble 5DEH, variable t, mode 194380, level 30, by amount 0.1. 
```
The {path}/init directory now contains initial conditions for all members of the perturbed ensemble. The name for each member is based on the original experiment name adding an underscore and the member number:
```bash
[]$ ls {path}/init
ECE3  4RXF  5DEH  ITNV  JI9Q  KB5R  O2Q7  W5S0  WCA4  YC1V  Z5Z7
```
Each directory contains a log file with sha256 checksums of all input and output files as well as information on how the results were created.