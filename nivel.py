import re

class elemento(object):
    def __init__(self, altura, anterior, arvore, no):
        self.altura = altura 
        self.anterior = anterior
        self.arvore = arvore
        self.no = no
        self.filhos = []

    def __str__(self):
        teste = "A altura é {}, anterior é {}, da arvore {}, com no {} e filhos {} \n".format(self.altura, self.anterior, self.arvore, self.no, self.filhos)
        return teste

class transicao(object):
    def __init__(self, antes, depois, antesPri, antesSeg):
        self.antes = antes
        self.depois = depois
        self.antesPri = antesPri
        self.antesSeg = antesSeg

    def __str__(self):
        teste = "{}({},{})->{}\n".format(self.antes, self.antesPri, self.antesSeg, self.depois)
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

numArvores = 2
elementoArvore = []
ultimaAlturaArvores = [] 
alfabetoRanqueado = []


#indice da coluna é num da arvore
#indice da linha é o node_id daquela árvore
for i in range(numArvores):
    alturaMaxima = 0
    nomeArq = "tree" + str(i) + ".txt"
    tamanhoArq = numLinhas(nomeArq)
    arq = open(nomeArq)
    linha = [-1] * (tamanhoArq+1)
    for j in range(tamanhoArq):
        texto = arq.readline()

        priNo, segNo = texto.split(' -> ')
        segNo = segNo.strip()

        if(j == 0 and "#" in priNo):
            priNo, priIgual = priNo.split("#")
            pri = int(priNo.partition('N')[2])
            if(priIgual in alfabetoRanqueado): 
                priNo = priIgual
            else: 
                alfabetoRanqueado.append(priNo)
        else: 
            pri = int(priNo.partition('N')[2])
            if(j == 0): alfabetoRanqueado.append(priNo)
        if("#" in segNo): 
            segNo, segIgual = segNo.split("#")
            seg = int(segNo.partition('N')[2])
            if(segIgual in alfabetoRanqueado): 
                segNo= segIgual
            else: 
                alfabetoRanqueado.append(segNo)
        else:
            alfabetoRanqueado.append(segNo)
            seg = int(segNo.partition('N')[2])

        if (j == 0):
            linha[pri] = elemento(0, -1, i, priNo)
        print(pri, seg)
        linha[seg] = elemento(linha[pri].altura+1, linha[pri], i, segNo)
        linha[pri].filhos.append(linha[seg]) 
        if(linha[seg].altura > alturaMaxima): alturaMaxima = linha[seg].altura

    ultimaAlturaArvores.append(alturaMaxima)
    elementoArvore.append(linha)
    arq.close()

transicoes = []
conjEstados = []
conjEstadosFinal = []
numAlturas = max(ultimaAlturaArvores)
numTransicaoDepois = 0
for i in range(numArvores):
    for j in range(len(elementoArvore[i])):
        print(elementoArvore[i][j].no)


for i in range(max(ultimaAlturaArvores)+1):
    for j in range(numArvores):
        for k in range(len(elementoArvore[j])):
            if (elementoArvore[j][k].altura == numAlturas):
                if(len(elementoArvore[j][k].filhos) == 0): 
                    ant = -1 
                    dep = -1
                elif (len(elementoArvore[j][k].filhos) == 1):
                    ant = elementoArvore[j][k].filhos[0].no
                    dep = -1
                else:
                    ant = elementoArvore[j][k].filhos[0].no
                    dep = elementoArvore[j][k].filhos[1].no

                teveTransicao = 0
                
                
                for l in range(len(transicoes)):
                    #se tiver uma transição compatível:
                    if (elementoArvore[j][k].no == transicoes[l].antes and 
                    transicoes[l].antesPri == ant and transicoes[l].antesSeg == dep):
                        teveTransicao = 1
                        elementoArvore[j][k].no = transicoes[l].depois
                        if(elementoArvore[j][k].altura == 0): conjEstadosFinal.append(elementoArvore[j][k].no)
                        break


                if (teveTransicao == 0):
                    estado = "q" + str(numTransicaoDepois)
                    numTransicaoDepois = numTransicaoDepois + 1
                    conjEstados.append(estado)
                    if(elementoArvore[j][k].altura == 0): conjEstadosFinal.append(estado)
                    transicoes.append(transicao(elementoArvore[j][k].no, estado, ant, dep))
                    elementoArvore[j][k].no = estado
                
    numAlturas = numAlturas - 1
                        
                
 

print()
print("Conjunto de estados: \n", conjEstados)
print()
print("Conjunto de estados finais: \n", conjEstadosFinal)
print()
print("Transições:")
for i in range(len(transicoes)):
    print(transicoes[i])
