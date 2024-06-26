# Sudoku Solver

## Description

This repository contains code that can solve Sudoku puzzles by implementing a simple brute-force algorithm. It has functionality that enables users to enter Sudoku puzzles as text files, and then output the solution in a user friendly way, within a matter of seconds.

The project is intended to be a model example of some of the most fundamental software development practices, to ensure that a software project is maintainble, robust, optimised, and organised in a way that facilitates collaboration.

## How to use the project

The project is designed to be usable via Docker. In order to run the project in this way, it is best to clone the repository to your local device using git, build the docker image using the terminal command

`docker build -t sudokusolver .`

and then running the container by executing the command

`docker run --rm -ti sudokusolver`

where the options specify that the container is removed after exiting, and ensure that the container can be interacted with easily in the terminal.

Alternatively, you can run (in the root directory)

`conda env create -f environment.yml`

`conda activate mphildis_assessment_jh2284`

to build the correct conda environment and run the code in the location you cloned it to.

Next, to run the actual code you simply execute the command

`python src/solve_sudoku.py input.txt`

This gives the solution to the standard sudoku puzzle specified in input.txt, which can be modified to solve different puzzles. Alternatively, use

`python src/solve_sudoku.py input.txt > output.txt`

to save the solution grid to output.txt.

## Details

Measures have been taken to optimise the code and it is intended to solve most Sudoku puzzles in well under 60 seconds. Moreover, it should account for any errors in the input, for instance it will output an error message if the specified problem has no solution. The current version of the code will not however notify the user of a non-unique solution; it will simply output the first solution it finds.

The code is written in Python using version 3.9.18. The testing is done using pytest, and the testing suite can be run by simply using the command `pytest` in the root directory.

James Hughes, 12th December 2023.
