#!/usr/bin/env python

import numpy as np
import argparse
import pygrib
import os
import shutil
import hashlib

'''
description:    Create an ensemble of IFS initial conditions from an existing
                initial state.
license:        APACHE 2.0
author:         Ronald van Haren, NLeSC (r.vanharen@esciencecenter.nl)
'''


class FullPaths(argparse.Action):
    """Expand user- and relative-paths"""
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest,
                os.path.abspath(os.path.expanduser(values)))


def is_dir(dirname):
    """
    Checks if a path is an actual directory

    :param dirname: path of a directory
    :type dirname: string
    :returns: path of a directory
    :rtype: string
    """
    if not os.path.isdir(dirname):
        msg = "{0} is not a directory".format(dirname)
        raise argparse.ArgumentTypeError(msg)
    else:
        return dirname


def sha256_checksum(filename, block_size=65536):
    '''
    Return sha256 checksum of file

    :param filename: path of a file
    :type filename: string
    :returns: sha256 checksum
    :rtype: string
    '''
    sha256 = hashlib.sha256()
    with open(filename, 'rb') as f:
        for block in iter(lambda: f.read(block_size), b''):
            sha256.update(block)
    return sha256.hexdigest()


def main(istate, iexp, outdir, members, seed, var='t',
         level=30, pert=0.1, force=False):
    """
    Create an ensemble of perturbed IFS initial conditions.
    Perturbs one random mode at level=level by amount=pert.

    :param istate: directory containing initial state to perturb [path]
    :type istate: string
    :param iexp: experiment name of initial state to perturb
    :type iexp: string
    :param outdir: base output directory [path]
    :type outdir:  string
    :param members: number of ensemble members to create
    :type members: int
    :param seed: random seed
    :type seed: int
    :param var: variable name to perturb
    :type var: string
    :param level: model level
    :type level: int
    :param pert: amount to perturb with
    :type pert: float
    :param force: Force overwriting existing perturbed conditions
    :type force: bool
    """
    inFile = "ICMSH{}INIT".format(iexp)
    file_in = os.path.join(istate, inFile)
    file_in_sha256 = sha256_checksum(file_in)
    # Open and read messages in original initial state file
    istate_in = pygrib.open(file_in)
    messages_in = istate_in.read()  # read all messages in grib file
    istate_in.close()
    # total number of modes
    nmodes = len(messages_in[0].values)
    # seed the random generator
    np.random.seed(seed)
    # pick random even modes
    modes = np.random.choice(range(0, nmodes, 2), members, replace=False)
    # define input file
    for idx, mode in enumerate(modes):
        # define new experiment name
        expName = iexp + '_' + str(idx + 1)
        # output directory experiment
        outDirExp = os.path.join(outdir, expName)
        # remove directory if exists and force==True
        if force:
            shutil.rmtree(outDirExp, ignore_errors=True)
        # create output directory
        os.makedirs(outDirExp)
        # create logger
        logger = open(os.path.join(outDirExp, expName + ".log"), 'w')
        log = {}
        log['input'] = ["[Input] sha256 {}: {}\n".format
                        (file_in, file_in_sha256)]
        log['output'] = []
        # randomize sign of perturbation
        pert = np.random.choice([-1, 1]) * pert
        # list of outputfiles to copy that don't need to be modified
        oFiles = ["ICMGG{}INIT", "ICMGG{}INIUA"]
        for oFile in oFiles:
            outputFile = oFile.format(expName)
            outputPath = os.path.join(outDirExp, outputFile)
            inputFile = oFile.format(iexp)
            inputPath = os.path.join(istate, inputFile)
            # copy original initial state directory to new experiment
            try:
                shutil.copyfile(inputPath, outputPath)
                # add to logging dict
                sha256_in = sha256_checksum(inputPath)
                sha256_out = sha256_checksum(outputPath)
                log['input'].append("[Input] sha256 {}: {}\n".format
                                    (inputPath, sha256_in))
                log['output'].append("[Output] sha256 {}: {}\n".format
                                     (outputPath, sha256_out))
            except IOError:
                pass  # silently fail
        # create a new grib file in which perturbed initial conditions
        # will be saved
        outFile = "ICMSH{}INIT".format(expName)
        fileOut = os.path.join(outDirExp, outFile)
        grbOut = open(fileOut, 'wb')
        # perturb
        for msg in messages_in:
            if (msg['shortName'] == var and msg['level'] == level):
                t = msg['values']
                t[mode] = t[mode] + pert
                msg['values'] = t
            else:
                pass
            # write perturbed gribfile
            grbOut.write(msg.tostring())
        # Closing the perturbed gribfile
        grbOut.close()
        sha256_out = sha256_checksum(fileOut)
        # add to logging dict
        log['output'].insert(0, "[Output] sha256 {}: {}\n".format
                             (fileOut, sha256_out))
        # write log
        [logger.write(msg) for msg in log['input']]
        logger.write("\n")
        [logger.write(msg) for msg in log['output']]
        # test if perturbation was a success
        if testPerturbation(file_in, fileOut, var, level, mode):
            msg = (("\nPerturbed ensemble {}, variable {}, mode {}, " +
                    "level {}, by amount {}. ").format
                   (expName, var, mode, level, pert))
            print(msg)
            logger.write(msg)
            msg = (("Random seed {} was used to create the perturbed " +
                    "initial state.\n").format(seed))
            logger.write(msg)
            logger.close()
        else:
            msg = (("Perturbation failed: input file {} and output file {}" +
                   " are the same.\n").format(file_in, fileOut))
            logger.write("\n {}".format(msg))
            logger.close()
            raise IOError(msg)


def testPerturbation(iFile, oFile, var, level, mode):
    '''
    Test if perturbation was succesful

    :param iFile: original input file [path]
    :type iFile: string
    :param oFile: perturbed output file [path]
    :type oFile: string
    :param var: variable name
    :type var: string
    :param level: perturbed model level
    :type level: int
    :param mode: perturbed mode
    :type mode: int
    :returns: success
    :rtype: bool
    '''
    # unperturbed gribfile
    grbindxIn = pygrib.index(iFile, 'shortName', 'level')
    unPert = grbindxIn.select(shortName=var, level=level)[0]['values'][mode]
    grbindxIn.close()
    # perturbed gribfile
    grbindxOut = pygrib.index(oFile, 'shortName', 'level')
    pert = grbindxOut.select(shortName=var, level=level)[0]['values'][mode]
    grbindxOut.close()
    if not (unPert == pert):
        return True
    else:
        return False


if __name__ == '__main__':
    # define command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--initialstate',
                        help='Directory containing initial state to perturb',
                        action=FullPaths, type=is_dir, required=True)
    parser.add_argument('-e', '--experiment',
                        help='Experiment name of initial state to perturb',
                        type=str, required=True)
    parser.add_argument('-o', '--outputdir', help='Output directory',
                        action=FullPaths, type=is_dir, required=True)
    parser.add_argument('-m', '--members',
                        help='Number of initial states to create',
                        type=int, default=1, required=False)
    parser.add_argument('-s', '--seed', help='Random seed', type=int,
                        required=False)
    parser.add_argument('-f', '--force', action='store_true',
                        help="force overwriting existing files")
    parser.add_argument('-v', '--variable', type=str, required=False,
                        help="variable name", default='t')
    parser.add_argument('-l', '--level', type=int, required=False,
                        help="model level", default=30)
    parser.add_argument('-p', '--perturbation', type=float, required=False,
                        help="perturbation amount", default=0.1)
    # get arguments
    args = parser.parse_args()
    # call main()
    main(args.initialstate, args.experiment, args.outputdir,
         args.members, args.seed,
         args.variable, args.level, args.perturbation, args.force)
