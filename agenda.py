import sys
import matplotlib.pyplot as plt

from typing import List

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


# comp = Compromisso(descricao)

class Compromisso:
    def __init__(self, descricao: str, prioridade: str = '',
                 data: str = '', hora: str = '', contexto: str = '', projeto: str = ''):

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

    def getDataOrdenacao(self):
        # TODO Usar Timestamp
        ano = 9999
        mes = 13
        dia = 32

        if self.data != '':
            ano = int(self.data[4:8])
            mes = int(self.data[2:4])
            dia = int(self.data[0:2])

        return (ano, mes, dia)

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


# Imprime texto com cores. Por exemplo, para imprimir "Oi mundo!" em vermelho, basta usar
#
# printCores('Oi mundo!', RED)
# printCores('Texto amarelo e negrito', YELLOW + BOLD)
def printCores(texto, cor):
    print(cor + texto + RESET)


# Adiciona um compromisso aa agenda. Um compromisso tem no minimo
# uma descrição. Adicionalmente, pode ter, em caráter opcional, uma
# data (formato DDMMAAAA), um horário (formato HHMM), uma prioridade de A a Z, 
# um contexto onde a atividade será realizada (precedido pelo caractere
# '@') e um projeto do qual faz parte (precedido pelo caractere '+'). Esses
# itens opcionais podem ser implementados como uma tupla, dicionário  ou objeto. A função
# recebe esse item através do parâmetro extras.
#
# extras tem como elementos data, hora, prioridade, contexto, projeto
#
def adicionar(novoCompromisso):
    # não é possível adicionar uma atividade que não possui descrição.
    if novoCompromisso.descricao == '':
        return False

    novaAtividade: str = novoCompromisso.stringTXT()

    # Escreve no TODO_FILE.
    try:
        fp = open(TODO_FILE, 'a')
        fp.write(novaAtividade + "\n")
    except IOError as err:
        print("Não foi possível escrever para o arquivo " + TODO_FILE)
        print(err)
        return False
    finally:
        fp.close()

    return True


# Valida a prioridade.
def prioridadeValida(pri: str):
    if len(pri) == 3:
        if pri[0] == "(" and pri[2] == ")":
            if soLetras(pri[1]):
                return True

    return False


# Valida a hora. Consideramos que o dia tem 24 horas, como no Brasil, ao invés
# de dois blocos de 12 (AM e PM), como nos EUA.
def horaValida(horaMin: str):
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


# Valida datas. Verificar inclusive se não estamos tentando
# colocar 31 dias em fevereiro. Não precisamos nos certificar, porém,
# de que um ano é bissexto. 
def dataValida(data: str):
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


# Valida que o string do projeto está no formato correto.
def projetoValido(proj: str):
    if len(proj) >= 2 and proj[0] == '+':
        return True

    return False


# Valida que o string do contexto está no formato correto.
def contextoValido(cont: str):
    if len(cont) >= 2 and cont[0] == '@':
        return True

    return False


# Valida que a data ou a hora contém apenas dígitos, desprezando espaços
# extras no início e no fim.
def soDigitos(numero):
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


def reverterSplit(tokens: List[str]) -> str:
    string: str = ''
    if len(tokens):
        string += tokens.pop(0)
        while len(tokens):
            string += " " + tokens.pop(0)

    return string


# Dadas as linhas de texto obtidas a partir do arquivo texto todo.txt, devolve
# uma lista de tuplas contendo os pedaços de cada linha, conforme o seguinte
# formato:
#
# (descrição, prioridade, (data, hora, contexto, projeto))
#
# É importante lembrar que linhas do arquivo todo.txt devem estar organizadas de acordo com o
# seguinte formato:
#
# DDMMAAAA HHMM (P) DESC @CONTEXT +PROJ
#
# Todos os itens menos DESC são opcionais. Se qualquer um deles estiver fora do formato, por exemplo,
# data que não tem todos os componentes ou prioridade com mais de um caractere (além dos parênteses),
# tudo que vier depois será considerado parte da descrição.
def organizar(linhas: List[str]) -> List[Compromisso]:
    itens: List[Compromisso] = []

    for l in linhas:
        data = ''
        hora = ''
        prioridade = ''
        descricao = ''
        contexto = ''
        projeto = ''

        l = l.strip()  # remove espaços em branco e quebras de linha do começo e do fim
        tokens = l.split()  # quebra o string em palavras

        # Processa os tokens um a um, verificando se são as partes da atividade.
        # Por exemplo, se o primeiro token é uma data válida, deve ser guardado
        # na variável data e posteriormente removido a lista de tokens. Feito isso,
        # é só repetir o processo verificando se o primeiro token é uma hora. Depois,
        # faz-se o mesmo para prioridade. Neste ponto, verifica-se os últimos tokens
        # para saber se são contexto e/ou projeto. Quando isso terminar, o que sobrar
        # corresponde à descrição. É só transformar a lista de tokens em um string e
        # construir a tupla com as informações disponíveis.
        tokensDescricao = []
        while len(tokens):
            token = tokens.pop(0)

            if dataValida(token):
                data = token
            elif horaValida(token):
                hora = token
            elif prioridadeValida(token):
                prioridade = token
            elif contextoValido(token):
                contexto = token
            elif projetoValido(token):
                projeto = token
            else:
                tokensDescricao.append(token)

        # descricao = ' '.join(tokensDescricao)
        # if len(tokensDescricao):
        descricao = reverterSplit(tokensDescricao)

        # A linha abaixo inclui em itens um objeto contendo as informações relativas aos compromissos
        # nas várias linhas do arquivo.
        itens.append(Compromisso(descricao, prioridade, data,
                                 hora, contexto, projeto))

    return itens


# Datas e horas são armazenadas nos formatos DDMMAAAA e HHMM, mas são exibidas
# como se espera (com os separadores apropridados). 
#
# Uma extensão possível é listar com base em diversos critérios: (i) atividades com certa prioridade;
# (ii) atividades a ser realizadas em certo contexto; (iii) atividades associadas com
# determinado projeto; (vi) atividades de determinado dia (data específica, hoje ou amanhã). Isso não
# é uma das tarefas básicas do projeto, porém.
def listar():
    try:
        arquivo = open(TODO_FILE, 'r')
    except IOError as err:
        print("Não foi possível ler para o arquivo " + TODO_FILE)
        print(err)
        return False

    # organizar([linha for linha in arquivo])
    linhas: List[str] = []
    for linha in arquivo:
        linhas.append(linha)

    listaCompromissos: List[Compromisso] = organizar(linhas)

    listaTuplasIndiceCompromisso = []

    for i, compromisso in enumerate(listaCompromissos):
        listaTuplasIndiceCompromisso.append((i, compromisso))

    listaTuplasOrdenadaData = ordenarPorDataHora(listaTuplasIndiceCompromisso)
    listaTuplasOrdenadaPrioridade = ordenarPorPrioridade(listaTuplasOrdenadaData)

    for tupla in listaTuplasOrdenadaPrioridade:
        string: str = str(tupla[0]) + ' ' + tupla[1].stringTXT()
        if tupla[1].getPrioridade() == 'A':
            printCores(string,
                       RED)  # TODO botar bold, não estamos conseguindo usar como especificado (RED + BOLD) fica só bold
        elif tupla[1].getPrioridade() == 'B':
            printCores(string, YELLOW)
        elif tupla[1].getPrioridade() == 'C':
            printCores(string, GREEN)
        elif tupla[1].getPrioridade() == 'D':
            printCores(string, BLUE)
        else:
            print(string)

    return True


def ordenarPorDataHora(itens: List[Compromisso]):
    return sorted(itens, key=lambda x: x[1].getDataOrdenacao())


def ordenarPorPrioridade(itens: List[Compromisso]):
    return sorted(itens, key=lambda x: x[1].getPrioridadeOrdenacao())


def fazer(num: int):
    linhas = []
    try:
        arquivo = open(TODO_FILE, 'r')
        for linha in arquivo:
            linhas.append(linha)
    except IOError as err:
        print("Não foi possível ler para o arquivo " + TODO_FILE)
        print(err)
        return False
    finally:
        arquivo.close()

    atividadeConcluida: str = linhas.pop(num)

    try:
        arquivo = open(ARCHIVE_FILE, 'a')
        arquivo.write(atividadeConcluida + "\n")
    except IOError as err:
        print("Não foi possível escrever para o arquivo " + ARCHIVE_FILE)
        print(err)
        return False
    finally:
        arquivo.close()

    try:
        arquivo = open(TODO_FILE, 'w')
        for linha in linhas:
            arquivo.write(linha)
    except IOError as err:
        print("Não foi possível abrir para escrita o arquivo " + TODO_FILE)
        print(err)
        return False
    finally:
        arquivo.close()

    return True


def remover(num: int):
    try:
        arquivo = open(TODO_FILE, 'r')
    except IOError as err:
        print("Não foi possível ler para o arquivo " + TODO_FILE)
        print(err)
        return False

    linhas = []
    for linha in arquivo:
        linhas.append(linha)

    if num >= len(linhas):
        print('Não há atividade para o indice selecionado')
        return False
    linhas.pop(num)

    arquivo.close()

    try:
        arquivo = open(TODO_FILE, 'w')
    except IOError as err:
        print("Não foi possível abrir para escrita o arquivo " + TODO_FILE)
        print(err)
        return False

    for linha in linhas:
        arquivo.write(linha)

    return True


# prioridade é uma letra entre A a Z, onde A é a mais alta e Z a mais baixa.
# num é o número da atividade cuja prioridade se planeja modificar, conforme
# exibido pelo comando 'l'. 
def priorizar(num: int, prioridade: str):
    try:
        arquivo = open(TODO_FILE, 'r')
    except IOError as err:
        print("Não foi possível ler para o arquivo " + TODO_FILE)
        print(err)
        return False

    linhas = []
    for linha in arquivo:
        linhas.append(linha)
    arquivo.close()

    if num >= len(linhas):
        print('Não há atividade para o indice selecionado')
        return False

    listaCompromissos = organizar(linhas)
    listaCompromissos[num].adicionarPrioridade('(' + prioridade + ')')

    try:
        arquivo = open(TODO_FILE, 'w')
    except IOError as err:
        print("Não foi possível abrir para escrita o arquivo " + TODO_FILE)
        print(err)
        return False

    for compromisso in listaCompromissos:
        arquivo.write(compromisso.stringTXT() + '\n')


def desenhar(dias: int):
    linhasCompletadas = []
    try:
        arquivo = open(ARCHIVE_FILE, 'r')
        for linha in arquivo:
            if linha != '\n':
                linhasCompletadas.append(linha)
    except IOError as err:
        print("Não foi possível ler o arquivo " + TODO_FILE)
        print(err)
        return False
    finally:
        arquivo.close()

    atividadesCompletadas = organizar(linhasCompletadas)
    atividadesCompletadas.sort(key=lambda x: x.getDataOrdenacao(), reverse=True)

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
    plt.plot(x, atividadesCompletadasPorDia)
    plt.show()

    return


# Esta função processa os comandos e informações passados através da linha de comando e identifica
# que função do programa deve ser invocada. Por exemplo, se o comando 'adicionar' foi usado,
# isso significa que a função adicionar() deve ser invocada para registrar a nova atividade.
# O bloco principal fica responsável também por tirar espaços em branco no início e fim dos strings
# usando o método strip(). Além disso, realiza a validação de horas, datas, prioridades, contextos e
# projetos. 
def processarComandos(comandos):
    if comandos[1] == ADICIONAR:
        comandos.pop(0)  # remove 'agenda.py'
        comandos.pop(0)  # remove 'adicionar'
        itemParaAdicionar: Compromisso = organizar([' '.join(comandos)])[0]
        adicionar(itemParaAdicionar)  # novos itens não têm prioridade
    elif comandos[1] == LISTAR:
        listar()
    elif comandos[1] == REMOVER:
        remover(int(comandos[2]))
        return
    elif comandos[1] == FAZER:
        fazer(int(comandos[2]))
        return
    elif comandos[1] == PRIORIZAR:
        priorizar(int(comandos[2]), comandos[3])
        return
    elif comandos[1] == DESENHAR:
        desenhar(int(comandos[2]))
        return
    else:
        print("Comando inválido.")


# sys.argv é uma lista de strings onde o primeiro elemento é o nome do programa
# invocado a partir da linha de comando e os elementos restantes são tudo que
# foi fornecido em sequência. Por exemplo, se o programa foi invocado como
#
# python3 agenda.py a Mudar de nome.
#
# sys.argv terá como conteúdo
#
# ['agenda.py', 'a', 'Mudar', 'de', 'nome']

# Main para possibilitar importar as funções para teste
if __name__ == "__main__":
    processarComandos(sys.argv)
