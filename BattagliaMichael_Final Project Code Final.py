# -*- coding: utf-8 -*-
"""
MICHAEL BATTAGLIA

MET CS 521 A2

Fall 2020

Final Project
"""

import pandas as pd
import matplotlib.pyplot as plt


try:
    #reading data from excel. File path will need to be changed to match current file path
    df = pd.read_excel(r"final project data.xlsx",
                       converters={"Date" : str})
    HRV = df["HRV"] 
    TSS = df["TSS"]
    dates = list(df["Date"])
    dates_trunc = [] #trimming dates to just MM-DD so the plot values are as short as possible
    if len(dates) > 0:
        for i in dates:
            x = i[5:10]
            dates_trunc.append(x)
except Exception as e:
    print(e)
    
#nested dictionary to store HRV and TSS with the correct date
m = {x: {str(y): str(z)} for x, y, z in zip(dates_trunc,HRV,TSS)}

def plot_data(x1, y1, x2, y2):
    """create plot of hrv, tss data on y axis and dates_trunc on x axis"""
    try:
        #HRV Plot
        plt.plot(x1, y1, label = "HRV", color = "red", linewidth = 1)
        #TSS Plot
        plt.plot(x2, y2, label = "TSS", color = "blue", linestyle = "dashed", linewidth = 1)
        
        #Plot Formatting
        plt.xlabel("Day", fontsize = 8)
        plt.ylabel("Metrics", fontsize = 8)
        plt.title("HRV and TSS Over Time")
        plt.legend()
        plt.rcParams.update({"font.size" : 8})
        plt.xticks(fontsize = 4, rotation=90)
        dplt = plt.savefig("HRV and TSS Plot.png", dpi = 300) #saves .png image to current directory
        
    except Exception as e: #if HRV or TSS column in excel file is empty, print ValueError
        print(e, "\n unable to graph data")
    return dplt
        
#HRV Plot
y1 = HRV
x1 = dates_trunc

#TSS Plot
y2 = TSS
x2 = dates_trunc

class AverageHRV():
    __hrv_list = []
    def __init__(self, hrv):
        self.hrv = hrv
        
        for e in self.hrv:
            AverageHRV.__hrv_list.append(float(e))
            
    def avg_of_hrv_list(self): #convert return value to str with 2 decimal places
        return "%.2f" % float(sum(AverageHRV.__hrv_list) / len(AverageHRV.__hrv_list))
       
class AverageTSS():
    __tss_list = []
    def __init__(self, tss):
        self.tss = tss
        
        for e in self.tss:
            AverageTSS.__tss_list.append(float(e))
            
    def avg_of_tss_list(self): #convert return value to str with 2 decimal places
        return "%.2f" % float(sum(AverageTSS.__tss_list) / len(AverageTSS.__tss_list))
    
class Correlation():
    """ Known issue: corr() function returns incorrect result.
        Pearson correlation for top 15 HRV values and top 15 TSS values should be -0.92
    """
    def __init__(self, hrv, tss):
        self.hrv = hrv
        self.tss = tss
        self.corr = self.hrv.corr(self.tss, method = "pearson")
        
    def __str__(self):
        return "{}".format("%.2f" % self.corr) #convert return value to str with 2 decimal places
        
    def corr(self):
        return self.corr

class PrintStatistics():
    def __init__(self, hrv, tss):
        #convert values to str with 2 decimal places
        self.hrv = "%.2f" % float(hrv) 
        self.tss = "%.2f" % float(tss)
        
    def __str__(self):
        return  "HRV Metric is {}, TSS Metric is {}".format(self.hrv, self.tss)


#try/except block raises error if either HRV/TSS list is empty
try:    
    #average, min/max variables
    hrv_avg = AverageHRV(HRV).avg_of_hrv_list()
    tss_avg = AverageTSS(TSS).avg_of_tss_list()
    stats = PrintStatistics(hrv_avg, tss_avg)
    max_val = PrintStatistics(max(HRV), max(TSS))
    min_val = PrintStatistics(min(HRV), min(TSS))

    #correlation variables
    sorted_hrv = sorted(HRV)
    sorted_tss = sorted(TSS)
    hrv_series_15 = pd.Series(sorted_hrv[0:15]) #first five HRV values correspond to lowest values in list
    tss_series_15 = pd.Series(sorted_tss[-15:]) #last five TSS values correspond to highest values in list
    corr_15 = Correlation(hrv_series_15, tss_series_15)
    
    # df = pd.DataFrame({"HRV":sorted_hrv, "TSS":sorted_tss})
    
except Exception as e:
    print("Empty data set error,", e)

def output_statistics(x_input):
    """determine is user wants to see computed statistics"""
    if x_input.lower() == "yes" or x_input.lower() == "y":
        #output data to console
        print("Averages:", stats)
        print("Maximum:", max_val)
        print("Minimum:", min_val)
        print("Top 5 TSS values and bottom 5 HRV correlation:", corr_15)
        plot_data(x1, y1, x2, y2)
        #write data to txt file in current directory. Only write to file if user indicates "yes" or "y"
        var_dict = {"HRV Average: ": hrv_avg, 
                    "TSS Average: ": tss_avg, 
                    "Maximum Values: ": max_val, 
                    "Minimum Values: ": min_val, 
                    "Correlation: ": corr_15}
        file_obj = open("OutputData.txt", "w")
        for k, v in var_dict.items():
            file_obj.write("{} {}".format(k, v) + "\n")
    else: print("Goodbye")
    
#User Input
x = input("Would you like to see some HRV and TSS statistics? Please enter yes or no: ")
output_statistics(x)    





