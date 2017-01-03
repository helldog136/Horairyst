def parse(filename):
    from horairyst.parsers import csvParser
    import pandas
    outFile = "/tmp/out.csv"

    xl = pandas.ExcelFile(filename)
    sh = xl.parse(xl.sheet_names[0])
    sh.to_csv(outFile)
    return csvParser.parse(outFile)


def getHandledExtensions():
    return [".xls"]
