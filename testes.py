import agenda

# Testes tarefa 3, função horaValida()
print("-----------------------------------")
print("Testes função horaValida()")
print(agenda.horaValida("000000")==False)
print(agenda.horaValida("aaaaaa")==False)
print(agenda.horaValida("0000")==True)
print(agenda.horaValida("2359")==True)
print(agenda.horaValida("2400")==False)
print(agenda.horaValida("12:30")==False)
print(agenda.horaValida("1135")==True)
print("-----------------------------------")

# Testes tarefa 4, função dataValida()
print("-----------------------------------")
print("Testes função dataValida()")
print(agenda.dataValida("20042020")==True)
print(agenda.dataValida("33042020")==False)
print(agenda.dataValida("30022020")==False)
print(agenda.dataValida("20132020")==False)
print(agenda.dataValida("31042020")==False)
print(agenda.dataValida("100220")==False)
print(agenda.dataValida("472928828")==False)
print("-----------------------------------")
