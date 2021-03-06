# -*- coding: utf-8 -*- 

print("Loading modules...")
import warnings
warnings.filterwarnings("ignore")
from sklearn.linear_model import LogisticRegression
import pickle
import time
import re
import numpy as np
from goto import with_goto
import pdfplumber
print("Done")
print()


def pdf_text(filename):
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
    print("bot: Загрузка модели")
    with open(filename, 'rb') as file:
            model = pickle.load(file)
    print("bot: Готово")
    return model
    
def make_pred(model, words, p_num):
    print("bot: Making prediction")
    if p_num==1:
        pred = model.predict([words])
        return pred
    else:
        print()
        print("bot: Внимание, тк вы хотите получить более одного результата, имейте в виду, что результат может не соответствовать вашим ожиданиям.")
        R = []
        allpreds = model.decision_function([words]).reshape(-1)
        for i in allpreds.argsort()[-p_num:][::-1]:
            R.append(model.classes_[i])
        return R
        
def cleaning(w):
    print("bot: Уберем ненужные слова и символы")
    print("bot: Всего слов: ", len(w.split()))
    a=len(w.split()) 
    w = re.sub('[–\n\r."("")"©•,«»:;%$!@#0-9$a-z]', '', w).lower()
    stopwords = ["тд","c","а","алло","без","белый","близко","более","больше","большой","будем","будет","будете","будешь","будто","буду","будут","будь","бы","бывает","бывь","был","была","были","было","быть","в","важная","важное","важные","важный","вам","вами","вас","ваш","ваша","ваше","ваши","вверх","вдали","вдруг","ведь","везде","вернуться","весь","вечер","взгляд","взять","вид","видел","видеть","вместе","вне","вниз","внизу","во","вода","война","вокруг","вон","вообще","вопрос","восемнадцатый","восемнадцать","восемь","восьмой","вот","впрочем","времени","время","все","все еще","всегда","всего","всем","всеми","всему","всех","всею","всю","всюду","вся","всё","второй","вы","выйти","г","где","главный","глаз","говорил","говорит","говорить","год","года","году","голова","голос","город","да","давать","давно","даже","далекий","далеко","дальше","даром","дать","два","двадцатый","двадцать","две","двенадцатый","двенадцать","дверь","двух","девятнадцатый","девятнадцать","девятый","девять","действительно","дел","делал","делать","делаю","дело","день","деньги","десятый","десять","для","до","довольно","долго","должен","должно","должный","дом","дорога","друг","другая","другие","других","друго","другое","другой","думать","душа","е","его","ее","ей","ему","если","есть","еще","ещё","ею","её","ж","ждать","же","жена","женщина","жизнь","жить","за","занят","занята","занято","заняты","затем","зато","зачем","здесь","земля","знать","значит","значить","и","иди","идти","из","или","им","имеет","имел","именно","иметь","ими","имя","иногда","их","к","каждая","каждое","каждые","каждый","кажется","казаться","как","какая","какой","кем","книга","когда","кого","ком","комната","кому","конец","конечно","которая","которого","которой","которые","который","которых","кроме","кругом","кто","куда","лежать","лет","ли","лицо","лишь","лучше","любить","люди","м","маленький","мало","мать","машина","между","меля","менее","меньше","меня","место","миллионов","мимо","минута","мир","мира","мне","много","многочисленная","многочисленное","многочисленные","многочисленный","мной","мною","мог","могу","могут","мож","может","может быть","можно","можхо","мои","мой","мор","москва","мочь","моя","моё","мы","на","наверху","над","надо","назад","наиболее","найти","наконец","нам","нами","народ","нас","начала","начать","наш","наша","наше","наши","не","него","недавно","недалеко","нее","ней","некоторый","нельзя","нем","немного","нему","непрерывно","нередко","несколько","нет","нею","неё","ни","нибудь","ниже","низко","никакой","никогда","никто","никуда","ним","ними","них","ничего","ничто","но","новый","нога","ночь","ну","нужно","нужный","нх","о","об","оба","обычно","один","одиннадцатый","одиннадцать","однажды","однако","одного","одной","оказаться","окно","около","он","она","они","оно","опять","особенно","остаться","от","ответить","отец","откуда","отовсюду","отсюда","очень","первый","перед","писать","плечо","по","под","подойди","подумать","пожалуйста","позже","пойти","пока","пол","получить","помнить","понимать","понять","пор","пора","после","последний","посмотреть","посреди","потом","потому","почему","почти","правда","прекрасно","при","про","просто","против","процентов","путь","пятнадцатый","пятнадцать","пятый","пять","работа","работать","раз","разве","рано","раньше","ребенок","решить","россия","рука","русский","ряд","рядом","с","с кем","сам","сама","сами","самим","самими","самих","само","самого","самой","самом","самому","саму","самый","свет","свое","своего","своей","свои","своих","свой","свою","сделать","сеаой","себе","себя","сегодня","седьмой","сейчас","семнадцатый","семнадцать","семь","сидеть","сила","сих","сказал","сказала","сказать","сколько","слишком","слово","случай","смотреть","сначала","снова","со","собой","собою","советский","совсем","спасибо","спросить","сразу","стал","старый","стать","стол","сторона","стоять","страна","суть","считать","т","та","так","такая","также","таки","такие","такое","такой","там","твои","твой","твоя","твоё","те","тебе","тебя","тем","теми","теперь","тех","то","тобой","тобою","товарищ","тогда","того","тоже","только","том","тому","тот","тою","третий","три","тринадцатый","тринадцать","ту","туда","тут","ты","тысяч","у","увидеть","уж","уже","улица","уметь","утро","хороший","хорошо","хотел бы","хотеть","хоть","хотя","хочешь","час","часто","часть","чаще","чего","человек","чем","чему","через","четвертый","четыре","четырнадцатый","четырнадцать","что","чтоб","чтобы","чуть","шестнадцатый","шестнадцать","шестой","шесть","эта","эти","этим","этими","этих","это","этого","этой","этом","этому","этот","эту","я","являюсь"]
    w = ' '.join([word for word in w.split() if word not in (stopwords)])
    print("bot: Убрано: ", a - len(w.split()))
    return w
    
def helpp():
    print("bot: Если у вас возникли какие-либо проблемы, убедитесь что все ваши файлы находятся в одной директории и вы везде указываете расширение файлов. Если вы считаете что вам выдается неточный результат знайте, что чем больше вы расскажете или напишите в вашем резюме о себе, тeм точнее будет результат.")



@with_goto
def main():
    while True:
        print("bot: Здравствуйте. Cледуйте указаниям и все будет хорошо. Если у вас возникают какие-то проблемы, вы в любой момент можете набрать help и это выведет вам справку с указаниями. Так же в любой момент вы можете набрать exit чтобы выйти.")
        label .restart
        a = input("bot: Введите название вашего pdf файла(с расширением) или опишите словами что вы умеете: \n")
        if a == "help":
            helpp()
            goto .restart
        elif a == "exit":
            break
        elif "pdf" in a:
            print("bot: Ваш файл ",a,"?(y/n)")
            b=input()
            if b == "help":
                helpp()
                goto .restart
            elif b == "exit":
                break
            elif b == "y":
                words = pdf_text(filename=a)
            else: 
                goto .restart
        else: 
            words = a
            print("bot: Вы ввели: ", words)
            c=input("bot: Продолжить? (y/n)")
            if c == "help":
                helpp()
                goto .restart
            elif c == "exit":
                break
            elif c=="n":
                goto .restart

        words = cleaning(words)
        label .loadmodel
        a = input("bot: Введите название вашей модели pkl(model.pkl): ")
        if a == "help":
            helpp()
            goto .loadmodel
        elif a == "exit":
            break
        elif "pkl" in a:
            print("bot: Ваш файл ",a,"?(y/n)")
            b=input()
            if b == "help":
                helpp()
                goto .loadmodel
            elif b == "exit":
                break
            elif b == "y":
                try:
                    model = load_model(filename=a)
                except Exception:
                    print("bot: Что то не так с моделью")
                    goto .loadmodel
            else: 
                goto .loadmodel
        n = int(input("bot: Сколько вы хотите получить предсказанных компетенций: "))
        R = make_pred(model, words, p_num=n)
        print("<========RESULT========>")
        for i in R:
            print(i)
        print("<========RESULT========>")
        break
main()
