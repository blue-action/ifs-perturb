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
During the process the following output is printed to the screen:
```
```
