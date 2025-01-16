import os
import re
import random
import string

from pprint import pprint

# путь до проекта
path_project = "../../../C/Harvester_Copy/client/"
# директории, которые нужно игнорировать
dirs_ignore = [".git"]

# определяем список для поиска переменных и функций, данные значения будут использоваться в регулярных выражениях
data_types_c = ["char", "unsigned char", "signed char",
                "char*", "unsigned char*", "signed char*",
                "short", "short int", "signed short", "signed short int", "unsigned short", "unsigned short int",
                "short*", "short int*", "signed short*", "signed short int*", "unsigned short*", "unsigned short int*",
                "int", "signed int", "signed", "unsigned int", "unsigned",
                "int*", "signed int*", "signed*", "unsigned int*", "unsigned*",
                "long", "long int", "signed long int", "signed long", "unsigned long", "unsigned long int", "long long", "long long int", "signed long long int", "signed long long", "unsigned long long", "unsigned long long int",
                "long*", "long int*", "signed long int*", "signed long*", "unsigned long*", "unsigned long int*", "long long*", "long long int*", "signed long long int*", "signed long long*", "unsigned long long*", "unsigned long long int*",
                "float",
                "float*",
                "double", "long double",
                "double*", "long double*",
                "void", "void*",
                "size_t", "size_t*"
                ]

# если в переменную попадут данные значения, они будут игнорироваться
special_cases_searching_variables = ["main", "typedef", "ifdef", "elif", "defined", "ifndef", "define",
                                     'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                                     'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                                     "str"]

# если строка, которая попала под замену будет содержать одну из этих переменных, она будет игнорироваться
special_cases_substitution_variables = ["include", "ifdef", "defined", "define"]


class Obfuscator():

    # рекурсивное получение всех файлов по указанному пути
    def get_all_files_recursively(self, path):
        # создание пустого списка для хранения всех найденных файлов
        all_files = []
        
        # использование os.walk() для рекурсивного обхода директорий
        for root, dirs, files in os.walk(path):
            for file in files:
                # создание полного пути к файлу с использованием os.path.join()
                full_path = os.path.join(root, file)
                # игнорируем указанные директории
                if not any(ignore in full_path for ignore in dirs_ignore):
                    all_files.append(full_path)
        return all_files


    # удаление пуcтых строк и коментариев из файла
    def clearing_blank_lines_and_comments(self, path):
        try:
            with open(path, 'r') as file:
                content = file.readlines() 

            filtered_lines = [line for line in content if line.strip() and not line.strip().startswith("//")]  

            with open(path, 'w') as n_file:
                n_file.writelines(filtered_lines)
        # если попадается бинарный файл
        except UnicodeDecodeError:
            pass
    

    # поиск и сбор переменных из файлов
    def searching_variables(self, path):

        variables = []

        try:
            with open(path, 'r') as file:
                content = file.readlines() 

            for line in content:
                for d in data_types_c:
                    
                    re_patterns = [
                        # для переменных и функций типа
                        # int test;
                        # int test();
                        rf"\s{d}\s(\w*)",
                        # для переменных и функций типа
                        # int* test;
                        # int* test();
                        rf"\s{d}\*\s(\w*)",
                        # для функций типа
                        # int test()
                        rf"{d}\s(\w*)",
                        # для функций типа
                        # int* test()
                        rf"{d}\*\s(\w*)"
                    ]

                    for re_pattern in re_patterns:
                        vars = re.findall(re_pattern, line)
                        if vars:
                            for var in vars:
                                # игнорируем все переменные, которые совпали с переменными из special_cases_searching_variables
                                if all(case != var for case in special_cases_searching_variables):
                                    # если переменная не является типом данных
                                    if all(case != var for case in data_types_c):
                                        variables.append(var)
        # если попадается бинарный файл
        except UnicodeDecodeError:
            pass
        return variables


    def generating_random_string(self):
        # https://ru.stackoverflow.com/questions/1197413/%D0%93%D0%B5%D0%BD%D0%B5%D1%80%D0%B0%D1%86%D0%B8%D1%8F-%D1%80%D0%B0%D0%BD%D0%B4%D0%BE%D0%BC%D0%BD%D0%BE%D0%B9-%D1%81%D1%82%D1%80%D0%BE%D0%BA%D0%B8
        text = [random.choice(string.ascii_lowercase if i != 5 else string.ascii_uppercase) for i in range(random.randint(10, 20))]
        return (''.join(text))


    def name_generation(self, list, dict):

        for name in list:
            dict[name] = self.generating_random_string()
    

    # замена всех найденных переменных
    def substitution_variables(self, path, dict):
        try:
            with open(path, 'r') as file:
                content = file.readlines()
            
            with open(path, 'w') as file:
                for line in content:
                    for key, data in dict.items():
                        if key in line:
                            # print(f"key: {key}")
                            # print(f"line_old: {line.strip()}")
                            if all(case not in line for case in special_cases_substitution_variables):
                                line = line.replace(key, data)
                            # print(f"line_new: {line.strip()}\n")
                    file.write(line)
                    print(line, end="")
                        
        except UnicodeDecodeError:
            pass


def main():

    obfuscator = Obfuscator()

    # получение всех файлов в проекте
    all_files = obfuscator.get_all_files_recursively(path_project)

    # удаляем пустые строки и коментарии из файлов
    for file in all_files:
        obfuscator.clearing_blank_lines_and_comments(file)
    
    # получаем все существующие переменные в проекте
    variables = []
    for file in all_files:
        print(f"-----------------------------file--------------------------\n{file}")
        vars_file = obfuscator.searching_variables(file)
        if vars_file:
            variables += vars_file
    # # сортируем массив
    variables = sorted(variables)
    # удаляем повторения
    variables = list(dict.fromkeys(variables))
    # удаляем пустые элементы
    variables = list(filter(None, variables))
    print(variables)
    print()

    # получаем словарь {name: random_name} от переданного массива
    modified_names = {}
    obfuscator.name_generation(variables, modified_names)
    # Сортируем ключи по длине
    # так как если этого не сделать, то маленькие key могут частично заменить код переменной или функции
    modified_names = dict(sorted(modified_names.items(), key=lambda x: len(x[0]), reverse=True))
    # Создаем новый словарь из отсортированных элементов
    # modified_names = dict(modified_names)
    print(modified_names)

    for file in all_files:
        print(f"\n------------------{file}----------------------\n")
        obfuscator.substitution_variables(file, modified_names)
    

if __name__ == "__main__":
    main()