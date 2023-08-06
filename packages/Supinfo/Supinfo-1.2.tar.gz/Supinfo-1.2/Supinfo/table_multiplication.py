"""
Tables de multiplication
version 1.0
"""
def multiplication(nombre):
    for i in range(11):
        print(f'{nombre} x {i} = {nombre*i} \t', end='')
        print("\t")

 

if __name__ == "__main__":
    nombre = int(input("Donner un nombre: "))
    multiplication(nombre)
