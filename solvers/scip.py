import subprocess


def run_command(cmd):
    return subprocess.getoutput(cmd)

def getSolverOutput(filePath):
    return run_command("/home/helldog136/Dropbox/School/MA2/Projet/Horairyst/scip -f " + filePath)


def extractSolution(output):
    print(output)


def solve(filePath):
    return extractSolution(getSolverOutput(filePath))
