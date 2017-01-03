class Problem(object):
    def __init__(self, _S, _P, _E, _R, _C, _strongConstraints, _weakConstraints):
        # if len(_C) != len(_E) or len(_C[0]) != len(_R):
        #    print("wrong size for _C is ", len(_C), "X", len(_C[0]), " but should be ", len(_E), "X", len(_R))
        #    exit(-1)
        self.sep = "_"
        self.S = _S
        self.P = _P
        self.E = _E
        self.R = _R
        self.C = _C
        self.strongConstraints = _strongConstraints
        self.weakConstraints = _weakConstraints

        # init 2 matrix X and Y for decision variables
        self.X = []
        self.Y = []
        for i in range(len(self.S)):
            line1 = []
            line2 = []
            for j in range(len(self.P)):
                l1 = []
                for k in range(len(self.E)):
                    l1.append(0)
                line1.append(l1)
                l2 = []
                for l in range(len(self.R)):
                    l2.append(0)
                line2.append(l2)
            self.X.append(line1)
            self.Y.append(line2)

    def write(self):
        obj = ""
        binr = ""
        for i in range(len(self.X)):
            for j in range(len(self.X[i])):
                for k in range(len(self.X[i][j])):
                    obj += self.prettyPrintVar("x", i, j, k) + " + "
                    binr += self.prettyPrintVar("x", i, j, k) + "\n"
        for i in range(len(self.Y)):
            for j in range(len(self.Y[i])):
                for l in range(len(self.Y[i][j])):
                    obj += self.prettyPrintVar("y", i, j, l) + " + "
                    binr += self.prettyPrintVar("y", i, j, l) + "\n"
        for c in self.weakConstraints.getAll(self):
            obj = (obj[:-3] if c[:2] == " -" else obj) + str(c) +\
                  ("" if len(c) == 0 or c[-2:] == "+ " else " + ")
        obj = obj[:-2]

        cst = ""
        for c in self.strongConstraints.getAll(self):
            cst += str(c) + "" if len(c) == 0 or c[-1] == "\n" else "\n"

        res = "Minimize\n"
        res += obj
        res += "\n"
        res += "Subject To\n"
        res += cst
        res += "Binary\n"
        res += binr


        print(res)
        return res

    def prettyPrintVar(self, x, i, j, k):
        return x + self.sep + str(i) + self.sep + str(j) + self.sep + str(k)

    def setSolution(self, sol):
        for t in sol["solution"]:
            self._setSol(t)

    def displaySolution(self):
        for i in range(len(self.X)):
            for j in range(len(self.X[i])):
                for k in range(len(self.X[i][j])):
                    if self.X[i][j][k] == 1:
                        print(self.E[k], self.S[i], self.P[j])
                        for l in range(len(self.Y[i][j])):
                            if self.Y[i][j][l] == 1:
                                print(("" if self.C[k][l] == 1 else "#") + self.R[l])

    def _setSol(self, t):
        tmp = t[0].split(self.sep)
        if tmp[0] == "x":
            self.X[int(tmp[1])][int(tmp[2])][int(tmp[3])] = t[1]
        elif tmp[0] == "y":
            self.Y[int(tmp[1])][int(tmp[2])][int(tmp[3])] = t[1]
        else:
            print("error")
