import subprocess

outfile = "/tmp/horairyst_output"

def run_command(cmd):
    subprocess.getoutput(cmd)
    file = open(outfile, "r")
    res = ""
    for line in file:
        res += line
    return res


def createBatch(filePath):
    text  = "read "+filePath+"\n"
    text += "optimize\n"
    text += "write solution "+outfile+"\n"
    text += "quit"

    file = open(outfile, "w")
    file.write(text)
    file.flush()
    file.close()
    return outfile


def getSolverOutput(filePath):
    batchPath = createBatch(filePath)
    return run_command("./scip -b " + batchPath)


def extractSolution(output):
    lines = output.split("\n")
    res = {}
    res["status"] = lines[0].split(":")[1].strip()
    res["value"] = float(lines[1].split(":")[1].strip())
    res["solution"] = []
    for i in range(2,len(lines)-1):
        ln = lines[i].split("\t")[0].split(" ")
        res["solution"].append((ln[0], float(ln[-2])))
    print(output)
    print("-"*80)
    print(res)


def solve(filePath):
    return extractSolution(getSolverOutput(filePath))
