import copy
import heapq
import time
import tracemalloc

finalBoard =[[1,5,9,13],
            [2,6,10,14],
            [3,7,11,15],
            [4,8,12,0]]

elementsFinalPositions = [  [3, 3], [0, 0], [1, 0], [2, 0], 
                            [3, 0], [0, 1], [1, 1], [2, 1], 
                            [3, 1], [0, 2], [1, 2], [2, 2], 
                            [3, 2], [0, 3], [1, 3], [2, 3]]

# matriz que armazena o valor esperado na posicao i - 1
matrizEsperada = ["null",5,6,7,8,9,10,11,12,13,14,15,"null",2,3,4]


class Node:
    def __init__(self, tabuleiro,nodePai):
        self.tabuleiro = copy.deepcopy(tabuleiro)
        self.nodePai = nodePai
        self.G = 0
        self.H = 0
        self.F = 0


    def __lt__(self, other):
        return self.F < other.F


def main():
    valuesInput = input()

    board = FormataEntrada(valuesInput)

    start_time = time.time()

    path = A_estrela(board, finalBoard)

    ImprimirResult(path)

    print("Tempo de execução: %s segundos" % (time.time() - start_time))


def FormataEntrada(valuesInput):
    initialValuesSplited = valuesInput.split(' ')

    if (initialValuesSplited[0] == '' or initialValuesSplited[0] == ' '):
        initialValuesSplited.pop(0)

    lastIndex = len(initialValuesSplited)-1

    if (initialValuesSplited[lastIndex] == '' or initialValuesSplited[lastIndex] == ' '):
        initialValuesSplited.pop()

    initialBoard = []

    for x in initialValuesSplited:
        initialBoard.append(int(x))

    return ListaParaMatriz(initialBoard)
    

def ListaParaMatriz(lista):
    matriz = [  [0,0,0,0],
                [0,0,0,0],
                [0,0,0,0],
                [0,0,0,0]]
    k = 0

    for i in range(4):
        for j in range(4):
            matriz[i][j] = int(lista[k])
            k += 1
    
    return matriz


def heuristica1(board):
    result = 0

    for i in range(4):
        for j in range(4):
            if (board[i][j] != 0 and board[i][j] != finalBoard[i][j]):
                result += 1
    return result


def heuristica2(matriz):
    result = 0
    aux = []
    
    for i in range(4):
        for j in range(4):
            aux.append(matriz[i][j])

    for k in range(15):
        if (matrizEsperada[aux[k]] == "null"):
            continue
        if (aux[k+1] != matrizEsperada[aux[k]]):
            result += 1
    
    return result


def heuristica3(board):
    distancia_manhatan = 0
    for i in range(4):
        for j in range(4):
            if (board[i][j] != 0 and board[i][j] != finalBoard[i][j]):
                (u,v) = elementsFinalPositions[board[i][j]]
                distancia_manhatan += abs(i-u) + abs(j-v)

    return distancia_manhatan


def heuristica4(board):
    pesos = [0.4,0.2,0.4]
    h1 = heuristica1(board)
    h2 = heuristica2(board)
    h3 = heuristica3(board)
    result = pesos[0]*h1 + pesos[1]*h2 + pesos[2]*h3
    return result


def heuristica5(board):
    h1 = heuristica1(board)
    h2 = heuristica2(board)
    h3 = heuristica3(board)
    result = max(h1,h2,h3)
    return result


def BuscaEspacoVazio(board):
    for i in range(4):
        for j in range(4):
            if (board[i][j] == 0):
                return (i,j)


def TrocaPosicoes(board, peca1, peca2):
    (x, y) = peca1
    (u, v) = peca2
    newBoard = copy.deepcopy(board)
    newBoard[u][v] = board[x][y]
    newBoard[x][y] = board[u][v]
    return newBoard


def GeraSucessores(currentNode):
    (i, j) = BuscaEspacoVazio(currentNode.tabuleiro)
    children = []

    if (i - 1 >= 0):
        childBoard1 = TrocaPosicoes(currentNode.tabuleiro, (i,j), (i-1,j))
        childNode1 = Node(childBoard1, [])
        children.append(childNode1)
    if (i + 1 < 4):
        childBoard2 = TrocaPosicoes(currentNode.tabuleiro, (i,j), (i+1,j))
        childNode2 = Node(childBoard2, []) 
        children.append(childNode2)
    if (j - 1 >= 0):
        childBoard3 = TrocaPosicoes(currentNode.tabuleiro, (i,j), (i,j-1))
        childNode3 = Node(childBoard3, []) 
        children.append(childNode3)
    if (j + 1 < 4):
        childBoard4 = TrocaPosicoes(currentNode.tabuleiro, (i,j), (i,j+1))
        childNode4 = Node(childBoard4, []) 
        children.append(childNode4)

    return children


def A_estrela(initialBoard,finalBoard):
  
    A = {}
    F = {}
    heap = []
    heapq.heapify(heap)

    startNode = Node(initialBoard,None)
    finalNode = Node(finalBoard,None)

    A[str(startNode.tabuleiro)] = startNode

    heapq.heappush(heap, (startNode.F, startNode.tabuleiro))

    while (heap):
        currentNode = "null"

        while (currentNode == "null"):
            currentBoard = heapq.heappop(heap)[1]
            
            if (str(currentBoard) in A):
                currentNode = A[str(currentBoard)]

        if (currentNode.tabuleiro == finalBoard):     
            path = []
            
            while (currentNode.tabuleiro != initialBoard):
                path.append(currentNode.tabuleiro)
                currentNode = currentNode.nodePai
            
            return path[::-1]
          
        A.pop(str(currentNode.tabuleiro))
        F[str(currentNode.tabuleiro)] = currentNode

        successors = GeraSucessores(currentNode)

        for childNode in successors:
            g = currentNode.G + 1

            if (str(childNode.tabuleiro) in F):
                continue

            if (str(childNode.tabuleiro) in A) and (A[str(childNode.tabuleiro)].G > g):
                A.pop(str(childNode.tabuleiro))
            
            if (str(childNode.tabuleiro) not in A):
                A[str(childNode.tabuleiro)] = childNode
                A[str(childNode.tabuleiro)].nodePai = currentNode
                A[str(childNode.tabuleiro)].G = g
                A[str(childNode.tabuleiro)].H = heuristica3(childNode.tabuleiro)
                A[str(childNode.tabuleiro)].F = A[str(childNode.tabuleiro)].G + A[str(childNode.tabuleiro)].H
                heapq.heappush(heap, (A[str(childNode.tabuleiro)].F, childNode.tabuleiro))

    return None


def ImprimirMatriz(matriz):
    x = PrettyTable()
    x.title = "Board"
    x.header = False
    x.padding_width = 1
    
    for linha in matriz:
        x.add_row(linha)
    
    print(x)


def ImprimirResult(path):
    if path is not None:
        print("Resposta:", len(path))
    else:
        print('Não foi encontrado nenhum caminho')


if __name__ == '__main__':
    tracemalloc.start()
    main()
    atual,maior=tracemalloc.get_traced_memory()
    print(f"consumo atual de memoria: {atual/10**6}MB;O pico maior foi {maior/10**6}MB")
    tracemalloc.stop()