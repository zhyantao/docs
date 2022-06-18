# -*- coding: utf-8 -*-

def setup(app):
    import cairosvg
    import os

    def exportsvg(fromDir, targetDir, exportType):
        num = 0
        for a, f, c in os.walk(fromDir):
            for fileName in c:
                path = os.path.join(a, fileName)
                if os.path.isfile(path) and fileName[-3:] == "svg":
                    num += 1
                    
                    fileHandle = open(path, encoding='utf-8')
                    svg = fileHandle.read()
                    fileHandle.close()

                    exportPath = os.path.join(targetDir, fileName[:-3] + exportType)
                    
                    if (os.path.exists(exportPath)):
                        continue

                    exportFileHandle = open(exportPath, 'w')

                    if exportType == "png":
                        try:
                            cairosvg.svg2png(bytestring=svg, write_to=exportPath)
                        except:
                            print("error in convert svg file : %s to png." % (path))

                    elif exportType == "pdf":
                        try:
                            cairosvg.svg2pdf(bytestring=svg, write_to=exportPath)
                        except:
                            print("error in convert svg file: %s to pdf." % (path))

                    exportFileHandle.close()
                    print("Export ", exportType, " to ", exportPath)

    CURRENT_DIR = os.path.abspath('.')
    svgDir = f'{CURRENT_DIR}/_static/images/'
    exportDir = f'{CURRENT_DIR}/_static/images/'
    exportFormat = 'png'
    if not os.path.exists(exportDir):
        os.mkdir(exportDir)
    exportsvg(svgDir, exportDir, exportFormat)
