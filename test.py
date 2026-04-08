from re import fullmatch, escape


syms = '!@#$%^&*()_+-?='
pattern = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*["+escape(syms)+"])[A-Za-z\\d"+escape(syms)+"]{8,}$"
if fullmatch(pattern, input()):
    print(1)
else:
    print(0)