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
