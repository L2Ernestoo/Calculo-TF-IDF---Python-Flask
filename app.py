import math
from flask import Flask, render_template, request
from nltk.text import TextCollection

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/calcular')
def convertidor():
    return render_template('convertidor.html')


@app.route('/acerca-de')
def acerca():
    return render_template('acerca_de.html')


@app.route('/convertidor_out', methods=['get','post'])
def convertidor_out():
    txt = request.form['txt']
    documentos = [txt]
    directorioP = {}

    for index, oracion in enumerate(documentos):
        tokens = oracion.split(' ')
        directorioP[index] = [(palabra, tokens.count(palabra)) for palabra in tokens]

    # ___________________________________-TERMINO FRECUENTE-______________________________#
    terminoFrecuente = {}

    for i in range(0, len(documentos)):
        arrayDuplicados = []
        for frecPalabra in directorioP[i]:
            if frecPalabra not in arrayDuplicados:
                arrayDuplicados.append(frecPalabra)
            terminoFrecuente[i] = arrayDuplicados

    termFrecNormList = {}
    terminoFrecuenteNormalizado = {}
    count_1 = 0
    for i in range(0, len(documentos)):
        oracion = directorioP[i]
        longitudOracion = len(oracion)
        listaNormalizada = []
        for frecPalabra in terminoFrecuente[i]:
            frecNormalizada = frecPalabra[1] / longitudOracion
            termFrecNormList[count_1] = frecPalabra[0] + ": " + str(frecNormalizada)
            count_1 = count_1 + 1
            listaNormalizada.append((frecPalabra[0], frecNormalizada))
        terminoFrecuenteNormalizado[i] = listaNormalizada

    todosLosDocumentos = ''
    for oracion in documentos:
        todosLosDocumentos += oracion + ' '
    todosLosDocumentosTokenized = todosLosDocumentos.split(' ')

    todosLosDocumentosNoDuplicates = []

    for palabra in todosLosDocumentosTokenized:
        if palabra not in todosLosDocumentosNoDuplicates:
            todosLosDocumentosNoDuplicates.append(palabra)

    directorioDocumentosConTerminoDentro = {}

    for index, voc in enumerate(todosLosDocumentosNoDuplicates):
        count = 0
        for oracion in documentos:
            if voc in oracion:
                count += 1
        directorioDocumentosConTerminoDentro[index] = (voc, count)

    # calculate IDF _ Inversa

    directorioDeIDFNoDuplicados = {}
    dirIDFNotDuplicates = {}
    count_2 = 0
    for i in range(0, len(terminoFrecuenteNormalizado)):
        listaDeIDFCalculados = []
        for palabra in terminoFrecuenteNormalizado[i]:
            for x in range(0, len(directorioDocumentosConTerminoDentro)):
                if palabra[0] == directorioDocumentosConTerminoDentro[x][0]:
                    dirIDFNotDuplicates[count_2] = palabra[0] + ": " + str(
                        math.log(len(documentos) / directorioDocumentosConTerminoDentro[x][1]))
                    count_2 = count_2 + 1
                    listaDeIDFCalculados.append(
                        (palabra[0], math.log(len(documentos) / directorioDocumentosConTerminoDentro[x][1])))
        directorioDeIDFNoDuplicados[i] = listaDeIDFCalculados

    # Multiply tf by idf for tf-idf

    dictOfTF_IDF = {}

    dictOfTF_IDFL = {}
    count_2 = 0
    for i in range(0, len(terminoFrecuenteNormalizado)):
        listOfTF_IDF = []
        TForacion = terminoFrecuenteNormalizado[i]
        IDForacion = directorioDeIDFNoDuplicados[i]
        for x in range(0, len(TForacion)):
            dictOfTF_IDFL[count_2] = TForacion[x][0] + ": " + str(TForacion[x][1] * IDForacion[x][1])
            count_2 = count_2 + 1
            listOfTF_IDF.append((TForacion[x][0], TForacion[x][1] * IDForacion[x][1]))
        dictOfTF_IDF[i] = listOfTF_IDF

    return render_template('convertidor_out.html',
                           termNormal=termFrecNormList,
                           termL=len(termFrecNormList),
                           frecInversa=dirIDFNotDuplicates,
                           frecInversaL=len(dirIDFNotDuplicates),
                           tfIDf=dictOfTF_IDFL,
                           tfIDfL=len(dictOfTF_IDFL)
                           )


if __name__ == '__main__':
    app.run()
