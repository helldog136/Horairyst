class Problem(object):


    def __init__(self, _S, _P, _E, _R, _C, _roles, _strongConstraints, _weakConstraints):
        # if len(_C) != len(_E) or len(_C[0]) != len(_R):
        #    print("wrong size for _C is ", len(_C), "X", len(_C[0]), " but should be ", len(_E), "X", len(_R))
        #    exit(-1)
        self.sep = "_"
        self.S = _S
        self.P = _P
        self.E = _E
        self.R = _R
        self.C = _C
        self.roles = _roles
        self.strongConstraints = _strongConstraints
        self.weakConstraints = _weakConstraints
        self.value = None
        problemMatrix = []
        for i in range(len(self.S)):
            problemMatrix.append([])
            for j in range(len(self.P)):
                problemMatrix[i].append((True, []))
        self.validity = (True, [], [], [], [], problemMatrix)

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

    @classmethod
    def fromJsonMatrix(cls, data):
        from horairyst.problem import constraint

        S = data['sessions']
        P = data['periods']
        E = []
        R = []
        C = []
        roles = []
        X = []
        Y = []

        tmp = []

        doublesE = []

        #TODO populate C and roles and X,Y
        for j, line in enumerate(data['matrix']):
            for i, slot in enumerate(line):
                stud = slot['student']
                if stud != "":
                    if stud in E:
                        tupll = (i, j, stud, [], [])
                        for teacher in slot['teachers']:
                            if teacher["role"] == "R":
                                tupll[3].append(teacher["name"])
                            else:
                                tupll[4].append(teacher["name"])
                            if teacher["name"] not in R:
                                R.append(teacher["name"])
                        doublesE.append(tupll)
                    else:
                        C.append([])
                        roles.append([])
                        E.append(stud)
                        tupll = (i, j, stud, [], [])
                        for teacher in slot['teachers']:
                            if teacher["role"] == "R":
                                tupll[3].append(teacher["name"])
                            else:
                                tupll[4].append(teacher["name"])
                            if teacher["name"] not in R:
                                R.append(teacher["name"])

                        tmp.append(tupll)

        for i in range(len(S)):
            X.append([])
            Y.append([])
            for j in range(len(P)):
                X[i].append([])
                Y[i].append([])
                for k in range(len(E)):
                    X[i][j].append(0)
                for l in range(len(R)):
                    Y[i][j].append(0)

        # init C
        for k in range(len(C)):
            for l in range(len(R)):
                C[k].append(0)
                roles[k].append("")

        for i, j, k, r, d in tmp:
            X[i][j][E.index(k)] = 1
            for rap in r:
                Y[i][j][R.index(rap)] = 1
                C[E.index(k)][R.index(rap)] = 1
                roles[E.index(k)][R.index(rap)] = "R"
            for dirc in d:
                Y[i][j][R.index(dirc)] = 1
                C[E.index(k)][R.index(dirc)] = 1
                roles[E.index(k)][R.index(dirc)] = "D"

        for i, j, k, r, d in doublesE:
            X[i][j][E.index(k)] = 1
            for rap in r:
                Y[i][j][R.index(rap)] = 1
                C[E.index(k)][R.index(rap)] = 1
                roles[E.index(k)][R.index(rap)] = "R"
            for dirc in d:
                Y[i][j][R.index(dirc)] = 1
                C[E.index(k)][R.index(dirc)] = 1
                roles[E.index(k)][R.index(dirc)] = "D"


        print(S, P, E, R, C, roles, X, Y)

        res = cls(S, P, E, R, C, roles, constraint.getStrongConstraints(), constraint.getWeakConstraints())

        res.X = X
        res.Y = Y

        res.checkValidity()

        print(res.isValid())


        return res

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

        for c in self.weakConstraints.getConstraints(self):
            print("weak\n------\n"+c+"\n---")
            obj = (obj[:-3] if c[:2] == " -" else obj) + str(c) +\
                  ("" if len(c) == 0 or c[-2:] == "+ " else " + ")
        obj = obj[:-2]

        cst = ""
        for c in self.strongConstraints.getConstraints(self):
            print("strong\n------\n" + c + "\n---")
            cst += str(c) + ("" if len(c) == 0 or c[-1] == "\n" else "\n")

        res = "Minimize\n"
        res += obj
        res += "\n"
        res += "Subject To\n"
        res += cst
        res += "Binary\n"
        res += binr
        res += "End"


        print(res)
        return res

    def checkValidity(self):
        validity = self.strongConstraints.checkValidities(self.X, self.Y, self.S, self.P, self.E, self.R, self.C)
        wrongs_S = []
        wrongs_P = []
        wrongs_E = []
        wrongs_R = []
        problemMatrix = []
        for i in range(len(self.S)):
            problemMatrix.append([])
            for j in range(len(self.P)):
                problemMatrix[i].append((True, []))
        if not validity[0]:
            for problem in validity[1]:
                if problem[0] is False:
                    for w in problem[1]:
                        if w[0] >= 0:
                            wrongs_S.append((self.S[w[0]], problem[2], w))
                        if w[1] >= 0:
                            wrongs_P.append((self.P[w[1]], problem[2], w))
                        if w[2] >= 0:
                            wrongs_E.append((self.E[w[2]], problem[2], w))
                        if w[3] >= 0:
                            wrongs_R.append((self.R[w[3]], problem[2], w))

            # TODO synthetize what's wrong
            def printList(lst):
                res = ""
                for i in lst:
                    res += str(i) + ", "
                return res

            for v, p, reason in validity[1]:
                if v is False:
                    for (i, j, k, l) in p:
                        if i >= 0 and j >= 0:
                            problemMatrix[i][j] = (False, problemMatrix[i][j][1])
                            problemMatrix[i][j][1].append(reason)

            print("Problems in sessions: " + printList(wrongs_S))
            print("Problems in periods: " + printList(wrongs_P))
            print("Problems with students: " + printList(wrongs_E))
            print("Problems with teachers: " + printList(wrongs_R))
            print(problemMatrix)

        self.validity = (validity[0], wrongs_S, wrongs_P, wrongs_E, wrongs_R, problemMatrix)


    def isValid(self):
        self.checkValidity()
        return self.validity[0]

    def prettyPrintVar(self, var, i, j, ind):
        return var + self.sep + str(i) + self.sep + str(j) + self.sep + str(ind)

    def resetSolution(self):
        for i in range(len(self.X)):
            for j in range(len(self.X[i])):
                for k in range(len(self.X[i][j])):
                    self.X[i][j][k] = 0
        for i in range(len(self.Y)):
            for j in range(len(self.Y[i])):
                for l in range(len(self.Y[i][j])):
                    self.Y[i][j][l] = 0

    def setSolution(self, sol):
        # wipe data in X and Y
        self.resetSolution()

        for t in sol["solution"]:
            self._setSol(t)
        self.value = sol["value"]
        self.checkValidity()

    def displaySolution(self):
        for i in range(len(self.X)):
            for j in range(len(self.X[i])):
                for k in range(len(self.X[i][j])):
                    if self.X[i][j][k] == 1:
                        print(self.E[k], self.S[i], self.P[j])
                        for l in range(len(self.Y[i][j])):
                            if self.Y[i][j][l] == 1:
                                if self.C[k][l] == 1:
                                    print(self.roles[k][l] + ": " +self.R[l])
                                else:
                                    #print("#" + self.R[l])
                                    pass

    def getSolutionAsJson(self):
        res = {}

        res["slots"] = []
        for i in range(len(self.X)):
            for j in range(len(self.X[i])):
                for k in range(len(self.X[i][j])):
                    if self.X[i][j][k] == 1:
                        slot = {"hour": self.P[j],
                                "room": self.S[i],
                                "student": self.E[k],
                                "teachers": [],
                                "validity": {"value": self.validity[-1][i][j][0],
                                             "reasons": self.validity[-1][i][j][1]}
                                }
                        for l in range(len(self.Y[i][j])):
                            if self.Y[i][j][l] == 1 and self.C[k][l] == 1:
                                teacher = {"role": self.roles[k][l], "name": self.R[l]}
                                slot["teachers"].append(teacher)
                        res["slots"].append(slot)
        print(res)
        return res

    def getCompleteJson(self):
        return {"value": self.value,
                "matrix": self.getSolutionAsJSONMatrix(),
                "linear": self.getSolutionAsJson(),
                "latex": self.getSolutionAsLatex()}

    def getSolutionAsJSONMatrix(self):
        self.checkValidity()
        # {"sessions":["0a07", "0a11"],
        #  "periods":["09h00","09h30","10h00"],
        #  "matrix": [[{"student":"Alain Terieur",
        #               "directors":["A. Buys"],
        #               "reporters":["J. Wijsen"]},
        #              {"student":"",
        #               "directors":[],
        #               "reporters":[]}],
        #             [{"student":"Alain Terieur",
        #               "directors":["A. Buys"],
        #               "reporters":["J. Wijsen"]},
        #              {"student":"",
        #               "directors":[],
        #               "reporters":[]}],
        #             [{"student":"Alain Terieur",
        #               "directors":["A. Buys"],
        #               "reporters":["J. Wijsen"]},
        #              {"student":"",
        #               "directors":[],
        #               "reporters":[]}]
        #             ]
        # }
        #
        res = {"sessions": [], "periods": [], "matrix": []}
        for i in self.S:
            res["sessions"].append(str(i))
        for j in self.P:
            res["periods"].append(str(j))

        for j in range(len(self.P)):
            period = []
            for i in range(len(self.S)):
                slot = {"student": "", "teachers": [], "validity": {"value": self.validity[-1][i][j][0],
                                                                    "reasons": self.validity[-1][i][j][1]}}
                for k in range(len(self.E)):
                    if self.X[i][j][k] == 1:
                        slot["student"] = self.E[k]
                        for l in range(len(self.R)):
                            if self.Y[i][j][l] == 1 and self.C[k][l] == 1:
                                slot["teachers"].append({"name": self.R[l], "role": self.roles[k][l]})
                period.append(slot)
            res["matrix"].append(period)
        return res

    def getSolutionAsLatex(self):
        def latex(string):
            return string.replace("é", "\\'e")\
                .replace("è", "\\`e")\
                .replace("ë", "\\\"e")\
                .replace("à", "\\'a")\
                .replace("ü", "\\\"u")
        import itertools
        res = """\\documentclass[a4paper,11pt]{article}

\\usepackage[T1]{fontenc}
\\usepackage[latin1]{inputenc}
\\usepackage[english,frenchb]{babel}
\\usepackage{amsmath}
\\usepackage{amssymb}
\\usepackage{graphicx}
\\usepackage{wrapfig}
\\usepackage[margin=2cm]{geometry}
\\usepackage{enumerate}
\\usepackage{algorithm}
\\usepackage[noend]{algorithmic}
\\usepackage{tikz}
\\usetikzlibrary{shapes,arrows}
                
\\begin{document}

\\centerline{\\Large\\bf Master en sciences informatiques, \\`a horaire d\\'ecal\\'e \\`a Charleroi}

\\centerline{TODO}
\\centerline{Boulevard Joseph II, 38-40, \\`a Charleroi}

\\subsection*{D\\'efenses :  cours de lecture et r\\'edaction scientifiques - m\\'emoires}

\\begin{itemize}
\\item Dur\\'ee des pr\\'esentations : 15 minutes  -  Questions : 10 minutes. 
\\item Mat\\'eriel : PC portable, projecteur data et projecteur de transparents.
\\item Les d\\'efenses des m\\'emoires sont indiqu\\'ees en italique.
\\end{itemize}
"""
        for i, iN in enumerate(self.S):
            res += "\\bigskip\\noindent Session "+iN+" (Pr\\'esident TODO)\\\\\n"
            res += "\\begin{tabular}{|r|l|l|l|}\n"
            res += "\t\\hline\n"
            res += "\t & Etudiant & Directeur(s) & Rapporteur(s) \\\\\n"
            res += "\t\\hline\n"
            for j, slot in enumerate(self.X[i]):
                mod = lambda x: x
                currentK = -1
                for k, stud in enumerate(self.E):
                    if self.X[i][j][k] == 1:
                        currentK = k
                        if stud[0] == "M":
                            mod = lambda x: "\\textit{"+x+"}"
                        stud = stud[2:]
                        res += "\t"+latex(self.P[j])+" & "+mod(latex(stud))+" & "
                if currentK == -1: #no programmed student
                    pass#res += " & & \\\\\n"
                else:
                    dirs = []
                    rapp = []
                    for l, teach in enumerate(self.R):
                        if self.roles[currentK][l] == 'D':
                            dirs.append(teach)
                        elif self.roles[currentK][l] == 'R':
                            rapp.append(teach)
                    res += mod(latex(dirs[0])) + " & " + mod(latex(rapp[0])) + "\\\\\n"
                    flip = False
                    for d, r in itertools.zip_longest(dirs, rapp, fillvalue=""):
                        if flip:
                            res += "\t & & " + mod(latex(d)) + " & " + mod(latex(r)) + "\\\\\n"
                        else:
                            flip = True
                    res += "\t\\hline\n"
            res += "\\end{tabular}\\\\\n"
        res += """\\subsection*{D\\'elib\\'erations et proclamations}
\\begin{itemize}
\\item De TODO \\`a TODO, d\\'elib\\'erations pour le cours de lecture et r\\'edaction scientifiques et pour les m\\'emoires
\\item A partir de TODO, d\\'elib\\'erations pour le master en sciences informatiques, \\`a horaire d\\'ecal\\'e \\`a Charleroi
\\item Les proclamations suivront directement (vers TODO - TODO)
\\end{itemize}"""

        return res



    def _setSol(self, t):
        tmp = t[0].split(self.sep)
        if tmp[0] == "x":
            self.X[int(tmp[1])][int(tmp[2])][int(tmp[3])] = int(round(float(t[1])))
        elif tmp[0] == "y":
            self.Y[int(tmp[1])][int(tmp[2])][int(tmp[3])] = int(round(float(t[1])))
        else:
            print("error")
