import numpy as np
from .plain import jordanGauss
def index_row(data, row):
    """
    data массив ndarray numpy
    row массив array
    Функция ищет вхождение row в data
    и выдает номер индекса или -1, если не входит
    """
    for r in data.tolist():
        if r==row.tolist():
            return data.tolist().index(r)
    return -1
def transformationJG(P_adv,ii,jj):
    """
    Преобразование Жордана-Гаусса для метода искусственного базиса
    Входные параметры: P_adv - Подготовленная матрица (np.array или list)
    ii - номер ключевой строки
    jj - номер ключевого столбца
    Выходные параметры: Словарь с ключами 
    P_new - преобразованная матрица (np.array)
    x - опорный план ЗЛП 
    Fun - значение целевой функции в опорном плане
    """
    b=np.zeros((len(P_adv), len(P_adv[0])))
    b=jordanGauss(P_adv,ii,jj)
    
    P_transp=b.transpose()
    basis=np.insert(np.eye(len(b)-1), len(b)-1, 0, axis = 1)
    ind=[-1]*len(basis)
    indexs_of_x=[index_row(P_transp[1:,],basis[i]) for i in range(len(ind)) ]
    indexs_of_x=[int(val) for val in indexs_of_x]
    x=[0]*(len(P_transp)-1)
    for i in range(len(indexs_of_x)):
        x[indexs_of_x[i]]=P_transp[:1,:len(b)-1][0].tolist()[i]
    Fun=P_transp[0][len(P_transp[0])-1]
    dict = {'P_new': b, 'x': x, 'Fun':Fun}
    return dict

    


