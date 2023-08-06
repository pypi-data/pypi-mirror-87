import numpy as np
def jordanGauss(P_adv,ii,jj):
    """
    P_adv - numpy array или list, которую надо преобразовать
	
    ii - номер ключевой (ведущей) строки
	номер первой строки - 0
	jj - номер ключевого (ведущего) столбца
    номер первого столца - 0----------

    Returns
	Возвращает преобразованную таблицу
    -------

    P_new: a numpy array
    """
    P_new=np.zeros((len(P_adv), len(P_adv[0])))
    if abs(P_adv[ii][jj])<0.00001:
        print("!!!!!!!!!!!!!!!!!!")
        print("Ключевой элемент 0")
        print("Матрица не изменена")
        print("!!!!!!!!!!!!!!!!!!")
        return P_adv
    for i in range(len(P_adv)):
        for j in range(len(P_adv[0])):
            P_new[i][j]=(P_adv[i][j]*P_adv[ii][jj]-P_adv[i][jj]*P_adv[ii][j])/P_adv[ii][jj]
        for j in range(len(P_adv[0])):
            P_new[ii][j]=P_adv[ii][j]/P_adv[ii][jj]
    return P_new  

