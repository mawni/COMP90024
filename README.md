# COMP90024
This project involved conducting analysis on a 14GB+ JSON file of Twitter data. 4,233,611 tweets were processed to calculate sentiment scores for different grid regions across Melbourne. The python script is parallelised, and uses MPI (mpi4py) to faciliate parallel computing on the University of Melbourne's High Performance Computing (HPC) system. 

Files included:
Sample twitter data.
Two python scripts for the central processing: one for small scale testing (no MPI work), the other with fully parallelised code for final execution.
SLURM bash scripts used for job submission to the University of Melbourne's HPC.

Note: *.slurm files were edited with Notepad++ in order to have Unix end-of-line characters. This is a requirement for SLURM scripts.

Tech stack: git, python, MPI (with mpi4py), SLURM, JSON, Spyder, Anaconda
