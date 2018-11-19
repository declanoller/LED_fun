

dict_str = '{'

alphabet = 'abcdefghijklmnopqrstuvwxyz'

for i in range(len(alphabet)):

    dict_str += ('\'' + alphabet[i] + '\': letter' + str(i) + ', \n')


dict_str += '}'

print(dict_str)
