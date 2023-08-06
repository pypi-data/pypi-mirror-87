def curvefit(ftoread,ftowrite,ts=1000,density_coeff=5,plot="off"):
    """
    takes 5 parameters file to read, file to write to, max timestep,density coeff and plot ="on" will display plot for given values. 
    assume first column is timesteps starting from 1 and first row is titles(can be empty)
    dilutes to number of timesteps by density_coeff.
    curvefits with respect to timesteps and normalize max value to 1.
    applied to all columns.
    writes 3 files "real" ,"curvefit", "toff (off-rates)"
    """

    from scipy.optimize import curve_fit as cvf
    import numpy as np
    import csv
    import matplotlib.pyplot as plt
    
    csvName = ftoread
    
    csv_file = open(csvName,"r")
    csv_input = csv.reader(csv_file)
    dens_coef = density_coeff
    
     #create an array from csv file until the given timestep
    arr = []
    cof = 0
    ts = ts + 50
    for row in csv_input:
        cof +=1
        if cof<=ts:
            arr.append(row)
    
    
    arr = np.array(arr)
    
    nrow,ncol = arr.shape
    
    exp = int(nrow/dens_coef)
    init_btf = float(arr[1,1])
    
    time = np.zeros(exp)
    value = np.zeros(exp)
    
    tm = np.linspace(0,ts-dens_coef,exp)
    
    
    for i in range(exp):
        time[i] = arr[i*dens_coef+1,0]
    #tm will be used as first columnt reference time list to fit to.
    w = tm.reshape(exp,1)
    
    toff = np.ones(ncol)

    #Every column is curvefit according to time step values.
    tt = -1
    for j in range(ncol):
        tt+=1
        for i in range(1,exp):
            value[i-1] = arr[i*dens_coef,j]
        #curvefit function   
        def func(x, a, b,c ,d):
            return a - b*np.log(x+d)+c*x**0.25
        
        #parameter optimaztion with initial parameters
        popt,pcov = cvf(func,time,value, p0 = [0,-30,30,+30] ,maxfev = 1000000)
        value_fit = func(tm,*popt)
        
        #finding the step where btf = (inital bound tf number/e)
        ii = -1
        for o in value_fit:
            ii+=1
            e = np.e
            tau = init_btf/e
            if o > tau -0.5 and o < tau+0.5 :
                toff[tt] = tm[ii]
                
            elif o > tau-1 and o < tau+1:
                toff[tt] = tm[ii]
                
            elif o > tau-1.5 and o < tau+1.5:
                toff[tt] = tm[ii]
            elif o > tau-2.5 and o < tau+2.5:
                toff[tt] = tm[ii]
                break
        value_fit[0] = init_btf
        value_fit = value_fit/init_btf
        
        #fitted values is turned into column
        value_fit =value_fit.reshape(exp,1)
        
        for index,fraction in enumerate(value_fit):
            
            if fraction > 1:
                value_fit[index]=1
            elif fraction < 0:
                value_fit[index]=0

    
        if j == 0:
            pass
        else:
            #all the values will be appended
            w = np.append(w,value_fit,axis=1)
    
    if plot == "on":
        plt.plot(time,value/init_btf,"b.", label= "real")
        plt.plot(tm,value_fit, "r-", label = "fit")
        plt.show()
    else:
        pass


    arr3 = []
    zero = -1
    delim = int(ts/(dens_coef*10)-1)*dens_coef
    for k in arr:
        zero +=1
        if zero == 1:
            k[0]=0
            arr3.append(k)
        elif zero%delim == 0:
            arr3.append(k)
    csv_file.close()
    arr4 = []
    
    i =0
    while(w[i][0]<=ts-50 and i<len(w)):
        arr4.append(w[i])
        i+=1
    
    #toff file
    toff = 1/toff
    toff = toff.reshape([1,ncol])
    ff = "off" + ftowrite
    np.savetxt(ff,toff,fmt= "%s",delimiter=",")
    print("done " + ff)
    
    #curvefit values file
    arr4 = np.array(arr4)
    orig = "cf" + ftowrite
    np.savetxt(orig,arr4,fmt= "%s",delimiter=",")
    print("done " + orig)
    
    
    arr3 = np.array(arr3)
    nr, nc = arr3.shape
    arr5 = np.zeros([nr-1,nc])
    for h in range(nc):
        for p in range(1,nr):
            arr5[p-1][h] = float(arr3[p][h])/init_btf
            arr5[p-1][0] = float(arr3[p][0])

    #real values file
    pp = "real"+ftowrite
    np.savetxt(pp,arr5,fmt= "%s",delimiter=",")
    print("done " +  pp + "\n")
    return 

if __name__ == "__main__":
    curvefit("ftoread.csv", "ftowrite.csv",1000,5,plot="off")