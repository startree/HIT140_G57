import pandas as pd
import scipy.stats as sd
import numpy as np
import matplotlib.pyplot as plt
# define the feature dictation:
Feature_dict = {
    "Subject identifier": None, #"This number identifies a study subject",
    "Jitter1": None, #"Jitter in %",
    "Jitter2": None, #"Absolute jitter in microseconds",
    "Jitter3": None, #"Jitter as relative amplitude perturbation (r.a.p.)",
    "Jitter4": None, #"Jitter as 5-point period perturbation quotient (p.p.q.5)",
    "Jitter5": None, #"Jitter as average absolute difference of differences between jitter cycles (d.d.p.)",
    "Shimmer1": None, #"Shimmer in %",
    "Shimmer2": None, #"Absolute shimmer in decibels (dB)",
    "Shimmer3": None,#"Shimmer as 3-point amplitude perturbation quotient (a.p.q.3)",
    "Shimmer4": None,#"Shimmer as 5-point amplitude perturbation quotient (a.p.q.5)",
    "Shimmer5": None,#"Shimmer as 11-point amplitude perturbation quotient (a.p.q.11)",
    "Shimmer6": None,#"Shimmer as average absolute differences between consecutive differences between the amplitudes of shimmer cycles (d.d.a.)",
    "Harmonicity1":None,#"Autocorrelation between NHR and HNR",
    "Harmonicity2":None,#"Noise-to-Harmonic ratio (NHR)",
    "Harmonicity3":None,#"Harmonic-to-Noise ratio (HNR)",
    "Pitch1": None,#"Median pitch",
    "Pitch2": None,#"Mean pitch",
    "Pitch3": None,#"Standard deviation of pitch",
    "Pitch4": None,#"Minimum pitch",
    "Pitch5": None,#"Maximum pitch",
    "Pulse1": None,#"Number of pulses",
    "Pulse2": None,#"Number of periods",
    "Pulse3": None,#"Mean period",
    "Pulse4": None,#"Standard deviation of period",
    "Voice1": None,#"Fraction of unvoiced frames",
    "Voice2": None,#"Number of voice breaks",
    "Voice3": None,#"Degree of voice breaks",
    "UPDRS": None,#"The Unified Parkinsons Disease Rating Scale (UPDRS) score that is assigned to the subject by a physician via a medical examination to determine the severity and progression of Parkinson’s disease.",
    "PD indicator": None,#"Value “1” indicates a subject suffering from PD. Value “0” indicates a healthy subject."     
}
def drawingDistribution(n,df1,df0):
  for i in range(n):
      value = list[i]
      data1 = df1[value]
      data0 = df0[value]
      plt.hist([data1, data0], bins=50, color=['Red', 'Green'], edgecolor='white', label=['Data 1', 'Data 0'])
      # Add the Title and tag
      plt.title(features[i])
      plt.xlabel('Data')
      plt.ylabel('Freqency')
      # show the diagram
      plt.show()
# This function turned the df into a datamap
# Cluster data with SampleVoice number and feature
def clusterbysample(df):
    data_map = {}
    for index, row in df.iterrows():
        sample_voice = row["SampleVoice"]
        for feature in features:
            if feature != 'SampleVoice':
                featureValue = row[feature]
                if sample_voice not in data_map:
                    data_map[sample_voice] = {}
                data_map.setdefault(sample_voice, {}).setdefault(feature, []).append(featureValue)
    return data_map

# read txt into a DataFrame
data = np.loadtxt("po1_data.txt", delimiter=",")

#add the column header
column_headers = Feature_dict.keys()
df = pd.DataFrame(data, columns = column_headers)

# --------Solution D --------
#Assuming each row of each subject 
#with the same vow, giving it a count and make it group
SampleVoice_values = list(range(26)) * 40
df["SampleVoice"] = SampleVoice_values

# Split the Group into two groups
# g1: PD Group
# g0: Common group
g1 = df[df["PD indicator"]==1]
g0 = df[df["PD indicator"]==0]

# Get the list of features
features = df.columns[1:-1]   # Exclude the first column ("Subject identifier") 
# turn g1 into dataMap using clusterbysample
g1DataMap = clusterbysample(g1)
print(g1DataMap[0]['Jitter1'])
g0DataMap = clusterbysample(g0)


print("\nThe significant Features&Voice are:")
list = []
for feature in features:
    for voice in range(26):
        #compare the group of same voice and same feature to find
        #which feature and voice is significant
        list1 = g1DataMap[voice][feature]
        list0 = g0DataMap[voice][feature]
        t_stat, p_value = sd.ttest_ind(list1, list0) 
        if p_value < 0.05: 
            #  resultdf.loc[i, 'significant feature']=i
            print(feature,voice,"       p_value is:",p_value,"      t_stat is:",t_stat)
            turple = (feature, voice)
            # list.append(turple)
            #for i in range(n):
            plt.hist([list1, list0], bins=40, color=['Red', 'Green'], edgecolor='white', label=['Data 1', 'Data 0'])
            # Add the Title and tag
            plt.title(turple)
            plt.xlabel('Data')
            plt.ylabel('Freqency')
            # show the diagram
            plt.show()
 
#drawingDistribution(list,list1,list0)

