import pandas as pd
import numpy as np


def emAlgo(s,fileDir):
    #Given s, r = (1-s)/s
    r = (1-s)/s
    
    #Reading the datset and loading it into a dataframe and set Xjt = zjt, with Xjt = 0 if j doesn't belong to St
    df = pd.read_csv(fileDir)

    N = df["Total"].copy()
    N0 = r * N.sum()
    
    df = df.drop(df.columns[0], axis=1)
    df = df.drop("Total", axis=1)
    
    #Variables initialization
    T = df.shape[1]
    J = df.shape[0]
    X0 = [[N0/T] for y in range(T)]
    Vj = N/N0
    Y0 = [0 for x in range(T)]
    niter = 1
    x_old = [[1 for x in range(T)] for y in range(J)]
    x_old = pd.DataFrame(data=x_old, index = df.index , columns = df.columns)
    Stop_var = 0.01
    precision = 2
    
    St = []
    StA = np.arange(J)
    S = []
    x = df.copy()
    x = x.replace(np.nan,0)
    y = [[np.nan for x in range(T)] for y in range(J)]
    while True :

        for t in range(0,T):
            for j in range(0,J):
                if not np.isnan(df.iat[j,t]):
                    S.append(j)
            St.append(S[:])
            S.clear()
            negST = list(set(StA)-set(St[t])) 
            for j in range(0,J):
                if j in negST:
                    x.iat[j,t] = round((Vj[j]/(Vj.sum()+1))*((Vj[St[t]].sum()+1)/(Vj[St[t]].sum()))*(df.iloc[St[t],t]).sum(),precision)
                    y[j][t] = -x.iat[j,t]
                else:
                    y[j][t] = round(((Vj[negST].sum())/(Vj.sum()+1)) * df.iat[j,t],precision)
                    x.iat[j,t] = df.iat[j,t]-y[j][t]
                          
            X0[t] = round((1/(Vj.sum()))*(x.loc[:,str(T-t)]).sum(axis=0),precision)
            Y0[t] = round((1/(Vj[St[t]].sum()+1))*x.iloc[negST,t].sum(axis=0),precision)

        print(niter)
        N0 = sum(X0)
        for j in range(0,J):
            N[j] = x.iloc[j].sum()
        Vj= round(N/N0,precision)
        
        flag = True
        test = abs(x.sub(x_old)) > Stop_var
        if True in test.values:
            flag = False
            
        if flag:
            break     
        else:
            niter = niter + 1
            x_old = x.copy()
            
    x["Total"] = N
    print(test)
    x.to_csv (r'x.csv', index = None, header=True)
     

fileDir = "products_data.csv"
emAlgo(0.70,fileDir)