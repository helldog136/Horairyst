class Problem(object):
    def __init__(self, _S, _P, _E, _R, _C, _constraints):
        # if len(_C) != len(_E) or len(_C[0]) != len(_R):
        #    print("wrong size for _C is ", len(_C), "X", len(_C[0]), " but should be ", len(_E), "X", len(_R))
        #    exit(-1)
        self.S = _S
        self.P = _P
        self.E = _E
        self.R = _R
        self.C = _C
        self.constraints = _constraints

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
        res = "Minimize\n"
        binr = "Binary\n"
        for i in range(len(self.X)):
            for j in range(len(self.X[i])):
                for k in range(len(self.X[i][j])):
                    res += self.prettyPrintVar("x", i, j, k) + " + "
                    binr += self.prettyPrintVar("x", i, j, k) + "\n"
        for i in range(len(self.Y)):
            for j in range(len(self.Y[i])):
                for l in range(len(self.Y[i][j])):
                    res += self.prettyPrintVar("y", i, j, l)
                    res += "\n" if (i, j, l) == (len(self.Y) - 1, len(self.Y[i]) - 1, len(self.Y[i][j]) - 1) else " + "
                    binr += self.prettyPrintVar("y", i, j, l) + "\n"
        res += "Subject To\n"
        for c in self.constraints.getAll(self):
            res += str(c) + "" if c[-1] == "\n" else "\n"

        res += binr
        return res

    def prettyPrintVar(self, x, i, j, k, sep=":"):
        return x + sep + str(i) + sep + str(j) + sep + str(k)
