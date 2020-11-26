import os
from os import path
import scipy.stats as stats
import numpy as np

def elementsCount(matrix):
    n = 0
    for arr in matrix:
        n += len(arr)
    return n

def concat(matrix):
    result = []
    for arr in matrix:
        for i in arr:
            result.append(i)
            
    return result

def mean(arr):
    return sum(arr) / len(arr)

# межгрупповая вариация
def SSA(matrix):
    gen_mean = mean(concat(matrix))
    
    result = 0
    for arr in matrix:
        result += len(arr) * (mean(arr) - gen_mean) ** 2
    
    return result

# внутригрупповая вариация
def SSW(matrix):
    
    result = 0
    for arr in matrix:
        arr_mean = mean(arr)
        for i in arr:
            result += (i - arr_mean) ** 2
            
    return result

# межгрупповая дисперсия
def MSA(matrix):
    return SSA(matrix) / getDFN(matrix)

# внутригрупповая дисперсия
def MSW(matrix):
    return SSW(matrix) / getDFD(matrix)

def getFishersCritery(matrix):
    return MSA(matrix)/MSW(matrix)

def getDFN(matrix):
    return len(matrix) - 1

def getDFD(matrix):
    return elementsCount(matrix) - len(matrix)

def getCriticalFishersCritery(pvalue, matrix):
    dfn = getDFN(matrix)
    dfd = getDFD(matrix)
    return stats.f.isf(pvalue, dfn, dfd)

def inputFile():
    while True:   
        filename = input('Введите путь к файлу: ')

        dir_path = os.getcwd()  
        filename = path.join(dir_path, filename)
                
        if os.path.isfile(filename):
            f = open(filename, 'r')

            fileString = ''
            for s in f:        
                fileString += s.strip() 
            fileString = fileString.replace(',', '.').replace('\t', ' ').replace('\n', ' ')
            
            f.close()
            
            return fileString
        else:
            print(f'Ошибка: файла {filename} не существует.')

def inputCountSplit(count):
    while True:
        num = input('Введите количество серий, на которое стоит разделить выборку: ')
        if num.isdigit():
            num = int(num)
            if num > 1 and num < count:
                return num
            else:
                print(f'Ошибка: Число должно быть в больше 1 и меньше {count - 1}.')
        else:    
            print('Ошибка: Не удалось преобразовать ввод в число.')
    
def inputSignificanceLevel():
    while True:
        num = input('Введите уровень значимости: ').replace(',', '.')

        if num.replace('.', '',1).isdigit():
            num = float(num)
            if num > 0 and num < 1:
                return num
            else:
                print('Ошибка: Число должно быть больше 0 и меньше 1.')
        else:
            print('Ошибка: Не удалось преобразовать ввод в число.')
    
def normalizeFloat(num):
    return "{:4.3e}".format(num)

def printFisher():
    fileString = inputFile()
    
    arr = list(map(float,fileString.split(' ')))

    print(f'Количество элементов выборки: {len(arr)}')
    print(f'Среднее арифметическое значение: {normalizeFloat(np.mean(arr))}')
    print(f'Оценка среднего квадратического отклонения: {normalizeFloat(stats.tstd(arr))}')

    countSplit = inputCountSplit(len(arr))
    significanceLevel = inputSignificanceLevel()
    
    arr = np.array_split(arr, countSplit)    

    print(f'Межгрупповая дисперсия: {normalizeFloat(MSA(arr))}')
    print(f'Внутригрупповая дисперсия: {normalizeFloat(MSW(arr))}')
    
    fCritery = getFishersCritery(arr)    
    print(f'Критерий Фишера: {normalizeFloat(fCritery)}')
    fCriticalCritery = getCriticalFishersCritery(significanceLevel, arr)
    print(f'Критический критерий Фишера: {normalizeFloat(fCriticalCritery)}')
    
    print(f'{normalizeFloat(fCritery)} {">=" if fCritery >= fCriticalCritery else "<"} {normalizeFloat(fCriticalCritery)}')    

    print(f'{"Систематическая погрешность присутствует." if fCritery >= fCriticalCritery else "Систематическая погрешность отсутствует."}') 

printFisher()