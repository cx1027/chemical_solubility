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

    mol = Chem.MolFromSmiles(smiles)


    baseData = np.arange(1, 1)


    desc_MolLogP = Descriptors.MolLogP(mol)
    desc_MolWt = Descriptors.MolWt(mol)
    desc_NumRotatableBonds = Descriptors.NumRotatableBonds(mol)

    row = np.array([desc_MolLogP,
                        desc_MolWt,
                        desc_NumRotatableBonds])



    columnNames = ["MolLogP", "MolWt", "NumRotatableBonds"]
    descriptors = pd.DataFrame(data=baseData, columns=columnNames)

    return descriptors



# smileString = 'COc1cccc2cc(C(=O)NCCCCN3CCN(c4cccc5nccnc54)CC3)oc21'

def smileToFeature(smileString):
    mol_list= []

    mol = Chem.MolFromSmiles(smileString)



    desc_AromaticProportion = [AromaticAtoms(mol) / Descriptors.HeavyAtomCount(mol)]
    df_desc_AromaticProportion = pd.DataFrame(desc_AromaticProportion, columns=['AromaticProportion'])
    print(df_desc_AromaticProportion)
    # df = generate(smileString)

    desc_MolLogP = Descriptors.MolLogP(mol)
    desc_MolWt = Descriptors.MolWt(mol)
    desc_NumRotatableBonds = Descriptors.NumRotatableBonds(mol)

    # row = np.array([desc_MolLogP, desc_MolWt, desc_NumRotatableBonds])

    df = pd.DataFrame(columns=['MolLogP', 'MolWt', 'NumRotatableBonds'])
    # df.ilocx[0, 'MolLogP']=10
    MolLogPList = []
    MolWtList = []
    NumRotatableBondsList = []
    MolLogPList.append(desc_MolLogP)
    MolWtList.append(desc_MolWt)
    NumRotatableBondsList.append(desc_NumRotatableBonds)

    dataframe = pd.DataFrame({'MolLogP': MolLogPList, 'MolWt': MolWtList, 'NumRotatableBonds':NumRotatableBondsList})
    # print("dataframe", dataframe)
    df = df.append(dataframe, ignore_index=True)
    print("dataframe")
    print(df)

    X = pd.concat([df, df_desc_AromaticProportion], axis=1, ignore_index=True)
    # print("X")
    return X


