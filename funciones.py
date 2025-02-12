def leerER(file):
    with open(file, "r") as f:
        for line in f:
            print('La expresion regular es: ',line)
        return line