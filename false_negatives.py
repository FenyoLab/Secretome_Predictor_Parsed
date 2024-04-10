import pandas as pd
import numpy as np
import requests
import os
from sklearn.linear_model import LogisticRegression


def get_protein_name(acc):
    prot_data = requests.get(f"https://www.ebi.ac.uk/proteins/api/proteins/{acc}").json()
    prot_name = ' '
    if 'protein' in prot_data:
        prot_name = prot_data['protein']['recommendedName']['fullName']['value']
    return prot_name


df = pd.read_excel('secreted_proteins_pubmed.xlsx',usecols=['Accession'])
# df = pd.read_csv('Surely_NOT_Secreted.csv', usecols=['Accession','Signal_Peptide'])
# df = df[df['Signal_Peptide'] == '']
results = pd.read_csv('results_database.csv',usecols=['Accession','TOPCONS','Phobius','Predisi',
                                                      'SignalP','SecretomeP','Outcyte','DeepSig'])
pred = pd.merge(df,results)
pred = pred.replace(to_replace={'Y':1,'N':0})
total = pred.shape[0]
print(f"No. of samples: {total}")
check_what = 1
topcons_acc = pred['TOPCONS'].value_counts().to_dict()[check_what]/total
phobius_acc = pred['Phobius'].value_counts().to_dict()[check_what]/total
predisi_acc = pred['Predisi'].value_counts().to_dict()[check_what]/total
signalp_acc = pred['SignalP'].value_counts().to_dict()[check_what]/total
outcyte_acc = pred['Outcyte'].value_counts().to_dict()[check_what]/total
deepsig_acc = pred['DeepSig'].value_counts().to_dict()[check_what]/total
secretomep_acc = pred['SecretomeP'].value_counts().to_dict()[check_what]/total

print("TOPCONS Accuracy:",round(topcons_acc,3))
print("Phobius Accuracy:",round(phobius_acc,3))
print("Predisi Accuracy:",round(predisi_acc,3))
print("SignalP Accuracy:",round(signalp_acc,3))
print("Outcyte Accuracy:",round(outcyte_acc,3))
print("DeepSig Accuracy:",round(deepsig_acc,3))
print("SecretomeP Accuracy:",round(secretomep_acc,3))
pred = pred.replace(to_replace={'Y':1,'N':0})
# for algo in ['TOPCONS', 'Phobius', 'Predisi', 'SignalP',
#        'Outcyte', 'DeepSig']:
#     pred[algo] = pred[algo].replace({1:pred[algo].value_counts().to_dict()[1] / total})
pred['Total'] = np.sum(pred[['TOPCONS', 'Phobius', 'Predisi', 'SignalP',
       'Outcyte', 'DeepSig']],axis=1)

col_names = ['TOPCONS', 'Phobius', 'Predisi', 'SignalP', 'Outcyte', 'DeepSig']

print(pred[pred['Total'] > 0].shape[0]/total)
print(pred[pred['Total'] > 1].shape[0]/total)
print(pred[pred['Total'] > 2].shape[0]/total)
print(pred[pred['Total'] > 3].shape[0]/total)
print(pred[pred['Total'] > 4].shape[0]/total)
print(pred[pred['Total'] > 5].shape[0]/total)
# for n in range(6):
#     for i in range(6):
#         for j in range(6):
#             print(f"{col_names[n]}, {col_names[i]} and {col_names[j]}: "
#                   f"{pred[(pred[col_names[n]] == 1) & (pred[col_names[i]] == 1) & (pred[col_names[j]] == 1)].shape[0]/total}")

pred = pred[(pred['Total'] == 0) & (pred['SecretomeP'] == 0)]
# pred['Name'] = pred['Accession'].apply(get_protein_name)
# pred = pred[['Accession','Name', 'TOPCONS', 'Phobius', 'Predisi', 'SignalP',
#        'Outcyte', 'DeepSig', 'SecretomeP', 'Total']]
# pred.to_csv('false_negatives.csv',index=False)
print(pred.to_string())
print(pred.shape)
