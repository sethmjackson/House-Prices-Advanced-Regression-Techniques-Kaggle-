import pandas as pd
import datetime as dt
from typing import List, Dict, Callable
import matplotlib.pyplot as plt
import time
import types
import pickle


def getRows(df: pd.DataFrame) -> int:
    return len(df.index)


def getColumns(df: pd.DataFrame) -> int:
    return len(df.columns)


def printList(list: List, start=''):
    print(start)
    for i in list:
        print(i)
    print('')


def printDict(dict: Dict, start=''):
    print(start)
    print(type(dict))
    for k, v in dict.items():
        print(k)
        print(v,'\n')

def printNulls(df: pd.DataFrame):
    print('Null Columns:')
    null_columns = df.columns[df.isnull().any()]
    for c in null_columns:
        nullRows = df[c].isnull().sum()
        totalRows = getRows(df[c])
        print(c, ' ', nullRows, '/', totalRows, ' = ', int(nullRows / totalRows * 100), '%')
        print(df[c].value_counts(), '\n')
    print('# of Null columns: ', len(null_columns))

def getNulls(df: pd.DataFrame):
    null_columns = df.columns[df.isnull().any()]
    result = df[null_columns]
    return result[result.isnull().any(axis=1)]

def pickleObject(object, fileName):
    fileWrite = open(fileName, 'wb')
    models = pickle.dump(object, fileWrite)
    fileWrite.close()

def unpickleObject(fileName: str):
    fileRead = open(fileName, 'rb')
    object = pickle.load(fileRead)
    fileRead.close()
    return object



def dictDiff(dict1: Dict[str,int], dict2: Dict[str,int]):
    result = {}
    for i in dict1.keys():
        result[i] = dict1[i] - dict2[i]
    return result


def dfTypes(df: pd.DataFrame):
    typesDict = {}
    for c in df.columns:
        typesDict[c] = df[c].apply(type).value_counts()
    return typesDict

def seriesTypes(s: pd.Series):
    return s.apply(type).value_counts()


def dateFormat(df: pd.DataFrame, dateFormat='%m/%d/%Y'):
    dateColumns = []

    for k, v in dfTypes(df).items():
        if dt.datetime in v or pd.Timestamp in v or dt.time in v:
            dateColumns.append(k)

    for column in dateColumns:
        types = seriesTypes(df[column])
        df[column] = df[column].apply(lambda date: pd.to_datetime(date.strftime(dateFormat), infer_datetime_format=True).date() if isinstance(date, dt.datetime) and date is not pd.NaT else None)

        # print(types)

    for column in df.columns:
        if isinstance(column, dt.datetime):
            df.rename(columns={column: column.date().strftime(dateFormat)}, inplace=True)
            # print(df.columns)


def removeEmptyAll(list: List[pd.DataFrame]):
    for df in list:
        removeEmpty(df)

def removeEmpty(df: pd.DataFrame, printEmpty=False):
    rowCountBefore = getRows(df)
    columnCountBefore = getColumns(df)

    df.dropna(axis=0, how='all', inplace=True)
    df.dropna(axis=1, how='all', inplace=True)

    rowsRemoved = rowCountBefore - getRows(df)
    columnsRemoved = columnCountBefore - getColumns(df)

    if(printEmpty):
        print(rowsRemoved, ' of ', rowCountBefore, ' rows removed.')
        print(columnsRemoved, ' of ', columnCountBefore, ' columns removed.\n')


def validateNum(s: pd.Series, type='positive', text='', fun=lambda x: x):
    if type is 'positive':
        fun = lambda x : x > 0

    elif type is 'negative':
        fun = lambda x: x < 0

    validInts = len(s[fun(s)])
    totalInts = len(s)
    print(text, str(totalInts - validInts),' of ', str(totalInts), ' numbers are invalid.')

    return s[s[fun(s) == False]]

def printSum(s: pd.Series, text='', sig=2):
    seriesSum = s.sum()
    sigString = '%.'+str(sig)+'f'
    print(text,  sigString %(seriesSum))

def printMean(s: pd.Series, text='', sig=2):
    seriesSum = s.mean()
    sigString = '%.'+str(sig)+'f'
    print(text,  sigString %(seriesSum))





def validateType(s: pd.Series, t, text=''):
    validTypeCount = s.apply(type).value_counts().to_dict()[t]
    totalTypes = len(s)
    print(text, str(totalTypes - validTypeCount), ' of ', str(totalTypes), ' types are invalid.')

def colorByPositivity(df, column, output: Callable):
    posDF = df[df[column] >= 0]
    negDF = df[df[column] >= 0]

def roundFloats(df: pd.DataFrame):
    return df.applymap(lambda x: roundTraditional(x, 2) if isinstance(x, float) else x)

def roundTraditional(number, ndigits):
    return round(number + 10 ** (-len(str(number)) - 1), ndigits)

def setFloatPrecision(df: pd.DataFrame):
    df = df.applymap("${0:.2f}".format)

def multiplyPercentBy100 (df: pd.DataFrame):
    columns = []
    for c in df.columns:
        if '%' in c:
            columns.append(c)

    for c in columns:
        df[c] = df[c].apply(lambda x: x*100)

    return df

def convertColumns(df: pd.DataFrame, oldType, newType):
    columnsToConvert = df.select_dtypes(include=[oldType])

    for col in columnsToConvert.columns.values:
        df[col] = df[col].astype(newType)




def plotSetup(params: Dict):
    for f, p in params.items():
        if isinstance(p, types.LambdaType):
            getattr(plt, f)(p())
        elif isinstance(f, types.LambdaType):
            f()
        else:
            getattr(plt, f)(p)

def selectExcept(df, colnames: List[str]):
    return df[df.columns.difference(colnames, sort=False)]

def getLinSpace(listP: List):
    start = listP[0]
    stop = listP[-1]
    num = len(listP)
    return (start, stop, num)

def getRange(listP: List):
    start = int(listP[0])
    end = int(listP[-1])
    step = int(listP[1] - listP[0])
    return start, end, step

def multiplyRange(listP: List, mult: float):
    start, end, step = getRange(listP)
    listTest = list(range(start, end+step, step))
    newstep = int(step * mult)
    result = list(range(start, end+newstep, newstep))

    return result

def multiplyFigSize(x=1.0, y=1.0):
        fig = plt.gcf()
        figSize = fig.get_size_inches()
        fig.set_size_inches((figSize[0]*x, figSize[1]*y))


def getExecutionTime(fun: Callable):
    start_time = time.time()
    returnValue = fun()

    timeUsed = time.time() - start_time
    seconds = timeUsed % 60
    minutes = int(timeUsed // 60)

    if seconds < 1:
        seconds = round(seconds , 2)
    else:
        seconds = int(seconds)


    timeString = 'Minutes: '+ str(minutes)+ '  Seconds: '+ str(seconds)
    print(timeString,'\n')
    return timeString, returnValue

def appendColumns(columnList):
    return pd.concat(columnList, axis=1)

def getColumnDiff(df1: pd.DataFrame, df2: pd.DataFrame):
    return [value for value in df1.columns if value not in df2.columns]