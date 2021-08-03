from rdkit import Chem
import numpy as np
from rdkit.Chem import Descriptors
import pandas as pd

import pickle
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score



def AromaticAtoms(m):
    aromatic_atoms = [m.GetAtomWithIdx(i).GetIsAromatic() for i in range(m.GetNumAtoms())]
    aa_count = []
    for i in aromatic_atoms:
        if i == True:
            aa_count.append(1)
    sum_aa_count = sum(aa_count)
    return sum_aa_count

def generate(smiles, verbose=False):
    moldata = []
    for elem in smiles:
        mol = Chem.MolFromSmiles(elem)
        moldata.append(mol)

    baseData = np.arange(1, 1)
    i = 0
    for mol in moldata:

        desc_MolLogP = Descriptors.MolLogP(mol)
        desc_MolWt = Descriptors.MolWt(mol)
        desc_NumRotatableBonds = Descriptors.NumRotatableBonds(mol)

        row = np.array([desc_MolLogP,
                        desc_MolWt,
                        desc_NumRotatableBonds])

        if (i == 0):
            baseData = row
        else:
            baseData = np.vstack([baseData, row])
        i = i + 1

    columnNames = ["MolLogP", "MolWt", "NumRotatableBonds"]
    descriptors = pd.DataFrame(data=baseData, columns=columnNames)

    return descriptors



smileString = ['ClCC(Cl)(Cl)Cl', 'COc1cccc2cc(C(=O)NCCCCN3CCN(c4cccc5nccnc54)CC3)oc21']
mol_list= []
for element in smileString:
  mol = Chem.MolFromSmiles(element)
  mol_list.append(mol)

df = generate(smileString)
desc_AromaticProportion = [AromaticAtoms(element) / Descriptors.HeavyAtomCount(element) for element in mol_list]
df_desc_AromaticProportion = pd.DataFrame(desc_AromaticProportion, columns=['AromaticProportion'])
X = pd.concat([df, df_desc_AromaticProportion], axis=1)
print(X)

model = pickle.load(open('model.pkl', 'rb'))

Y_pred_test = model.predict(X)

print(Y_pred_test)
