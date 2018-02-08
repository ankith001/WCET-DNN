import numpy as np
import matplotlib.pyplot as plt
import pylab
count = 0
summation = []
sum_gpd = []
prob_exceedance = []
sum_cv = []
wcet = []
p = [10 ** -0.000001,10** -0.001,10 **- 0.01, 10** -0.1, 10 ** -0.5, 10 ** -1,10 ** -1.5, 10 ** -2, 10 ** -2.5, 10 ** -3, 10 ** -3.5,  10 ** -4, 10 **-5, 10**-6]
p1 = [10 ** 0, 10 ** -0.0000000001, 10** -0.001, 10 **- 0.01, 10** -0.1, 10 ** -0.5, 10 ** -1,10 ** -1.5, 10 ** -2, 10 ** -2.5, 10 **-3, 10**-6, 10 ** -9, 10 ** -12,10 ** -15, 10 **-18]
#WCET = [0.33,0.36,0.39,0.42,0.45,0.48,0.52,0.56,0.6,0.65] # resize_time
#WCET = [0.0010, 0.0019, 0.0023, .0026,0.0028,0.0030,0.0032, 0.0035, 0.0038, 0.0041, 0.0045, 0.0048, 0.0050, 0.0054]
WCET = [4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 5, 5.1, 5.2, 5.3, 5.4, 5.5]
data1 = np.loadtxt('./txt_files/googlenet_overall_inference_time_1500images_test.txt', dtype = float, delimiter =',')
gev_data = np.multiply(data1,1)
data = np.loadtxt('./txt_files/threshold_single_pixel_values_1500images.txt', dtype = float, delimiter =',')
y_1 = sorted(data, key=(float),reverse = True)
thres_data = np.multiply(y_1,1)
data_1 = np.loadtxt('./txt_files/single_pixel_values_1500images.txt', dtype = float, delimiter =',')
split_y = data_1[:6000]
y_2 = sorted(split_y, key=(float))
train_data = np.multiply(y_2,10**6)
#print train_data
file_size = float(len(y_2))
wcet = []
index = len(thres_data)
last_data = thres_data[index-1]
thres_data[:] = [x - last_data for x in thres_data]
rate = 1/(np.mean(thres_data))
rank = np.linspace(0, 120*max(thres_data),1000000) #change the multiplier depending on sample of data.
rank_length = len(rank)
Probccdf = 1-(1-np.exp(-rank*rate))
rank_data = rank+last_data
pwcetcurve = list(zip(rank_data, Probccdf)) 
#print pwcetcurve
# for generating test samples
for s in p1:
    total = 0
    for i in range(1, rank_length+1):
        total +=1
        if (pwcetcurve[i][1] <= s):
            q = pwcetcurve[i][0]     
            break
    sum_gpd.append(q)
#print summation

#for measured samples

rankeccdf = np.linspace(1, 1/file_size, 6000)
#print rankeccdf
eccdf = sorted(rankeccdf, key = (float))
eccdfcurve = zip(train_data, eccdf)

# MBPTA-CV
u =  0.0046 #threshold value
u1 = [i for i in train_data if i >= u]
u2 = sorted(u1, key=(float), reverse = True)
#print len(u2)
index1 = len(u1)
last_data1 = u2[index1-1]
#print last_data1
u2[:] = [x - last_data1 for x in u2]
#print u2
rate1 = 1/(np.mean(u2))
rank1 = np.linspace(0, 14.98*max(u2),1000000)
rank_length1 = len(rank1)
Probccdf1 = 1-(1-np.exp(-rank1*rate1))
rank_data1 = rank1+last_data1
pwcetcurve1 = list(zip(rank_data1, Probccdf1)) 
#print pwcetcurve
# for generating test samples
for o in p1:
    t = 0
    for i in range(1, rank_length1+1):
        t +=1
        if pwcetcurve1[i][1] <= o:
            f = pwcetcurve1[i][0]     
            break
    sum_cv.append(f)
#print summation
# for measured samples
rankeccdf1 = np.linspace(1, 1/file_size, 6000)
#print rankeccdf
eccdf1 = sorted(rankeccdf1, key = (float))
#print eccdf
eccdfcurve1 = zip(train_data, eccdf1)


# GEV Method               
#b = 50
#k =  -0.268200767294046    # prediction_time.txt
#sigma = 2.97104808576905
#mu = 222.62568344162744

#b = 40                       #overall_inference_time.txt
#k =  -0.239892863585615
#sigma = 3.076595150305488
#mu = 2.220077464410357e+02

#b = 50				#resize_time
#k =  -0.191669941023584
#sigma = 0.036281785185967
#mu =  0.494402303503732

b = 30
k = 0.021830613617241
sigma = 0.077930826159148
mu = 4.850511466792013

for i in p1:
    w = mu - (sigma/k)*(1-(-np.log(1-i))**(-k)) #gev
    wcet.append(w)
for j in WCET:
    count = 0
    for z in gev_data:
        if z > j:
            count +=1  
    summation.append(count)
print (summation)
for s in summation:
    pe = (float(s) / (len(gev_data)))    
    prob_exceedance.append(pe)
print (prob_exceedance)
plt.plot(wcet,p1, label = 'Expected WCET gev method')
plt.plot(WCET, prob_exceedance, label = 'Measured upper bound gev method')
#plt.plot(rank_data, Probccdf, label = 'Expected WCET gpd method')
#plt.plot(train_data, rankeccdf, label = 'Measured upper bound gpd method')
#plt.plot(rank_data1, Probccdf1, label = 'Expected WCET mbpta method')
#plt.plot(train_data, rankeccdf1, label = 'Measured upper bound mbpta method')
plt.yscale('log')
plt.xlabel('WCET (s)', fontsize=7)
plt.ylabel('WCET Exceedance Probability', fontsize=7)
pylab.legend(loc='upper right',fontsize=7)
pylab.xlim(4, 10)
plt.title('Predicted vs Measured Exceedance Probability (Overall Inference Time)',  fontsize=7)
plt.show()










