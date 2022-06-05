# Lewis signaling game simulation

This repository contains code for simulating a Lewis signaling game.
The first goal is covering everithying in [this paper](https://www.imbs.uci.edu/files/docs/technical/2006/mbs06_09.pdf) and try to replicate its findings.
Further code could cover more complicated signaling games.

## Features
As of now the program covers
- Running a n-states/m-terms game and getting its success rate, along with states and signals
- Urn learning with positive reenforcement
- Urn learning with positive and negative reenforcement

## Installation
Run
```
python signaling.py
```
To run a classic 2-states/2-terms game.

## Usage
```
usage: signaling.py [-h] [-r RUNS] [-s STATES] [-t TERMS] [-l {positive,positive_negative}]

A Lewis singaling game simulation

options:
  -h, --help            show this help message and exit
  -r RUNS, --runs RUNS  Number of runs
  -s STATES, --states STATES
                        Number of states
  -t TERMS, --terms TERMS
                        Number of terms (signals)
  -l {positive,positive_negative}, --learning {positive,positive_negative}
                        Type of learning
```

