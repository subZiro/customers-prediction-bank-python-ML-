#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

# загрузка данных из файла
def f_read_csv(filename_str):
	# загрузка данных, с кодировкой, через разделитель строк ';', десятичные числа разделяются через ','
	# первая колонка = уникальный номер анализируемого пользвт
    return pd.read_csv('../datasets/{}.csv'.format(filename_str), 
                 encoding = 'cp1251', 
                 sep = ';', 
                 decimal = ',',
                 #na_filter = False,
                 index_col = 'AGREEMENT_RK')

# очиска сырых данных
def f_data_clear_v2(df = 'df'):
    
    # заполнение пустых значений на 0 в колонке смена карты 
    df['PREVIOUS_CARD_NUM_UTILIZED'] = df['PREVIOUS_CARD_NUM_UTILIZED'].replace(np.nan, 0)
    #df['PREVIOUS_CARD_NUM_UTILIZED'] =  df['PREVIOUS_CARD_NUM_UTILIZED'].apply((lambda x : x if x > 1 else 0))
    
    # создание таблицы есть менял ли карту
    df['PREVIOUS_CARD_NUM_UTILIZED_MY'] = df['PREVIOUS_CARD_NUM_UTILIZED'].apply((lambda x : x if x == 0 else 1))
    df['PREVIOUS_CARD_NUM_UTILIZED_MY'] = df['PREVIOUS_CARD_NUM_UTILIZED_MY'].astype(object)

    
    
    # объединение степени и оконченное высшее в высшее образование
    edu_list_new = ['Два и более высших образования', 'Ученая степень', 'Высшее']
    df.EDUCATION = df.EDUCATION.replace(edu_list_new, 'Высшее или несколько высших')


    # группировка 5 и более детей в 5 
    #df.CHILD_TOTAL = df.CHILD_TOTAL.replace(range(5,15), 5)
    #df.CHILD_TOTAL.value_counts()

    # группировка 5 и более иждивенцев в 5
    #df.DEPENDANTS = df.DEPENDANTS.replace(range(5,14), 5)
    #df.DEPENDANTS.value_counts()

    #Создание категории есть дети или нет детей
    df['CHILD_TOTAL_G_MY'] = df['CHILD_TOTAL']
    df['CHILD_TOTAL_G_MY'] =  df['CHILD_TOTAL_G_MY'].apply((lambda x : x if x == 0 else 1)).astype(object)
    #astype='object'
    
    df['CHILD_TOTAL_MY'] = df['CHILD_TOTAL'].apply((lambda x : x if x < 3 else 4)).astype(int)
    
    
    # меняем тип на логический ( 1 | 0 ),  столбца причастность к иностранной валюте
    rplse_dict = {'Без участия': '1', 'С участием' : '0'}
    df['ORG_TP_FCAPITAL'] = df['ORG_TP_FCAPITAL'].map(rplse_dict).astype(object)

    
    # создание колонки состоит в браке или нет 
    a_list = ['Состою в браке', 'Гражданский брак']
    b_list = ['Не состоял в браке', 'Разведен(а)', 'Вдовец/Вдова']
    df['MARITAL_STATUS_G_MY'] = df['MARITAL_STATUS']
    df.MARITAL_STATUS_G_MY = df.MARITAL_STATUS_G_MY.replace(a_list, '1')
    df.MARITAL_STATUS_G_MY = df.MARITAL_STATUS_G_MY.replace(b_list, '0')
    df.MARITAL_STATUS_G_MY = df.MARITAL_STATUS_G_MY.astype(object)

    # создание столбца , есть ли машина
    #df['AUTO_G_MY'] = df['OWN_AUTO']
    df['AUTO_G_MY'] = df['OWN_AUTO'].apply((lambda x : x if x == 0 else 1)).astype(object)

    df['GEN_TITLE_MY'] = df['GEN_TITLE']
    df['GEN_TITLE_MY'] = df['GEN_TITLE_MY'].replace('Военнослужащий по контракту', 'Служащий')
    df['GEN_TITLE_MY'] = df['GEN_TITLE_MY'].replace('Высококвалифиц. специалист', 'Специалист')
    df['GEN_TITLE_MY'] = df['GEN_TITLE_MY'].replace('Руководитель среднего звена', 'Руководитель')
    df['GEN_TITLE_MY'] = df['GEN_TITLE_MY'].replace('Руководитель низшего звена', 'Руководитель')
    df['GEN_TITLE_MY'] = df['GEN_TITLE_MY'].replace('Руководитель высшего звена', 'Руководитель')
    df['GEN_TITLE_MY'] = df['GEN_TITLE_MY'].replace('Партнер', 'Другое')
    gen_list = ['Служащий', 'Специалист', 'Руководитель', 'Рабочий' 'Индивидуальный предприниматель'
                   'Другое']
    df['GEN_TITLE_MY'] = df['GEN_TITLE_MY'].apply(
        (lambda x : x if x in gen_list else 'Другое')).astype(object)
    

    # создание столбца, количество не движемого имещества
    #presence_list = ['FL_PRESENCE_FL', 'HS_PRESENCE_FL', 'COT_PRESENCE_FL', 'GAR_PRESENCE_FL', 'LAND_PRESENCE_FL']

    df['PRESENCE_COUNT_MY'] = df['FL_PRESENCE_FL'] + df['HS_PRESENCE_FL'] + \
                            df['COT_PRESENCE_FL'] + df['GAR_PRESENCE_FL'] + \
                            df['LAND_PRESENCE_FL']

    # создание столбца, не движимое имущество, если есть то 1 если нет то 0 
    df['PRESENCE_MY'] =  df['PRESENCE_COUNT_MY'].apply((lambda x : x if x == 0 else 1))
    df['PRESENCE_MY'] = df['PRESENCE_MY'].astype(object)

    # создание столбца была ли просроска при ссуде
    df['LOAN_DLQ_MY'] = df['LOAN_DLQ_NUM']
    df['LOAN_DLQ_MY'] =  df['LOAN_DLQ_MY'].apply((lambda x : x if x > 1 else 0)).astype(object)

    # создание столбца есть ли активая ссуда
    df['LOAN_NUM_ACTIVE_MY'] = df['LOAN_NUM_TOTAL'] - df['LOAN_NUM_CLOSED']
    #df[df['LOAN_NUM_ACTIVE_MY'] > 3].LOAN_NUM_ACTIVE_MY = 3
    df['LOAN_NUM_ACTIVE_MY'] =  df['LOAN_NUM_ACTIVE_MY'].apply((lambda x : x if x > 1 else 0)).astype(object)

    # создание возрастных групп
    df['AGE_MY'] = df['AGE'].map(lambda age: int(age // 10))
    #df.AGE_MY.head()

    # создание категорий возрастов
    age_list_value = ['e','f', 'a','b','c','d']
    age_dict = dict(zip(range(1,7),age_list_value))
    df['AGE_G_MY'] = df['AGE_MY']
    df['AGE_G_MY'] =  df['AGE_G_MY'].map(age_dict)

    #df.AGE_G_MY.value_counts()
    
    # заполненме пустых значений столбца время работы на значения из столбца время жизни на посл месте
    df['WORK_TIME'] = df['WORK_TIME'].replace(np.nan, df.FACT_LIVING_TERM)
    
    
    region_list = ['ПОВОЛЖСКИЙ', 'ЮЖНЫЙ', 'ВОСТОЧНО-СИБИРСКИЙ',
                   'ЦЕНТРАЛЬНЫЙ 1', 'ЦЕНТРАЛЬНЫЙ 2', 'ДАЛЬНЕВОСТОЧНЫЙ',
                   'УРАЛЬСКИЙ', 'ЗАПАДНО-СИБИРСКИЙ', 'СЕВЕРО-ЗАПАДНЫЙ',
                   'ПРИВОЛЖСКИЙ', 'ЦЕНТРАЛЬНЫЙ ОФИС']
    
    family_money = ['от 10000 до 20000 руб.', 'от 20000 до 50000 руб.',
       'свыше 50000 руб.', 'от 5000 до 10000 руб.', 'до 5000 руб.']
    
    worker_list = ['Частная компания', 'Индивидуальный предприниматель',
       'Государственная комп./учреж.', 'Некоммерческая организация',
       'Частная ком. с инос. капиталом']
    
    
    
    df['FAMILY_MONEY_MY'] = df['PERSONAL_INCOME'].apply((lambda x : x*2 if x > 1 else 0))
    
    
    
    work_list = ['Рабочий', 'Специалист', 'Руководитель среднего звена',
       'Руководитель высшего звена', 'Служащий', 'Работник сферы услуг',
       'Высококвалифиц. специалист', 'Индивидуальный предприниматель',
        'Руководитель низшего звена', 'Другое', 'Партнер']
    
    work_dir = ['Вспомогательный техперсонал', 'Участие в основ. деятельности',
       'Адм-хоз. и трансп. службы', 'Пр-техн. обесп. и телеком.',
       'Служба безопасности', 'Бухгалтерия, финансы, планир.',
       'Снабжение и сбыт', 'Кадровая служба и секретариат',
       'Юридическая служба', 'Реклама и маркетинг']
    
    return df


# преобразование в инт в объекты 
def f_data_to_obj(datafile = 'df'):
	# преобразование в инт в объекты 

	# ручное 
	#df.SOCSTATUS_WORK_FL = df.SOCSTATUS_WORK_FL.astype(object)
	#df.TARGET = df.TARGET.astype(object)
	#df.SOCSTATUS_PENS_FL = df.SOCSTATUS_PENS_FL.astype(object)
	

    # изменение через заданый список столбцов
    to_obj_list = ['SOCSTATUS_WORK_FL', 'SOCSTATUS_PENS_FL', 'GENDER',
                   'REG_FACT_FL', 'FACT_POST_FL', 'REG_POST_FL', 'REG_FACT_POST_FL',
                   'REG_FACT_POST_TP_FL', 'FL_PRESENCE_FL', 'AUTO_RUS_FL', 
                   'HS_PRESENCE_FL', 'COT_PRESENCE_FL', 'GAR_PRESENCE_FL', 
                   'LAND_PRESENCE_FL', 'DL_DOCUMENT_FL', 'GPF_DOCUMENT_FL', 
                   'FACT_PHONE_FL', 'REG_PHONE_FL', 'GEN_PHONE_FL',
                   'PREVIOUS_CARD_NUM_UTILIZED_MY', 'CHILD_TOTAL_G_MY', 'ORG_TP_FCAPITAL', 
                   'MARITAL_STATUS_G_MY', 'AUTO_G_MY', 'GEN_TITLE_MY',
                   'PRESENCE_MY', 'LOAN_DLQ_MY', 'LOAN_NUM_ACTIVE_MY']
    
    for elem in to_obj_list:
        datafile[elem] = datafile[elem].astype(object)
    
    return datafile



# заполнение пустых значений на лучшее в категориальных данных
def f_data_obj_notnan(datafile, categorical_columns):
    # заполнение пустых значений на лучшее в категориальных данных
    
    datafile_describe = datafile.describe(include=[object])
    
    for colm in categorical_columns:
        datafile[colm] = datafile[colm].fillna(datafile_describe[colm]['top'])
        #datafile[colm] = datafile[colm].replace(np.nan, datafile_describe[colm]['top'])
        #print(colm, 'ok')
        
    return datafile



def f_data_bin_colom_notnan(datafile = 'df'):
    datafile_describe = datafile.describe(include=[object])

    for colm in binary_columns:
        top = datafile_describe[colm]['top']
        top_items = datafile[colm] == top
        datafile.loc[top_items, colm] = 0
        datafile.loc[np.logical_not(top_items), colm] = 1
        #print(colm, 'ok')

       
    #print(df[binary_columns])
    return datafile


# заполнение пустых количественных признаков на медиану столбца
def f_data_npnan_num_col_to_median(datafile, numerical_columns):
	# заполнение пустых количественных признаков на медиану столбца
    for col in numerical_columns:
        #datafile = datafile[col].fillna(datafile[col].median(axis=0), axis=0)
        #df[col] = df[col].fillna(df[col].median(axis=0), axis=0)
        datafile[col] = datafile[col].replace(np.nan, datafile[col].median(axis=0))
        
    return datafile


#вывод всех значений категориальных признаков по каждому столбцу
def f_print_categorical_columns(datafile = 'df'):
	#вывод всех значений категориальных признаков по каждому столбцу
    for colm in categorical_columns:
        print (datafile[colm].unique())
        print() 


# функция находит пустые сроки и столбцы и выводит их
def f_data_is_npnan_colrow(datafile = 'df'):
	# функция находит пустые сроки и столбцы и выводит их
    col_mask = datafile.isnull().any(axis=0) 
    row_mask = datafile.isnull().any(axis=1)
    print(datafile.loc[row_mask,col_mask])
    


# получаем список столбцов с катерогриальными признаками
def f_data_type_cat_num(datafile = 'df'):

    # получаем список столбцов с катерогриальными признаками
    categorical_col = [colm for colm in datafile.columns if datafile[colm].dtype.name == 'object']
    #print (categorical_col)

    # получаем список столбцов с количественными признаками
    #список количественных признаков (1 34 54 8)
    '''numerical_col = ['AGE', 'CHILD_TOTAL', 'DEPENDANTS', 'PERSONAL_INCOME',
                         'OWN_AUTO', 'CREDIT', 'TERM', 'FST_PAYMENT',
                         'FACT_LIVING_TERM', 'WORK_TIME', 'LOAN_NUM_TOTAL',
                         'LOAN_NUM_CLOSED', 'LOAN_NUM_PAYM', 'LOAN_DLQ_NUM', 
                         'LOAN_MAX_DLQ', 'LOAN_AVG_DLQ_AMT', 'LOAN_MAX_DLQ_AMT']
    '''
    numerical_col = [colm for colm in datafile.columns if datafile[colm].dtype.name != 'object']
    #print(numerical_columns) 

    return categorical_col, numerical_col
        

def f_data_type_bi_nonbi(datafile = 'df', categorical_col = 'categorical_columns'):
    datafile_describe = datafile.describe(include=[object])
    
    # список бинарных признаков (да нет)
    binary_col = [colm for colm in categorical_col if datafile_describe[colm]['unique'] == 2]
    #print (binary_columns)

    # список не бинарных признаков (красный зеленый синий)
    nonbinary_col = [colm for colm in categorical_col if datafile_describe[colm]['unique'] > 2]
    #print(nonbinary_columns)
    
    return binary_col, nonbinary_col


#подготовка данных
def f_cleaning(fname):
	#подготовка данных к обучению и применению модели

	print(f'Cleaning {fname}.csv ...')
	# чтение тренировочного файла
	#filename_train = 'Credit'
	df = f_read_csv(fname)

	# очистка дф
	df = f_data_clear_v2(df)

	# преобразование int таблиц в obj
	df = f_data_to_obj(df)

	# отделение столбца таргет в отдельную переменую
	df['TARGET'] = df['TARGET'].astype(object)
	target_columns = df['TARGET']
	df = df[list(set(df.columns).difference(['TARGET']))]
	#df = df.difference(['TARGET'])
	#df.drop(df.TARGET, inplace=True)

	categorical_columns, numerical_columns = f_data_type_cat_num(df)
	binary_columns, nonbinary_columns = f_data_type_bi_nonbi(df, categorical_columns)

	# заполнение пустых значений на лучшее в категориальных данных
	df = f_data_obj_notnan(df, categorical_columns)

	# получаем информацию о котерогиальных признаках
	#df[categorical_columns].describe()

	# заполнение пустых бинарных признаков лучшими из столбца
	#df = f_data_bin_colom_notnan(df)

	# заполнение пустых количественных признаков медианами
	df = f_data_npnan_num_col_to_median(df, numerical_columns)

	#Нормализация количественных признаков
	df_numerical = df[numerical_columns]
	#df_numerical = df_numerical.drop('TARGET', 1)
	df_numerical = (df_numerical - df_numerical.mean()) / df_numerical.std()
	#df_numerical.describe()

	# вывод пустых колонок 
	f_data_is_npnan_colrow(df)

	#разбиение небинарных признаков на новые столбцы с заполнеными 1,0
	df_nonbinary = pd.get_dummies(df[nonbinary_columns])
	#print (df_nonbinary.columns)

	#собираем датафрейм из новых таблиц
	df = pd.concat((target_columns, df_numerical, df[binary_columns], df_nonbinary), axis=1)
	#df = pd.concat((df[binary_columns], df_nonbinary), axis=1)

	return df












if __name__ != '__main__':
	#'Credit' -данные для обучения модели 
	#'Credit_new - данные для применения модели (отсутствует столбец с метками)
	#'Credit_new (TARGET)' - данные для применения модели 
	df = f_cleaning('Credit')
	df_test = f_cleaning('Credit_new (TARGET)')

else:
	print('please run \'model-2\'')










