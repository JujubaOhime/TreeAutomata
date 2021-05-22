import re
# estado 0 = wait
# estado -1 = estado inesistente
# estado -2 = estado erro
# estado -3 = estado sucesso

class elemento(object):
    def __init__(self, altura, pai, arvore, filhos, valor, estado):
        self.altura = altura
        self.pai = pai
        self.arvore = arvore 
        self.valor = valor
        self.filhos = filhos
        self.estado = estado

    def __str__(self):

        paiRes = -1
        if(self.pai != -1):
            paiRes = self.pai.estado
        filhosRes = []
        for p in range(len(self.filhos)):
            if(self.filhos[p] != -1):
                filhosRes.append(self.filhos[p].estado)
            else: filhosRes.append(self.filhos[p])
        teste = "A altura é {}, pai é {}, da arvore {}, com valor {}, filhos {} e estado {}".format(self.altura, paiRes, self.arvore, self.valor, filhosRes, self.estado)
        
        return teste

def numLinhas(nomeArq):
    arq = open(nomeArq)
    numLinhas = 0
    conteudo = arq.read()
    conteudo = conteudo.split("\n")
    for i in conteudo:
        if i:
            numLinhas += 1
    arq.close()
    return numLinhas

def singXIXJ(elemento, i, j):
    i = i-1
    j = j-1
    estado = -1

    estado_ant = []
    for j in range (len(elemento.filhos)):
        if(elemento.filhos[j].estadoxixj): estado_ant.append(elemento.filhos[j].estadoxixj)
        else: estado_ant.append(-1)

    if(all(v == -1 for v in estado_ant)):
        if(elemento.valor[i] == 1 and elemento.valor[j] == 0): estado = 10
        elif(elemento.valor[i] == 1 and elemento.valor[j] == 1 ): estado = 11
        elif(elemento.valor[i] == 0 and elemento.valor[j] == 1): estado = 1
        elif(elemento.valor[i] == 0 and elemento.valor[j] == 0): estado = 0

    elif(elemento.valor[i] == 1 and elemento.valor[j] == 0):
        if (estado_ant.count(1) == 1): estado = 11
        elif (all(v == 0 for v in estado_ant)): estado = 10
        else: estado = -2

    elif(elemento.valor[i] == 1 and elemento.valor[j] == 1):
        if (all(v == 0 for v in estado_ant)): estado = 11
        else: estado = -2

    elif(elemento.valor[i] == 0 and elemento.valor[j] == 1):
        if (estado_ant.count(10) == 1): estado = 11
        elif (all(v == 0 for v in estado_ant)): estado = 1
        else: estado = -2
    
    elif(elemento.valor[i] == 0 and elemento.valor[j] == 0):
        if (estado_ant.count(10) == 1): estado = 10
        elif (estado_ant.count(11) == 1): estado = 11
        elif (estado_ant.count(1) == 1): estado = 1
        elif (sorted(estado_ant) == [1, 10]): estado = 11
        elif (all(v == 0 for v in estado_ant)): estado = 0
        else: estado = -2

    return estado


def singXI(elemento, i):
    i = i - 1
    estado = 0
    estado_ant = []
    for j in range (len(elemento.filhos)):
        if(hasattr(elemento.filhos[j], 'xi')): estado_ant.append(elemento.filhos[j].xi)
        else: estado_ant.append(-1)
    if(all(v == -1 for v in estado_ant)):
        if(elemento.valor[i] == 1): estado = 1
        else: estado = 0

    elif(elemento.valor[i] == 1):
        if(all(v == 0 for v in estado_ant)): estado = 1
        else: estado = -2

    elif(elemento.valor[i] == 0):
        if (estado_ant.count(1) == 1): estado = 1
        elif(all(v == 0 for v in estado_ant)): estado = 0
        else: estado = -2
        
    return estado


numArvores = 1
elementosArvore = []
ultimaAlturaArvores = [] 
alfabetoRanqueado = []
conjEstados = []
conjEstadosFinal = []
estado_ant = [0, 0]

for i in range(numArvores):
    arvore = i
    alturaMaxima = 0
    nomeArq = "treefinal" + str(i+1) + ".txt"
    tamanhoArq = numLinhas(nomeArq)
    arq = open(nomeArq)
    linha = []
    serLido = 0
    texto = arq.readline()
    alturaMaxima = 0
    for j in range(tamanhoArq - 3):
        texto = arq.readline()
        
        if ("Alfabeto Ranqueado:" in texto):
            serLido = 1
            texto = arq.readline() 
        elif ("Conjunto de estados:" in texto):
            serLido = 2
            texto = arq.readline()
        elif ("Conjunto de estados finais:" in texto ):
            serLido = 3
            texto = arq.readline()
        texto = texto.replace("\n", "")
        #def __init__(self, altura, pai, arvore, filhos, valor, estado):
        if (texto):

            if (serLido == 0):
                valor = []
                primeiro, estado = texto.split('->') # estado = q12
                parenteses = re.search('\(([^)]+)', primeiro).group(1) #parenteses = q10, q11
                no = primeiro.replace(("(" + parenteses + ")"), "") #no = T0N0                
                pri, seg = parenteses.split(',') # pri = q10, seg = q11
                if(pri == '-1'): pri = -1
                if(seg == '-1'): seg = -1
                filho = [pri, seg]
                for g in range(len(filho)):
                    valor.append(0) # valor é o -1 -1

                if (j == 0):

                    filho1 = -1
                    filho2 = -1
                    pai = elemento(0, -1, arvore , -1, [1,0], estado)
                    if(pri != -1):
                        filho1 = elemento(1, pai, arvore, [-1, -1], [1,0], pri)
                        filho1.pai = pai
                        linha.append(filho1)
                    if(seg != -1):
                        filho2 = elemento(1, pai, arvore,  [-1, -1], [0,0], seg)
                        filho2.pai = pai
                        linha.append(filho2)
                        
                    filhos = [filho1, filho2]
                    pai.filhos = filhos
                    linha.append(pai)
                    
                else:
                    for k in range(len(linha)):
                        for l in range(len(linha[k].filhos)):
                            
                            if (linha[k].filhos[l] != -1):
                                if(estado == linha[k].filhos[l].estado):#se o estado q11 for filho de q12

                                    altura = linha[k].altura + 1
                                    if (altura > alturaMaxima): alturaMaxima = altura

                                    filho1 = -1
                                    filho2 = -1

                                    if(pri != -1):
                                        filho1 = elemento(linha[k].filhos[l].altura + 1, linha[k].filhos[l], arvore, [-1, -1], valor, pri)
                                        linha.append(filho1)
                                    if(seg != -1):
                                        filho2 = elemento(linha[k].filhos[l].altura + 1, linha[k].filhos[l], arvore, [-1, -1], valor, seg)
                                        linha.append(filho2)

                                    filhos = [filho1, filho2]
                                    linha[k].filhos[l].filhos = filhos

                                    arvore = i
                                    break
                
        

            elif (serLido == 1):
                alfabetoRanqueado.append(texto)
            
            elif (serLido == 2):
                conjEstados.append(texto)
            else:
                conjEstadosFinal.append(texto)
    for tam_linha in range(len(linha)):
        #setattr(linha[tam_linha], 'aleatorio', '?')
        #delattr(linha[tam_linha], 'valor')
        print(linha[tam_linha])

    ultimaAlturaArvores.append(alturaMaxima)
    elementosArvore.append(linha)
    arq.close()

numAlturas = max(ultimaAlturaArvores) 

estadox1 = -1

for i in range(max(ultimaAlturaArvores) + 1):
    for j in range(numArvores):
        for k in range(len(elementosArvore[j])): #k vai de 0 até o máximo num_de_elementos daquela árvore
            if (elementosArvore[j][k].altura == numAlturas):
                setattr(elementosArvore[j][k], 'xi', -1)
                estado = singXI(elementosArvore[j][k], 1)
                elementosArvore[j][k].xi = estado
                print(elementosArvore[j][k].estado, estado, elementosArvore[j][k].valor[0])
                
                if (estado == -2):
                    ultimox1 = elementosArvore[j][k]
                    break

        if (estado == -2):
            break
    if (estado == -2):
        break



    numAlturas = numAlturas - 1

if(estado == -2):
    print("estado = {} falhou em {}".format(estado, ultimox1.estado))
elif(estado == 0):
    print("rodou e resultou em wait (estado 0)")
elif(estado == 1):
    print("Passou, uhul ")


        
    #numAlturas = numAlturas - 1
            
        