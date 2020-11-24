print("Loading...")
import pandas as pd
import warnings
warnings.filterwarnings("ignore")
from sklearn.linear_model import LogisticRegression
import pickle
import time
from goto import with_goto
print("Done")
print()
print("Добро подаловать в программу которая вам все быстренько посчитает и выдаст результат.\nВам лишь необходимо следовать инструкциям которые будут у вас на пути.\n\nДанная программа обрабатывает только данные с расширением '.dat',\nуказывать расширение при вводе имен файлов не нужно.\nФайл с данными должен находиться в той же директории что и console.py.\nВ любой момент можно набрать exit и это завершит программу")
print()
@with_goto
def main():
    def sh(data):
        for i in hord:
            data[i] = pd.concat([data[i][145:],data[i][:145]],ignore_index=True)
        for i in rs:
            data[i] = pd.concat([data[i][50:],data[i][:50]],ignore_index=True)

    def newvals(df, data, n):
        df[n + "_mean"]=data.mean(axis=1)
        df[n + "_median"]=data.median(axis=1)
        df[n + "_std"]=data.std(axis=1)
        df[n + "_min"]=data.min(axis=1)
        df[n + "_max"]=data.max(axis=1)
        
    label .restart
    while True:
        while True:
            file = input(">>> Write filename(file must be in the same dir as console.py): ")
            if file =="exit":
                goto .exit
            print(">>> Your file "+ file + ".dat")
            print()
            a=input(">>> Are you sure you want to continue(type 'c'), or retype filename(type 'r'): ")
            if a == 'c':
                break
            elif a =="exit":
                goto .exit
        print()
        print(">>> PreProcessing")
        time.sleep(2)
        try:
            data = pd.read_csv(file+".dat", engine="python", sep="\s+", header=None, skiprows=1, index_col=0)
            data = data.reset_index()
            data = data.drop([0],axis=1)
            hord = [1,2,7,8,11,12,13,14,15,16]
            rs=[3,4,5,6,10]
            sh(data)
            E = [1, 3, 7, 8]
            EC = [9, 11, 15, 16]
            SH = [5, 6, 13, 14]
            newvals(data, data[E], "echo")
            newvals(data, data[EC], "echo_cont")
            newvals(data, data[SH], "shadow")
            data = data[:1020]
            drop = [1,7,8,"echo_min","echo_median","echo_cont_min"]
            data.drop(drop, axis=1, inplace=True)
        except Exception:
            label .a1
            a =  input(">>> Smth went wrong, print 'exit' to stop or 'restart': ")
            if a=="exit":
                break
            elif a == "restart":
                goto .restart
            elif a =="exit":
                goto .exit
            else:
                print(">>> Try again")
                goto .a1
                
        print(">>> PreProcessing Done")
        print()
        print(">>> Loading model")
        time.sleep(2)
        with open("LR_model.pkl", 'rb') as file:
            model = pickle.load(file)
        print(">>> Making prediction")
        pred = model.predict(data)

        mas=[]
        for i in range(len(pred)):
            if pred[i]!=0:
                mas.append(i)
        print()
        print("<====================RESULTS====================>")
        tmp = {"start":[],"end":[]}
        print('start','end')
        print(mas[0], end=' ')
        tmp["start"] = mas[0]
        for i in range(len(mas)-1):
            if mas[i]+1 != mas[i+1]:
                print(mas[i])
                tmp["start"] = mas[i]
                print(mas[i+1], end = " ")
                tmp["end"] = mas[i+1]
        print(mas[-1])
        tmp["end"] = mas[-1]

        df = pd.DataFrame(data=tmp, index=[0])
        
        print("<====================RESULTS====================>")
        print()
        a=input(">>> Do you want to save your results(y/n): ")
        if a == "y":
            fn = input(">>> Please enter filename: ")
            df.to_csv(fn+".csv")
            print("File "+fn+".csv "+"has been saved")

        label .a2
        print(">>> If you are done type 'exit' else type 'restart' to restart")
        a=input()
        if a=="exit":
            label .exit
            break
        elif a=="restart":
            goto .restart
        else:
            print(">>> Try again")
            goto .a2
        
main()

