import agenda

# Testes tarefa 3, função horaValida()
print("Testes função horaValida()")
assert(agenda.horaValida("000000")==False)
assert(agenda.horaValida("aaaaaa")==False)
assert(agenda.horaValida("0000")==True)
assert(agenda.horaValida("2359")==True)
assert(agenda.horaValida("2400")==False)
assert(agenda.horaValida("12:30")==False)
assert(agenda.horaValida("1135")==True)

# Testes tarefa 4, função dataValida()
print("Testes função dataValida()")
assert(agenda.dataValida("20042020")==True)
assert(agenda.dataValida("33042020")==False)
assert(agenda.dataValida("30022020")==False)
assert(agenda.dataValida("20132020")==False)
assert(agenda.dataValida("31042020")==False)
assert(agenda.dataValida("100220")==False)
assert(agenda.dataValida("472928828")==False)

#Testes tarefa 5, função projetoValido()
print("Testes função projetoValido()")
assert(agenda.projetoValido("+Oi tudo bom")==True)
assert(agenda.projetoValido("+2")==True)
assert(agenda.projetoValido("+")==False)
assert(agenda.projetoValido("aapokdap")==False)
assert(agenda.projetoValido("")==False)

#Testes tarefa 6, função contextoValido()
print("Testes função contextoValido()")
assert(agenda.contextoValido("@casa")==True)
assert(agenda.contextoValido("@apsokdapsdka")==True)
assert(agenda.contextoValido("")==False)
assert(agenda.contextoValido("@")==False)
assert(agenda.contextoValido("+38")==False)

#Testes função soLetras()
print("Testes função soLetras")
assert(agenda.soLetras("apskodsapdk3232poskpoaksd")==False)
assert(agenda.soLetras(" ")==False)
assert(agenda.soLetras("aaposdk")==True)
assert(agenda.soLetras("912839")==False)
assert(agenda.soLetras("*¨*(APSOKD")==False)
assert(agenda.soLetras("A")==True)


if not agenda.prioridadeValida("(a)")==False:
    raise Exception

#Testes tarefa 7, função prioridadeValida()
print("Testes função prioridadeValida()")
assert(agenda.prioridadeValida("(a)")==True)
assert(agenda.prioridadeValida("(A)")==True)
assert(agenda.prioridadeValida("ASPODKAPODK")==False)
assert(agenda.prioridadeValida("( )")==False)
assert(agenda.prioridadeValida("()")==False)
assert(agenda.prioridadeValida("(7)")==False)
assert(agenda.prioridadeValida("A") == False)
assert(agenda.prioridadeValida("") == False)






