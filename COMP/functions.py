# -*- coding: utf-8 -*-
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import pandas as pd 
import warnings
warnings.filterwarnings("ignore")
import re
import numpy as np
import pdfplumber

def helpme():
    print("В этом модуле представлены 5 функций: \npdf_text()\nload_model()\nmake_pred\ncleaning()\nusr_val()\n\nДля вызова документации функции введите print(function.__doc__) или воспользуйтесь файлом Documentation.docx")
    
def pdf_text(filename):
    """
    Функция получения текста из pdf файла
    
    PARAMS:
    filename(str) - Имя pdf файла с расширением в той же директории или полный путь до файла(пример resume.pdf)
    
    RETURN:
    words(str)
    """
    pdf = pdfplumber.open(filename)
    T = []
    for i in range(2):
        try:
            page = pdf.pages[i]
            T.append(page.extract_text())
        except Exception:
            continue
    pdf.close()
    return " ".join(T)
    
def load_model(filename):
    """
    Функция загрузки скомпилированной модели pkl(import pickle)
    
    PARAMS:
    filename(str) - Имя pkl файла с расширением в той же директории или полный путь до файла(пример model.pkl)
    
    RETURN:
    Loaded model
    """
    print(">>> Загрузка модели")
    with open(filename, 'rb') as file:
            model = pickle.load(file)
    print(">>> Готово")
    return model
    
def make_pred(model, words, p_num):
    """
    Функция предсказания
    
    PARAMS:
    model - Загруженная модель, используйте load_model() или свою модель 
    words(str) - Получает загруженные слова из pdf: pdf_text() или стоку с вашими словами
    p_num(int) - Количество предсказываемых экземпляров класса
    
    RETURN:
    list of predictions(str)
    """
    print(">>> Making prediction")
    if p_num==1:
        pred = model.predict([words])
        return pred
    else:
        print()
        print(">>> Внимание, тк вы хотите получить более одного результата, имейте в виду, что результат может не соответствовать вашим ожиданиям.")
        R = []
        allpreds = model.decision_function([words]).reshape(-1)
        for i in allpreds.argsort()[-2:][::-1]:
            R.append(model.classes_[i])
        return R
        
def cleaning(words):
    """
    Функция очистки ваших слов от ненужных, таких как союзы, местоимения, часто встречаемые и тп
    
    PARAMS:
    words(str) - Ваши слова
    
    RETURN:
    words(str)
    """
    print(">>> Всего слов: ", len(words.split()))
    a=len(words.split()) 
    words = re.sub('[–\n\r."("")"©•,«»:;%$!@#0-9$a-z]', '', words).lower()
    stopwords = ["тд","c","а","алло","без","белый","близко","более","больше","большой","будем","будет","будете","будешь","будто","буду","будут","будь","бы","бывает","бывь","был","была","были","было","быть","в","важная","важное","важные","важный","вам","вами","вас","ваш","ваша","ваше","ваши","вверх","вдали","вдруг","ведь","везде","вернуться","весь","вечер","взгляд","взять","вид","видел","видеть","вместе","вне","вниз","внизу","во","вода","война","вокруг","вон","вообще","вопрос","восемнадцатый","восемнадцать","восемь","восьмой","вот","впрочем","времени","время","все","все еще","всегда","всего","всем","всеми","всему","всех","всею","всю","всюду","вся","всё","второй","вы","выйти","г","где","главный","глаз","говорил","говорит","говорить","год","года","году","голова","голос","город","да","давать","давно","даже","далекий","далеко","дальше","даром","дать","два","двадцатый","двадцать","две","двенадцатый","двенадцать","дверь","двух","девятнадцатый","девятнадцать","девятый","девять","действительно","дел","делал","делать","делаю","дело","день","деньги","десятый","десять","для","до","довольно","долго","должен","должно","должный","дом","дорога","друг","другая","другие","других","друго","другое","другой","думать","душа","е","его","ее","ей","ему","если","есть","еще","ещё","ею","её","ж","ждать","же","жена","женщина","жизнь","жить","за","занят","занята","занято","заняты","затем","зато","зачем","здесь","земля","знать","значит","значить","и","иди","идти","из","или","им","имеет","имел","именно","иметь","ими","имя","иногда","их","к","каждая","каждое","каждые","каждый","кажется","казаться","как","какая","какой","кем","книга","когда","кого","ком","комната","кому","конец","конечно","которая","которого","которой","которые","который","которых","кроме","кругом","кто","куда","лежать","лет","ли","лицо","лишь","лучше","любить","люди","м","маленький","мало","мать","машина","между","меля","менее","меньше","меня","место","миллионов","мимо","минута","мир","мира","мне","много","многочисленная","многочисленное","многочисленные","многочисленный","мной","мною","мог","могу","могут","мож","может","может быть","можно","можхо","мои","мой","мор","москва","мочь","моя","моё","мы","на","наверху","над","надо","назад","наиболее","найти","наконец","нам","нами","народ","нас","начала","начать","наш","наша","наше","наши","не","него","недавно","недалеко","нее","ней","некоторый","нельзя","нем","немного","нему","непрерывно","нередко","несколько","нет","нею","неё","ни","нибудь","ниже","низко","никакой","никогда","никто","никуда","ним","ними","них","ничего","ничто","но","новый","нога","ночь","ну","нужно","нужный","нх","о","об","оба","обычно","один","одиннадцатый","одиннадцать","однажды","однако","одного","одной","оказаться","окно","около","он","она","они","оно","опять","особенно","остаться","от","ответить","отец","откуда","отовсюду","отсюда","очень","первый","перед","писать","плечо","по","под","подойди","подумать","пожалуйста","позже","пойти","пока","пол","получить","помнить","понимать","понять","пор","пора","после","последний","посмотреть","посреди","потом","потому","почему","почти","правда","прекрасно","при","про","просто","против","процентов","путь","пятнадцатый","пятнадцать","пятый","пять","работа","работать","раз","разве","рано","раньше","ребенок","решить","россия","рука","русский","ряд","рядом","с","с кем","сам","сама","сами","самим","самими","самих","само","самого","самой","самом","самому","саму","самый","свет","свое","своего","своей","свои","своих","свой","свою","сделать","сеаой","себе","себя","сегодня","седьмой","сейчас","семнадцатый","семнадцать","семь","сидеть","сила","сих","сказал","сказала","сказать","сколько","слишком","слово","случай","смотреть","сначала","снова","со","собой","собою","советский","совсем","спасибо","спросить","сразу","стал","старый","стать","стол","сторона","стоять","страна","суть","считать","т","та","так","такая","также","таки","такие","такое","такой","там","твои","твой","твоя","твоё","те","тебе","тебя","тем","теми","теперь","тех","то","тобой","тобою","товарищ","тогда","того","тоже","только","том","тому","тот","тою","третий","три","тринадцатый","тринадцать","ту","туда","тут","ты","тысяч","у","увидеть","уж","уже","улица","уметь","утро","хороший","хорошо","хотел бы","хотеть","хоть","хотя","хочешь","час","часто","часть","чаще","чего","человек","чем","чему","через","четвертый","четыре","четырнадцатый","четырнадцать","что","чтоб","чтобы","чуть","шестнадцатый","шестнадцать","шестой","шесть","эта","эти","этим","этими","этих","это","этого","этой","этом","этому","этот","эту","я","являюсь"]
    words = ' '.join([word for word in words.split() if word not in (stopwords)])
    print(">>> Убрано: ", a - len(words.split()))
    return words
    
def usr_val(words):
    """
    Функция позволяет добавить в train_update.csv новые данные для последущего улучшения модели. Если файла train_update.csv нет, он будет создан.
    
    PARAMS:
    words(str) - Ваши слова
    
    RESULT:
    Обновленный файл 
    
    NO RETURN
    """
    tmp = {}
    try:
        df = pd.read_csv("train_update.csv")
    except Exception: 
        df = pd.DataFrame(columns=["W", "T"])
    T = input(">>> Введите компетенцию соответствующую вашим словам: ")
    tmp["W"] = words
    tmp["T"] = T
    df = df.append(tmp, ignore_index=True)
    df.to_csv("train_update.csv")
    print(">>> Спасибо")
    