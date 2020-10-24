import pandas as pd
import numpy as np
import math as mt
import pandas_datareader as web
import matplotlib.pyplot as plt

# Подробная статья по реализации индикатора
# Информация на сайте в плане кода не много устарела, но смысл тот же
# http://www.andrewshamlet.net/2017/02/16/python-tutorial-price-channels/

# Реализация индикатора ценового канала (Price Channels)
def Indicator_Price_Channels(Stock,Start,End):

    # Возвращает ряды данных с сайта YAHOO на временном отрезке
    def get_high(stock, start, end):    return web.get_data_yahoo(stock, start, end)['High']
    def get_low(stock, start, end):     return web.get_data_yahoo(stock, start, end)['Low']
    def get_close(stock, start, end):   return web.get_data_yahoo(stock, start, end)['Adj Close']

    # Получаем данные с YAHOO 
    Data            = pd.DataFrame(get_high(Stock,Start,End))
    Data['Low']     = pd.DataFrame(get_low(Stock,Start,End))
    Data['Close']   = pd.DataFrame(get_close(Stock,Start,End))

    # Данные индикатора
    Data['4WH']     = Data['High'].rolling(20).mean()
    Data['4WL']     = Data['Low'].rolling(20).mean()
    Data['50 sma']  = Data['Close'].rolling(50).mean()

    # Возвращаем данные индикатора
    return Data

# Модификатор
def Operator(Data,PW = False):

    # Проверка от левых данных
    Ys = []
    for i in Data: 
        if(mt.isnan(i) != True):
            Ys.append(float(i))

    # Масштабируем сигнал от 0 до Pi
    Xpi = np.linspace(0,np.pi,len(Ys))

    # Метод для конвертации массива данных в функцию от 0 до pi
    def F(x, E=0.1): 
        Nm, Xps = 0, x
        while(Xps > np.pi): Xps -= 2 * np.pi
        for k in Xpi: 
            if(abs(k-Xps) < E): return Ys[Nm] 
            Nm += 1
        return 0
        
    # Синк функция
    def S(k, x, n = 100): return ( ((-1)**k) * np.sin(n*x) ) / ( n * x - k * np.pi )

    # Функция Уиткера (4.1)
    # Принимает функцию, которую иследуют, его значение по X и постоянную n
    def Ln(f, x, n = 100):
        LN = 0
        for k in range(1, n): LN += (( ((-1)**k) * np.sin(n*x)) / (n * x - k * np.pi)) * f((k * np.pi) / n)
        return LN

    # Функция модификатор (5.42)
    def ATh(F,x):
        AT = 0 
        for k in range(1,len(Xpi)-1): AT +=  S(k,x) * (F(Xpi[k+1]) + ( 2 * F(Xpi[k]) ) + F(Xpi[k-1]))
        return  0.25 * AT 

    # Возращаем данные
    if(PW): return {"X" : Xpi, "Y" : [Ln(F,x) for x in Xpi]}
    else:   return {"X" : Xpi, "Y" : [ATh(F,x) for x in Xpi]}

def Start():

    # Получаем данные индикатора
    Data = Indicator_Price_Channels('FB', '1/1/2016', '12/31/2016')

    # Рисуем данные индикатора
    plt.subplot(3,1,1)
    plt.title("Price Channels")
    plt.plot(Data['4WH'],label="4WH")
    plt.plot(Data['4WL'],label="4WL")
    plt.plot(Data['50 sma'],label="50 sma")
    plt.plot(Data['Close'],label="Close")
    plt.legend()

    # Рисуем данные с модификаторм по формуле 4.1
    plt.subplot(3,1,2)
    plt.title("Модификация по формуле 4.1")

    DATA = Operator(Data['4WH'],True)
    plt.plot(DATA["X"],DATA["Y"],label="4WH")

    DATA = Operator(Data['4WL'],True)
    plt.plot(DATA["X"],DATA["Y"],label="4WL")

    DATA = Operator(Data['50 sma'],True)
    plt.plot(DATA["X"],DATA["Y"],label="50 sma")

    DATA = Operator(Data['Close'],True)
    plt.plot(DATA["X"],DATA["Y"],label="Close")

    plt.legend()

    # Рисуем данные с модификаторм по формуле 5.42
    plt.subplot(3,1,3)
    plt.title("Модификация по формуле 5.42")

    DATA = Operator(Data['4WH'])
    plt.plot(DATA["X"],DATA["Y"],label="4WH")
    
    DATA = Operator(Data['4WL'])
    plt.plot(DATA["X"],DATA["Y"],label="4WL")
    
    DATA = Operator(Data['50 sma'])
    plt.plot(DATA["X"],DATA["Y"],label="50 sma")
    
    DATA = Operator(Data['Close'])
    plt.plot(DATA["X"],DATA["Y"],label="Close")

    plt.legend()

    # Вывести график
    plt.show()

if __name__ == "__main__": Start()