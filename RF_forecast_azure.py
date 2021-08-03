import warnings
warnings.filterwarnings('ignore')
from dataCleanFun import *
import copy
import pickle
from azure.storage.blob import BlockBlobService
import pandas as pd
import io
import os

def uploadFileToBlob(fileName):
    STORAGEACCOUNTNAME = 'dockerblobstorage123'
    STORAGEACCOUNTKEY = 'hjV9LvwXg42n5ypEssEtq1KohqxbaSmXK18ZshgfmVvi5vaoGA8QXwKdQzwkjE39TfjYWiRIYm1zZ/UPIVZjSw=='
    BLOBNAME = fileName
    CONTAINERNAMEInput = 'forcast'
    blob_service = BlockBlobService(account_name=STORAGEACCOUNTNAME, account_key=STORAGEACCOUNTKEY)
    blob_service.create_blob_from_path(container_name=CONTAINERNAMEInput, blob_name=BLOBNAME,
                                       file_path=os.path.join('./static/uploadstorage', fileName))

def predictOnCSV(fileName):
    # STORAGEACCOUNTNAME = 'dockerblobstorage123'
    # STORAGEACCOUNTKEY = 'hjV9LvwXg42n5ypEssEtq1KohqxbaSmXK18ZshgfmVvi5vaoGA8QXwKdQzwkjE39TfjYWiRIYm1zZ/UPIVZjSw=='
    # LOCALFILENAME = fileName
    # CONTAINERNAMEInput = 'forcast'
    # CONTAINERNAMEOutput = 'result'
    # BLOBNAME = fileName
    #
    # blob_service = BlockBlobService(account_name=STORAGEACCOUNTNAME, account_key=STORAGEACCOUNTKEY)
    # blob_service.get_blob_to_path(CONTAINERNAMEInput, BLOBNAME, LOCALFILENAME)

    # Load data
    current_path=os.getcwd()
    file=current_path+'/static/uploadstorage/'+fileName
    print(file)
    data_raw = pd.read_csv(file)

    # print(data_raw.info())
    data_raw.sample(10)
    M = copy.deepcopy(data_raw)

    dataCleaner = dataCleanFun()
    not_use = ['ProviderCode']
    data_raw = dataCleaner.dropColumns(data_raw, not_use)

    pd.set_option('display.max_columns', None)
    data_raw.describe(include='all')

    # Data pre-processing
    # missing data fill0
    fill0 = [
        'ProviderName',
        'ProviderType',
        'Age at enrolment',
        'Gender',
        'isMaori',
        'isPasifika',
        'isEuropean',
        'isAsian',
        'IsNonMaoriAndNonPasifika',
        'IsUnknownEthnicity',
        'IsDomestic',
        'SchoolDecile',
        'NCEA level',
        'HighestPriorQualification',
        'EnrolmentQualificationCode',
        'WeightedScoreSTEM',
        'WeightedScoreLiteracy',
        'WeightedScoreNumeracy',
        'WeightedScore',
        'Prior years CCR EFTS weighted',
        'Prior years CCR EFTS weighted STEM',
        'Year1EFTS'
    ]

    data_raw = dataCleaner.fillwithNumber(data_raw, fill0, 0)
    print(data_raw.info())

    # onehot encoder
    onehot_column = [
        'ProviderName',
        'ProviderType',
        'Gender',
        'isMaori',
        'isPasifika',
        'isEuropean',
        'isAsian',
        'IsNonMaoriAndNonPasifika',
        'IsUnknownEthnicity',
        'IsDomestic',
        'EnrolmentQualificationCode'
    ]
    data_raw = dataCleaner.transferStringToOneHot(data_raw, onehot_column)
    X = data_raw
    model = pickle.load(open('rf.pkl', 'rb'))
    probs = model.predict_proba(X)
    result = pd.DataFrame(data=probs, columns=["N", "Y"])
    resultDataset = pd.concat([M, result['Y']], axis=1)
    resultfilename=fileName+'_result.csv'
    outputfilename=os.path.join(current_path+'/static/output/',resultfilename)
    resultDataset.to_csv(outputfilename,index_label="idx", encoding="utf-8")
    print("save as csv")
    output = io.StringIO()
    output = resultDataset.to_csv(index_label="idx", encoding="utf-8")

    #blob_service.create_blob_from_text(CONTAINERNAMEOutput, fileName[:-4] + '_Result.csv', output)
    return True

