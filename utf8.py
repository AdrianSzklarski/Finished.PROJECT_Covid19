import glob
from os.path import join


def encode_to_utf8(inputPaths, resultFolder):
    fileNumber = 0
    for path in inputPaths:
        outputPath = join(resultFolder, f'{fileNumber}.csv')
        fileNumber += 1
        try:
            with open(path, encoding='cp1250') as inputFile, open(outputPath, 'w', encoding='utf-8') as outputFile:
                for line in inputFile:
                    outputFile.write(line)
        except:
            with open(path, encoding='utf-8') as inputFile, open(outputPath, 'w', encoding='utf-8') as outputFile:
                for line in inputFile:
                    outputFile.write(line)


sickPaths = glob.glob(
    r'/home/adrian/Pulpit/GitHub_Public/Covid_19/dane_historyczne_powiaty/*.csv')

sickFolder = r'/home/adrian/Pulpit/GitHub_Public/Covid_19/sick'

allVacsPaths = glob.glob(
    r'/home/adrian/Pulpit/GitHub_Public/Covid_19/dane_historyczne_szczepienia/*.csv')

vacsFolder = r'/home/adrian/Pulpit/GitHub_Public/Covid_19/vacs'

vacsPaths = []
for path in allVacsPaths:
    fileName = path.split('/')[-1]  # For Windows path.split('\\')
    dataRange = fileName.split('_')[3]
    if dataRange == 'pow':
        vacsPaths.append(path)

encode_to_utf8(sickPaths, sickFolder)
encode_to_utf8(vacsPaths, vacsFolder)
