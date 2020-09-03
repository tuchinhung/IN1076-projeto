import sys
import time
import matplotlib.pyplot as plt

from datetime import datetime
from typing import List, Tuple

TODO_FILE = 'todo.txt'
ARCHIVE_FILE = 'done.txt'

RED = "\033[1;31m"
BLUE = "\033[1;34m"
CYAN = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD = "\033[;1m"
REVERSE = "\033[;7m"
YELLOW = "\033[0;33m"

ADICIONAR = 'a'
REMOVER = 'r'
FAZER = 'f'
PRIORIZAR = 'p'
LISTAR = 'l'
DESENHAR = 'g'


class Compromisso:
    def __init__(self, descricao: str, prioridade: str = '', data: str = '',
                hora: str = '', contexto: str = '', projeto: str = ''):

        self.descricao: str = descricao
        self.prioridade: str = ''
        self.data: str = ''
        self.hora: str = ''
        self.contexto: str = ''
        self.projeto: str = ''

        self.adicionarPrioridade(prioridade)
        self.adicionarData(data)
        self.adicionarHora(hora)
        self.adicionarContexto(contexto)
        self.adicionarProjeto(projeto)


    def adicionarPrioridade(self, prioridade: str):
        if prioridadeValida(prioridade):
            self.prioridade = prioridade
            return True
        return False

    def adicionarData(self, data: str):
        if dataValida(data):
            self.data = data

    def adicionarHora(self, hora: str):
        if horaValida(hora):
            self.hora = hora

    def adicionarContexto(self, contexto: str):
        if contextoValido(contexto):
            self.contexto = contexto

    def adicionarProjeto(self, projeto: str):
        if projetoValido(projeto):
            self.projeto = projeto

    def getPrioridade(self) -> str:
        if self.prioridade != '':
            return self.prioridade[1]

        return ''

    def getDatetime(self):
        if self.data == '' and self.hora == '':
            data = datetime.max
        elif self.data != '' and self.hora == '':
            data = datetime.strptime(self.data, "%d%m%Y")
        elif self.data == '' and self.hora != '':
            dataMaxima = '31129999'
            data = datetime.strptime(dataMaxima + self.hora, "%d%m%Y%H%M")
        else:
            data = datetime.strptime(self.data + self.hora, "%d%m%Y%H%M")

        return data

    def getPrioridadeOrdenacao(self):
        prioridade = 'ZZ'

        if self.prioridade != '':
            prioridade = self.prioridade[1]

        return prioridade

    def stringTXT(self):
        texto: str = ''
        if self.data != '':
            texto += self.data + ' '

        if self.hora != '':
            texto += self.hora + ' '

        if self.prioridade != '':
            texto += self.prioridade + ' '

        if self.descricao != '':
            texto += self.descricao

        if self.contexto != '':
            texto += ' ' + self.contexto

        if self.projeto != '':
            texto += ' ' + self.projeto

        return texto

    def stringTerminal(self):
        texto: str = ''

        if self.data != '':
            texto += self.data[0:2] + '/' + self.data[2:4] + '/' + self.data[4:8] + ' '

        if self.hora != '':
            texto += self.hora[0:2] + 'h' + self.hora[2:4] + 'm' + ' '

        if self.prioridade != '':
            texto += self.prioridade + ' '

        if self.descricao != '':
            texto += self.descricao

        if self.contexto != '':
            texto += ' ' + self.contexto

        if self.projeto != '':
            texto += ' ' + self.projeto

        return texto

def organizar(linhas: List[str]) -> List[Compromisso]:
    '''
    Dada uma lista de linhas de texto, 
    devove uma lista de objetos do tipo Compromisso

    É importante lembrar que linhas do arquivo todo.txt devem estar organizadas 
    de acordo com o seguinte formato:

    DDMMAAAA HHMM (P) DESC @CONTEXT +PROJ

    Todos os itens menos DESC são opcionais. Se qualquer um deles estiver fora 
    do formato, por exemplo, data que não tem todos os componentes ou prioridade
    com mais de um caractere (além dos parênteses), tudo que vier depois será 
    considerado parte da descrição.
    '''
    compromissos: List[Compromisso] = []

    for l in linhas:
        data:str = ''
        hora:str = ''
        prioridade:str = ''
        descricao:str = ''
        contexto:str = ''
        projeto:str = ''

        l = l.strip()  # remove espaços em branco e quebras de linha
        tokens:List[str] = l.split()  # quebra o string em palavras

        # Checa os primeiros tokens por data, hora e prioridade
        if len(tokens) and dataValida(tokens[0]):
            data = tokens.pop(0)
        if len(tokens) and horaValida(tokens[0]):
            hora = tokens.pop(0)
        if len(tokens) and prioridadeValida(tokens[0]):
            prioridade = tokens.pop(0)
        
        # Checa os ultimos tokens por projeto e contexto
        if len(tokens) and projetoValido(tokens[-1]):
            projeto = tokens.pop(-1)
        if len(tokens) and contextoValido(tokens[-1]):
            contexto = tokens.pop(-1)
        
        # A logica utilizada acima permite que o usuario use formatos na
        # descrição sem que sejam confundidos com os itens opcionais 

        # Reverte uma lista de tokens para uma string separada por espaços
        descricao = reverterSplit(tokens)

        # A linha abaixo inclui em compromissos um objeto contendo as 
        # informações relativas aos compromissos nas várias linhas do arquivo.
        compromissos.append(Compromisso(descricao=descricao,
                            prioridade=prioridade, data=data, hora=hora,
                            contexto=contexto, projeto=projeto))

    return compromissos

def reverterSplit(tokens: List[str]) -> str:
    '''
    Junta uma lista de palavras em uma unica linha, separada por espaços
    '''
    string: str = ''
    # Checa primeiro se a lista de tokens não esta vazia
    if len(tokens):
        string += tokens.pop(0)
        while len(tokens):
            string += " " + tokens.pop(0)

    return string

def adicionar(novoCompromisso: Compromisso) -> bool:
    '''
    Adiciona um compromisso aa agenda. Um compromisso tem no minimo
    uma descrição. Adicionalmente, pode ter, em caráter opcional, uma
    data (formato DDMMAAAA), um horário (formato HHMM), uma prioridade de A a Z, 
    um contexto onde a atividade será realizada (precedido pelo caractere
    '@') e um projeto do qual faz parte (precedido pelo caractere '+'). Esses
    itens opcionais podem ser implementados como uma tupla, dicionário 
    ou objeto. A função recebe esse item através do parâmetro extras.

    extras tem como elementos data, hora, prioridade, contexto, projeto
    '''
    # não é possível adicionar uma atividade que não possui descrição.
    if novoCompromisso.descricao == '':
        print("Não é possível adicionar uma atividade que não possui descrição")
        return False

    novaAtividade: str = novoCompromisso.stringTXT()

    # Escreve atividade no TODO_FILE.
    try:
        arquivoTODO = open(TODO_FILE, 'a')
        arquivoTODO.write(novaAtividade + "\n")
    except IOError as err:
        print("Não foi possível escrever para o arquivo " + TODO_FILE)
        print(err)
        return False
    finally:
        arquivoTODO.close()

    return True

def listar() -> bool:
    '''
    Datas e horas são armazenadas nos formatos DDMMAAAA e HHMM, mas são exibidas
    como se espera (com os separadores apropridados). 

    TODO Uma extensão possível é listar com base em diversos critérios: (i) atividades com certa prioridade;
    (ii) atividades a ser realizadas em certo contexto; (iii) atividades associadas com
    determinado projeto; (vi) atividades de determinado dia (data específica, hoje ou amanhã). Isso não
    é uma das tarefas básicas do projeto, porém.
    '''
    linhas: List[str] = []

    # Lê linhas do arquivo todo.txt e adciona suas linhas a uma lista de strings
    try:
        arquivoTODO = open(TODO_FILE, 'r')
        for linha in arquivoTODO:
            linhas.append(linha)
    except IOError as err:
        print("Não foi possível ler para o arquivo " + TODO_FILE)
        print(err)
        return False
    finally:
        arquivoTODO.close()

    # Retorna uma lista de objetos compromisso a partir das linhas do arquivo
    listaCompromissos: List[Compromisso] = organizar(linhas)

    # Converte a lista de objetos Compromisso para uma 
    # lista de tuplas (indice, Compromisso), para manter identificar a linha do
    # arquivo após operação de ordenação
    listaTuplasIndiceCompromisso = []
    for i, compromisso in enumerate(listaCompromissos):
        listaTuplasIndiceCompromisso.append((i, compromisso))

    # Ordena a lista por data e hora
    listaTuplasOrdenadaData = ordenarTuplasPorDataHora(listaTuplasIndiceCompromisso)

    # Ordena a lista por prioridade, mantendo ordem por data e hora nos casos com mesma
    # prioridade
    listaTuplasOrdenadaPrioridade = ordenarTuplasPorPrioridade(listaTuplasOrdenadaData)


    # Imprime no terminal as atividade ordenadas, utilizando cores para 
    # distinguir prioridades de A a D
    for tupla in listaTuplasOrdenadaPrioridade:
        string: str = str(tupla[0]) + ' ' + tupla[1].stringTerminal()
        if tupla[1].getPrioridade() == 'A':
            printCores(string, RED + BOLD)  # TODO botar bold, não estamos conseguindo usar como especificado (RED + BOLD) fica só bold
        elif tupla[1].getPrioridade() == 'B':
            printCores(string, YELLOW)
        elif tupla[1].getPrioridade() == 'C':
            printCores(string, GREEN)
        elif tupla[1].getPrioridade() == 'D':
            printCores(string, BLUE)
        else:
            print(string)

    return True

def ordenarTuplasPorDataHora(itens: List[Tuple[int, Compromisso]]) -> List[Tuple[int, Compromisso]]:
    if itens == []:
        return []
    else:
        pivo:Tuple[int, Compromisso] = itens.pop(0)
        menores:List[Tuple[int, Compromisso]] = [x for x in itens if x[1].getDatetime() < pivo[1].getDatetime()]
        maiores:List[Tuple[int, Compromisso]] = [y for y in itens if y[1].getDatetime() >= pivo[1].getDatetime()]
    return ordenarTuplasPorDataHora(menores) + [pivo] + ordenarTuplasPorDataHora(maiores)

def ordenarTuplasPorPrioridade(itens: List[Tuple[int, Compromisso]]) -> List[Tuple[int, Compromisso]]:
    if itens == []:
        return []
    else:
        pivo:Tuple[int, Compromisso] = itens.pop(0)
        menores:List[Tuple[int, Compromisso]] = [x for x in itens if x[1].getPrioridadeOrdenacao() < pivo[1].getPrioridadeOrdenacao()]
        maiores: List[Tuple[int, Compromisso]] = [y for y in itens if y[1].getPrioridadeOrdenacao() >= pivo[1].getPrioridadeOrdenacao()]

    return ordenarTuplasPorPrioridade(menores) + [pivo] + ordenarTuplasPorPrioridade(maiores)

def printCores(texto, cor):
    '''
    Imprime texto com cores. Por exemplo, para imprimir "Oi mundo!" em vermelho, basta usar

    printCores('Oi mundo!', RED)
    printCores('Texto amarelo e negrito', YELLOW + BOLD)
    '''
    print(cor + texto + RESET)

def prioridadeValida(pri: str):
    '''Valida a prioridade.'''
    if len(pri) == 3:
        if pri[0] == "(" and pri[2] == ")":
            if soLetras(pri[1]):
                return True

    return False

def horaValida(horaMin: str):
    '''
    Valida a hora. Consideramos que o dia tem 24 horas, como no Brasil, ao invés
    de dois blocos de 12 (AM e PM), como nos EUA.
    '''
    if len(horaMin) != 4 or not soDigitos(horaMin):
        return False
    else:
        horas: int = int(horaMin[0:2])
        minutos: int = int(horaMin[2:4])

        # Hora precisa ser entre 00 e 23
        if horas < 0 or horas > 23:
            return False

        # Minuto precisa ser entre 00 e 59
        if minutos < 0 or minutos > 59:
            return False

        return True

def dataValida(data: str):
    '''
    Valida datas. Verificar inclusive se não estamos tentando
    colocar 31 dias em fevereiro. Não precisamos nos certificar, porém,
    de que um ano é bissexto. 
    '''
    if len(data) != 8 or not soDigitos(data):
        return False
    else:
        dia: int = int(data[0:2])
        mes: int = int(data[2:4])

        # Caso mês de 31 dias
        if mes in [1, 3, 5, 7, 8, 10, 12]:
            nDiasMes: int = 31
        # Caso mês de 30 dias
        elif mes in [4, 6, 9, 11]:
            nDiasMes: int = 30
        # Caso fevereiro
        elif mes == 2:
            nDiasMes: int = 29
        # Nenhum dos casos = mes invalido
        else:
            return False

        # Dia precisa ser entre 1 e numero de dias no mês
        if dia < 0 or dia > nDiasMes:
            return False
        else:
            return True

def projetoValido(proj: str):
    '''
    Valida que o string do projeto está no formato correto.
    '''
    if len(proj) >= 2 and proj[0] == '+':
        return True

    return False

def contextoValido(cont: str):
    '''Valida que o string do contexto está no formato correto.'''
    if len(cont) >= 2 and cont[0] == '@':
        return True

    return False

def soDigitos(numero: str):
    '''
    Valida que a data ou a hora contém apenas dígitos, desprezando espaços
    extras no início e no fim.
    '''
    if type(numero) != str:
        return False
    for x in numero:
        if x < '0' or x > '9':
            return False
    return True

def soLetras(palavra):
    if type(palavra) != str:
        return False
    palavraMinusculo: str = palavra.lower()

    for caractere in palavraMinusculo:
        if caractere < 'a' or caractere > 'z':
            return False

    return True

def fazer(num: int):
    linhas:List[str] = []

    # ler linhas do arquivo txt e adiciona suas linhas em uma lista "linhas"
    try:
        arquivoTODO = open(TODO_FILE, 'r')
        for linha in arquivoTODO:
            linhas.append(linha)
    except IOError as err:
        print("Não foi possível ler para o arquivo " + TODO_FILE)
        print(err)
        return False
    finally:
        arquivoTODO.close()

    # verificação se o usuário selecionou uma linha válida, a partir do seu índice
    if num >= len(linhas):
        print('Não há atividade para o indice selecionado')
        return False
    atividadeConcluida: str = linhas.pop(num)

    # Abre como escrita o arquivo done para salvar a atividade concluída
    try:
        arquivoDONE = open(ARCHIVE_FILE, 'a')
        arquivoTODO = open(TODO_FILE, 'w')

        arquivoDONE.write(atividadeConcluida + "\n")
        for linha in linhas:
            arquivoTODO.write(linha)

    except IOError as err:
        print("Não foi possível escrever para os arquivos " + ARCHIVE_FILE + ' e ' + TODO_FILE)
        print(err)
        return False
    finally:
        arquivoDONE.close()
        arquivoTODO.close()

    return True

def remover(num: int) -> bool:

    linhas:List[str] = []
    # ler linhas do arquivo txt e adiciona suas linhas em uma lista "linhas"
    try:
        arquivoTODO = open(TODO_FILE, 'r')
        for linha in arquivoTODO:
            linhas.append(linha)
    except IOError as err:
        print("Não foi possível ler para o arquivo " + TODO_FILE)
        print(err)
        return False
    finally:
        arquivoTODO.close()

    # verificação se o usuário selecionou uma linha válida, a partir do seu índice
    if num >= len(linhas):
        print('Não há atividade para o indice selecionado')
        return False
    #remove linha selecionada pelo usuário
    linhas.pop(num)

    #reabertura do arquivo para reescrevê-lo sem a linha indesejada
    try:
        arquivoTODO = open(TODO_FILE, 'w')
        for linha in linhas:
            arquivoTODO.write(linha)
    except IOError as err:
        print("Não foi possível abrir para escrita o arquivo " + TODO_FILE)
        print(err)
        return False
    finally:
        arquivoTODO.close()

    return True

def priorizar(num: int, prioridade: str) -> True:
    '''
    prioridade é uma letra entre A a Z, onde A é a mais alta e Z a mais baixa.
    num é o número da atividade cuja prioridade se planeja modificar, conforme
    exibido pelo comando 'l'. 
    '''
    linhas:List[str] = []
    # ler linhas do arquivo txt e adiciona suas linhas em uma lista "linhas"
    try:
        arquivoTODO = open(TODO_FILE, 'r')
        for linha in arquivoTODO:
            linhas.append(linha)
    except IOError as err:
        print("Não foi possível ler para o arquivo " + TODO_FILE)
        print(err)
        return False
    finally:
        arquivoTODO.close()

    # verificação se o usuário selecionou uma linha válida, a partir do seu índice
    if num >= len(linhas):
        print('Não há atividade para o indice selecionado')
        return False

    # Transforma as linhas de string em uma lista de objetos "Compromisso"
    listaCompromissos:List[Compromisso] = organizar(linhas)

    # Verifica se usuario digitou uma prioridade no formato valido
    prioridade = '(' + prioridade.upper() + ')'
    if not prioridadeValida(prioridade):
        print("Fomato da prioridade fornecida não é valida")
        print("Forneça uma prioridade entre 'A'e 'Z'")
        return False

    # Adiciona ao compromisso selecionado, a prioridade indicada
    listaCompromissos[num].adicionarPrioridade(prioridade)

    #reabertura do arquivo para reescrevê-lo com a prioridade atualizada
    try:
        arquivoTODO = open(TODO_FILE, 'w')
        for compromisso in listaCompromissos:
            arquivoTODO.write(compromisso.stringTXT() + '\n')
    except IOError as err:
        print("Não foi possível abrir para escrita o arquivo " + TODO_FILE)
        print(err)
        return False
    finally:
        arquivoTODO.close()

    return True

def desenhar(dias: int):
    linhasCompletadas:List[str] = []
    # ler linhas do arquivo txt e adiciona suas linhas em uma lista "linhasCompletadas"
    try:
        arquivoDONE = open(ARCHIVE_FILE, 'r')
        for linha in arquivoDONE:
            if linha != '\n':
                linhasCompletadas.append(linha)
    except IOError as err:
        print("Não foi possível ler o arquivo " + TODO_FILE)
        print(err)
        return False
    finally:
        arquivoDONE.close()

    # Transforma as linhas de string em uma lista de objetos "Compromisso"
    atividadesCompletadas:List[Compromisso] = organizar(linhasCompletadas)


    dataUltimaAtividadeCompletada = (0, 0, 0)
    atividadesCompletadasPorDia = [0] * dias  # [0, 0, 0, 0, 0]
    for atividade in atividadesCompletadas:
        if atividade.data == '':
            break
        if dataUltimaAtividadeCompletada == (0, 0, 0):
            dataUltimaAtividadeCompletada = atividade.getDataOrdenacao()
            atividadesCompletadasPorDia[0] += 1
        else:
            dataAtividade = atividade.getDataOrdenacao()
            x = dataUltimaAtividadeCompletada[2] - dataAtividade[
                2]  # TODO SÓ CONSIDERA DIFERENCA DA DATA DO DIA, NÃO FUNCIONA PARA DIAS EM MESES DIFERENTE
            if x > dias:
                break
            atividadesCompletadasPorDia[x] += 1

    atividadesCompletadasPorDia.reverse()

    x = range(dias)  # [0, 1, 2 , 3, 4]
    # TODO CONFIGURAR O GRAFICO
    #plt.plot(x, atividadesCompletadasPorDia)
    #plt.title('ATIVIDADES REALIZADAS')

    fig, axs = plt.subplots()
    axs.bar(x, atividadesCompletadasPorDia)
    #axs[1].scatter(names, values)
    #axs[2].plot(names, values)
    #fig.suptitle('FELIPE ROCKS')
    plt.title('ATIVIDADES REALIZADAS')
    plt.xlabel('dias')
    plt.ylabel('quantidade de atividades realizadas')
    plt.show()

    return

def processarComandos(comandos):
    '''
    Esta função processa os comandos e informações passados através da linha de comando e identifica
    que função do programa deve ser invocada. Por exemplo, se o comando 'adicionar' foi usado,
    isso significa que a função adicionar() deve ser invocada para registrar a nova atividade.
    O bloco principal fica responsável também por tirar espaços em branco no início e fim dos strings
    usando o método strip(). Além disso, realiza a validação de horas, datas, prioridades, contextos e
    projetos. 
    '''
    if len(comandos) > 1:
        if comandos[1] == ADICIONAR:
            comandos.pop(0)  # remove 'agenda.py'
            comandos.pop(0)  # remove 'adicionar'
            itemParaAdicionar: Compromisso = organizar([' '.join(comandos)])[0]
            if adicionar(itemParaAdicionar):  # novos itens não têm prioridade
                print("Atividade adicionada com sucesso à agenda")
        elif comandos[1] == LISTAR:
            listar()
        elif comandos[1] == REMOVER:
            # Verifica se usuario entrou a quantidade de argumentos correto
            # Verifica se usuario digitou indice numerico
            # A função remover verifica se indice digitado corresponde a uma linha
            if len(comandos) != 3:
                print("Uso invalido do comando REMOVER")
                print("Uso: python agenda.py r (indice da atividade)")
            elif not soDigitos(comandos[2]):
                print("Indice da atividade precisa ser um valor numerico")
            elif remover(int(comandos[2])):
                print("Atividade removida com sucesso")
        elif comandos[1] == FAZER:
            # Verifica se usuario entrou a quantidade de argumentos correto
            # Verifica se usuario digitou indice numerico
            # A função fazer verifica se indice digitado corresponde a uma linha
            if len(comandos) != 3:
                print("Uso invalido do comando FAZER")
                print("Uso: python agenda.py f (indice da atividade)")
            elif not soDigitos(comandos[2]):
                print("Indice da atividade precisa ser um valor numerico")
            elif fazer(int(comandos[2])):
                print ("Atividade marcada como concluída com sucesso")
        elif comandos[1] == PRIORIZAR:
            # Verifica se usuario entrou a quantidade de argumentos correto
            # Verifica se usuario digitou indice numerico
            # A função priorizar verifica se indice digitado corresponde a uma linha
            # e se a prioridade digitada é valida
            if len(comandos) != 4:
                print("Uso invalido do comando PRIORIZAR")
                print("Uso: python agenda.py p (indice da atividade) (prioridade)")
            elif not soDigitos(comandos[2]):
                print("Indice da atividade precisa ser um valor numerico")
            elif priorizar(int(comandos[2]), comandos[3]):
                print("Prioridade atualizada com sucesso")
        elif comandos[1] == DESENHAR:
            # Verifica se usuario entrou a quantidade de argumentos correto
            # Verifica se usuario digitou um numero de dias numerico
            if len(comandos) != 3:
                print("Uso invalido do comando DESENHAR")
                print("Uso: python agenda.py g (dias)")
            elif not soDigitos(comandos[2]):
                print("Numero de dias precisa ser um valor numerico")
            else:
                desenhar(int(comandos[2]))
        else:
            print("Comando inválido.")
    else:
        print("É preciso mandar um comando na chamada da função")
        print("Uso: python agenda.py (comando)")

if __name__ == "__main__":
    '''
    sys.argv é uma lista de strings onde o primeiro elemento é o nome do programa
    invocado a partir da linha de comando e os elementos restantes são tudo que
    foi fornecido em sequência. Por exemplo, se o programa foi invocado como

    python3 agenda.py a Mudar de nome.

    sys.argv terá como conteúdo

    ['agenda.py', 'a', 'Mudar', 'de', 'nome']
    Main para possibilitar importar as funções para teste
    '''

    processarComandos(sys.argv)

