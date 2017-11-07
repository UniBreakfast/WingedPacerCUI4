
# Импортирую функцию для отлавливания кодов нажатых клавиш в консоли
from msvcrt import getch

# Список префиксов, с которых могут начинаться двусложные коды клавиш или комбинаций
keycode_prefixes = [b'\x00', b'\xe0']

# Словари приемлемых кодов и соответствующих им названий клавиш и комбинаций
numbers = {b'0': 0, b'2': 2, b'4': 4, b'6': 6, b'8': 8, 
           b'1': 1, b'3': 3, b'5': 5, b'7': 7, b'9': 9}

letters_eng = {b'A': 'A', b'B': 'B', b'C': 'C', b'D': 'D', b'E': 'E', b'F': 'F',
               b'G': 'G', b'H': 'H', b'I': 'I', b'J': 'J', b'K': 'K', b'L': 'L',
               b'M': 'M', b'N': 'N', b'O': 'O', b'P': 'P', b'Q': 'Q', b'R': 'R',
               b'S': 'S', b'T': 'T', b'U': 'U', b'V': 'V', b'W': 'W', b'X': 'X',
               b'Y': 'Y', b'Z': 'Z', 
               b'a': 'a', b'b': 'b', b'c': 'c', b'd': 'd', b'e': 'e', b'f': 'f',
               b'g': 'g', b'h': 'h', b'i': 'i', b'j': 'j', b'k': 'k', b'l': 'l',
               b'm': 'm', b'n': 'n', b'o': 'o', b'p': 'p', b'q': 'q', b'r': 'r',
               b's': 's', b't': 't', b'u': 'u', b'v': 'v', b'w': 'w', b'x': 'x',
               b'y': 'y', b'z': 'z'}

signs = {b',': ',', b'.': '.', b';': ';', b':': ':', b"'": "'", b'"': '"', b'`': '`',
         b'-': '-', b'=': '=', b'_': '_', b'(': '(', b')': ')', b'<': '<', b'>': '>',
         b'+': '+', b'[': '[', b']': ']', b'{': '{', b'}': '}', b'/': '/', b'|': '|',
         b'*': '*', b'?': '?', b'@': '@', b'#': '#', b'$': '$', b'%': '%', b'^': '^', 
         b'&': '&', b'~': '~', b' ': 'Space', b'\\': '\\'}

action_keys = {"b'\\xe0'b'H'": 'Up'   , "b'\\xe0'b'P'": 'Down', 
               "b'\\xe0'b'M'": 'Right', "b'\\xe0'b'K'": 'Left',
               b'\t': 'Tab'  ,   b'\r': 'Enter', b'\x1b': 'Esc',
               b'\x08': 'Backspace'   , "b'\\xe0'b'S'": 'Delete', }

Fkeys = {"b'\\x00'b';'": 'F1', "b'\\x00'b'<'": 'F2', "b'\\x00'b'='": 'F3', 
         "b'\\x00'b'>'": 'F4', "b'\\x00'b'?'": 'F5', "b'\\x00'b'@'": 'F6', 
         "b'\\x00'b'A'": 'F7', "b'\\x00'b'B'": 'F8', "b'\\x00'b'C'": 'F9', 
         "b'\\x00'b'D'": 'F10', "b'\\xe0'b'\\x85'": 'F11', "b'\\xe0'b'\\x86'":'F12'}

key_combos = {"b'\\x00'b'\\x94'": 'Ctrl+Tab', 
              b'\x13':  'Ctrl+S', b'\x0c': 'Ctrl+L', 
              "b'\\x00'b'k'": 'Alt+F4'}

letters_rus = {b'\x80': 'А', b'\x81': 'Б', b'\x82': 'В', b'\x83': 'Г', b'\x84': 'Д',
               b'\x85': 'Е', b'\xf0': 'Ё', b'\x86': 'Ж', b'\x87': 'З', b'\x88': 'И',
               b'\x89': 'Й', b'\x8a': 'К', b'\x8b': 'Л', b'\x8c': 'М', b'\x8d': 'Н',
               b'\x8e': 'О', b'\x8f': 'П', b'\x90': 'Р', b'\x91': 'С', b'\x92': 'Т',
               b'\x93': 'У', b'\x94': 'Ф', b'\x95': 'Х', b'\x96': 'Ц', b'\x97': 'Ч',
               b'\x98': 'Ш', b'\x99': 'Щ', b'\x9a': 'Ь', b'\x9b': 'Ы', b'\x9c': 'Ъ',
               b'\x9d': 'Э', b'\x9e': 'Ю', b'\x9f': 'Я',
               b'\xa0': 'а', b'\xa1': 'б', b'\xa2': 'в', b'\xa3': 'г', b'\xa4': 'д',
               b'\xa5': 'е', b'\xf1': 'ё', b'\xa6': 'ж', b'\xa7': 'з', b'\xa8': 'и',
               b'\xa9': 'й', b'\xaa': 'к', b'\xab': 'л', b'\xac': 'м', b'\xad': 'н',
               b'\xe0': 'о', b'\xaf': 'п', b'\xe0': 'р', b'\xe1': 'с', b'\xe2': 'т',
               b'\xe3': 'у', b'\xe4': 'ф', b'\xe5': 'х', b'\xe6': 'ц', b'\xe7': 'ч',
               b'\xe8': 'ш', b'\xe9': 'щ', b'\xec': 'ь', b'\xeb': 'ы', b'\xea': 'ъ',
               b'\xed': 'э', b'\xee': 'ю', b'\xef': 'я'}

# Сводный словарь кодов и названий клавиш и комбинаций из всех вышеперечисленных
meaning = {**letters_eng, **signs, **action_keys, **Fkeys, **key_combos, **letters_rus}


# Функция ожидает нажатия клавиши, игнорируя все, кроме переданных в качестве параметра
# Возвращает название нажатой и принятой клавиши или комбинации
# При нажатии чего-то кроме ожидаемых просит быть внимательнее,
# если с перечнем приемлемых клавиш последним не был передан параметр 'silent'
def catch_key(*acceptable_keys):
    acceptable_keys = [*acceptable_keys]
    if len(acceptable_keys) == 1 and type(acceptable_keys[0]) is list:
        acceptable_keys = acceptable_keys[0]
    
    firstTry = True
    choice = prechoice = None
                
    while choice not in acceptable_keys:
                    
        if choice != None:
            if choice in keycode_prefixes:
                prechoice = choice
            elif prechoice:
                temp = str(prechoice)+str(choice)
                if str(prechoice)+str(choice) in meaning and meaning[str(prechoice)+str(choice)] in acceptable_keys:
                    return meaning[str(prechoice)+str(choice)]
                elif str(prechoice)+str(choice) in meaning and meaning[str(prechoice)+str(choice)] == 'Alt+F4': quit()
                else:
                    prechoice = None
                    firstTry = False
            elif choice in meaning and meaning[choice] in acceptable_keys:
                return meaning[choice]
            elif firstTry:
                firstTry = False
                    
        choice = getch()


####   участок для тестирования   ####################################################

if __name__ == '__main__':
    pass

    #while True:
    #    print(catch_key(list(meaning.values())))

    def backslasher(string):
        if string.count('\\'):
            return string[:string.find('\\')]+'\\'+string[string.find('\\'):]
        else: return string
    while True:

        code_dic = {}
        double = False
        while True:
            if not double:
                print('', end="\n Нажми следующую кнопку или комбинацию:  ")
            key = getch()
            if key in [b'\x00', b'\xe0'] and not double:
                double = True
                c = str(key)
                prechoice = backslasher(str(key))
                continue
            elif double:
                double = False
                c += str(key)
                code = prechoice+backslasher(str(key))
                print('"'+code+'"')
            elif key == b'`':
                print('...\n Как скажешь, хватит так хватит. Итого в словаре у нас:\n',code_dic, '\n')
                print('\n'+'_'*80)
                break
            else:
                c = str(key)
                code = backslasher(str(key))
                print(code)

            if c not in code_dic:

                key_name = input(" Как бы ты записал эту комбинацию?  ")


                double = was_double = False
                for i in [1,2]:
                    if not double:
                        print('', end="\n Повтори кнопку или комбинацию - перепроверим:  ")
                    key = getch()
                    if key in [b'\x00', b'\xe0'] and not double:
                        double = True
                        prechoice = backslasher(str(key))
                        continue
                    elif double:
                        was_double = True
                        double = False
                        code2 = prechoice+backslasher(str(key))
                        print('"'+code2+'"')
                    else:
                        was_double = False
                        code2 = backslasher(str(key))
                        print(code2)
                    if code2 == code:
                        if was_double:
                            print('', end="\n Да, повторил так же. Значит, "
                            "так и запишем:  "+'"'+code2+'"'+'  =  '+ key_name)
                        else:
                            print('', end="\n Да, повторил так же. Значит, "
                            "так и запишем:  "+code2+'  =  '+ key_name)
                        code_dic[c] = key_name
                        print('\n'+'_'*80)
                        break
                    else:
                        if was_double:
                            print('', end="Ты что-то путаешь, первый раз ты "
                                  "нажимал:  "+'"'+code+'"')
                        else:
                            print('', end="Ты что-то путаешь, первый раз ты "
                                  "нажимал:  "+code)
                        print('\n'+'_'*80)
                        break

        else:
            print(" Такое ты уже нажимал и называл:  %s  =  %s" % (code, code_dic[code]))
            print('\n'+'_'*80)