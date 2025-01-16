# Подготовка перед запуском
Укажите расположение директории с вашим проектом:
```python
path_project = "path/you/project"
```
Отредактируейте переменные, которые вы хотите исключить из преобразования:
```python
special_cases_searching_variables = ["your", "vars"]
```

# Запуск
```bash
python3 obfuscator.py
```
После запуска будут постепенно отрабатывать каждые шаги обускации с подробным выводом в консоль. 
После 5 этапа все файлы проекта будут заменены на обфуцированные, поэтому производите все действия в копии проекта!

# Пример
Исходный код:
```c
#include <stdio.h>
#include <stdlib.h>


// добавление данных в массив
// массив, длина заполненного массива, длина массива, данные для записи 
void* append(short *data, size_t *length, size_t *capacity, short value)
{
    // если заполненость массива больше или равна размеру массива
    // то тогда увеличиваем его в 2 раза
    if(*length >= *capacity) {
        // уавеличиваем кол-во вмещаемых элементов в массив до 20
        (*capacity) *= 2;
        // создаем новый массив большего размера
        short *ar = malloc(sizeof(short) * *capacity);
        if(ar == NULL)
            return data;
        // копируем данные из прошлого массива в новый
        for(int i = 0; i < *length; ++i)
            ar[i] = data[i];
            
        free(data);
        data = ar;
    }
    
    // запись значения в массив
    data[*length] = value;
    (*length)++;
    return data;
}

int main(void)
{
    // максимальное числов элементов массива
    size_t capacity = 10;
    // число сохранненных в массив значений
    size_t length = 0;

    // получим непрерывную область памяти под массив
    short *data = malloc(sizeof(short) * capacity);

    // запись данных в массив
    for(int i = 0; i < 11; ++i) {
        data = append(data, &length, &capacity, rand() % 40 - 20);
    }
    
    printf("length = %u, capacity = %u\n", length, capacity);
    for(int i = 0; i < length; ++i) {
        printf("%d ", data[i]);
    }
    free(data);

    return 0;
}
```
Запуск программы:
```bash
python3 obfuscator.py
====================================================================================================
[*] STAGE 1: Getting all the project files
test/test.c
test/test
[+] STAGE 1: Is completed
Do you want to continue? (yes/no): yes
====================================================================================================
[*] STAGE 2: Removing comments and blank lines from files
[+] STAGE 2: Is completed
Do you want to continue? (yes/no): yes
====================================================================================================
[*] STAGE 3: Get all the existing variables and functions in the project
----------------------------------------------------------------------------------------------------
File: test/test.c
append
ar
capacity
data
length
value
----------------------------------------------------------------------------------------------------
File: All found variables and functions:
append
ar
capacity
data
length
value
[+] STAGE 3: Is completed
Do you want to continue? (yes/no): yes
====================================================================================================
[*] STAGE 4: Generating obfuscated names 
append   -> wdudsFlskdrupjppnlff
ar       -> mbfewTkyfmrvqegi
capacity -> rljndKqwjwwr
data     -> giuduAiarvrq
length   -> htznmLmrwjcbndiukzg
value    -> coswqSuxmgt
[+] STAGE 4: Is completed
Do you want to continue? (yes/no): yes
====================================================================================================
[*] STAGE 5: Name substitution 
replacement statrt: test/test.c
replacement end:    test/test.c
replacement statrt: test/test
replacement end:    test/test
[+] STAGE 5: Is completed
```

Итог:
```c
#include <stdio.h>
#include <stdlib.h>
void* wdudsFlskdrupjppnlff(short *giuduAimbfewTkyfmrvqegivrq, size_t *htznmLmrwjcbndiukzg, size_t *rljndKqwjwwr, short coswqSuxmgt)
{
    if(*htznmLmrwjcbndiukzg >= *rljndKqwjwwr) {
        (*rljndKqwjwwr) *= 2;
        short *mbfewTkyfmrvqegi = malloc(sizeof(short) * *rljndKqwjwwr);
        if(mbfewTkyfmrvqegi == NULL)
            return giuduAimbfewTkyfmrvqegivrq;
        for(int i = 0; i < *htznmLmrwjcbndiukzg; ++i)
            mbfewTkyfmrvqegi[i] = giuduAimbfewTkyfmrvqegivrq[i];
        free(giuduAimbfewTkyfmrvqegivrq);
        giuduAimbfewTkyfmrvqegivrq = mbfewTkyfmrvqegi;
    }
    giuduAimbfewTkyfmrvqegivrq[*htznmLmrwjcbndiukzg] = coswqSuxmgt;
    (*htznmLmrwjcbndiukzg)++;
    return giuduAimbfewTkyfmrvqegivrq;
}
int main(void)
{
    size_t rljndKqwjwwr = 10;
    size_t htznmLmrwjcbndiukzg = 0;
    short *giuduAimbfewTkyfmrvqegivrq = malloc(sizeof(short) * rljndKqwjwwr);
    for(int i = 0; i < 11; ++i) {
        giuduAimbfewTkyfmrvqegivrq = wdudsFlskdrupjppnlff(giuduAimbfewTkyfmrvqegivrq, &htznmLmrwjcbndiukzg, &rljndKqwjwwr, rand() % 40 - 20);
    }
    printf("htznmLmrwjcbndiukzg = %u, rljndKqwjwwr = %u\n", htznmLmrwjcbndiukzg, rljndKqwjwwr);
    for(int i = 0; i < htznmLmrwjcbndiukzg; ++i) {
        printf("%d ", giuduAimbfewTkyfmrvqegivrq[i]);
    }
    free(giuduAimbfewTkyfmrvqegivrq);
    return 0;
}   
```