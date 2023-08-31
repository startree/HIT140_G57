import pandas as pd
import scipy.stats as sd
import numpy as np
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
# read txt into a DataFrame
data = np.loadtxt("po1_data.txt", delimiter=",")

#add the column header
column_headers = Feature_dict.keys()
df = pd.DataFrame(data, columns = column_headers)

# --------Solution C --------
#Assuming each row of each subject 
#with the same vow, giving it a count and make it group
SampleVoice_values = list(range(26)) * 40
df["SampleVoice"] = SampleVoice_values
print(df.head())

# Split the Group into two groups
# g1: PD Group
# g0: Common group
g1 = df[df["PD indicator"]==1]
g0 = df[df["PD indicator"]==0]

#Group the data with the different voice
#And caculate the mean of the voice data
g1 = g1.groupby("SampleVoice").mean()
g0 = g0.groupby("SampleVoice").mean()
#print("The PD Group voice mean is", g1)
#print("The Common Group voice mean is ",g0)

# Get the list of features
features = df.columns[1:-1]  # Exclude the first column ("Subject identifier") 
# Set a dataFrme of significantfeatrue
SignificantFeature = pd.DataFrame(columns=['PD_mean','Normal_mean','PD_Median','PD_IQR','Normal_Median','Normal_IQR','t_stat','p_value'])

# If the p-value is less than 0.05 
# it suggests that there is enough evidence to reject the null hypothesis. 
# This typically means that the observed difference between groups (samples) is statistically significant, 
# and we can conclude that the means of the PD&Common Groups are likely different. 

for i in features:
    t_stat, p_value = sd.ttest_ind(g0[i], g1[i]) 
    if p_value < 0.05:  
      #  resultdf.loc[i, 'significant feature']=i
        SignificantFeature.loc[i,'PD_mean']=np.mean(g1[i])
        SignificantFeature.loc[i,'Normal_mean']=np.mean(g0[i])
        #Calulat the IQR of the PD Group
        SignificantFeature.loc[i,'PD_Median']=np.median(g1[i])
        q11=np.percentile(g1[i],25)
        q13=np.percentile(g1[i],75)
        SignificantFeature.loc[i,'PD_IQR']=q13-q11
        #Calulat the IQR of the Normal Group
        SignificantFeature.loc[i,'Normal_Median']=np.median(g0[i])
        q01=np.percentile(g0[i],25)
        q03=np.percentile(g0[i],75)
        SignificantFeature.loc[i,'Normal_IQR']=q03-q01
        SignificantFeature.loc[i,'t_stat']=t_stat
        SignificantFeature.loc[i,'p_value']=p_value
# Print significant features of solution C:
pd.set_option('display.float_format','{:.8f}'.format)
print("\nSignificant Features:")
print(SignificantFeature)


