import numpy as np
import pandas as pd
import subprocess
import os
import time
from itertools import repeat, product, chain
import glob 
import shutil 
from timesmash.utils import BIN_PATH, RANDOM_NAME, getValidKwargs
from multiprocessing import Pool
from sklearn import metrics

#func(param1, param2, **getValidKwargs(func, kwargsDict))

#BIN_PATH = '/home/virotaru/.local/lib/python2.7/site-packages/cynet'
bin_path = BIN_PATH
CYNET_PATH=bin_path + 'cynet'
FLEXROC_PATH=bin_path + 'flexroc'
XgenESeSS_PATH = bin_path + 'XgenESeSS_cynet'

def run_XgenESeSS(to_call):
    out = subprocess.check_output(to_call, shell=True)  
    
def get_auc(args):
    data = args[0][0]
    person = args[0][1]
    models = args[1]
    folder_name = RANDOM_NAME()
    os.mkdir(folder_name)
    for ts in data.index:
        temp_df = pd.DataFrame(data.loc[ts]).T
        temp_df.to_csv('{}/{}'.format(folder_name,ts),index=False, header=False, sep =' ')
    res = []
    for ts in data.index:
        stored_model = models[ts]
        auc, _, _ = _simulateModel(MODEL_PATH = stored_model, DATA_PATH = folder_name+'/', RUNLEN = data.shape[1]).run()
        res.append(auc)
    shutil.rmtree(folder_name)
    df = pd.DataFrame(res).T
    df.columns = [models[name] for name in models]
    df.index = [person]
    return df

class _AUC_Feature:
    def __init__(self,*, pool = Pool,**kwargs):
        self._model_manager = {}
        self._fitted = False
        self._fitted = False
        self._pool = pool
        self._all_kwargs = kwargs
        
    def fit(self, data, labels):
        data = _check_data(data, labels)
        it_list = []
        for label in labels[labels.columns[0]].unique():
            flat_data =  _flatten_data(data, labels, label)
            self._model_manager[label] = _xgModels()._setup_files(flat_data)
            it_list.append(self._model_manager[label]._get_commands())
        with self._pool() as executor:
            it = chain.from_iterable(it_list)
            executor.map(run_XgenESeSS, it)
        '''
        for label in labels[labels.columns[0]].unique():
            print(label)
            print(self._model_manager[label]._models)'''
        self._fitted = True
        return self
    
    def transform(self, data):
        it = _list_of_dataframe_iter(data)
        with self._pool() as executor:
            args = product(it, [self._model_manager[name]._models for name in self._model_manager])
            res = executor.map(get_auc, args)
        features = pd.concat(res, sort=False, axis = 0, join = 'outer' )
        return features.reset_index().groupby('index').max()
    
    def fit_transform(self, data, labels):
        return self.fit(data, labels).transform(data)
    
def _check_data(data, labels):
    index = labels.index
    
    return data

def _list_of_dataframe_iter(data):
    indexes = data[0].index
    for person in indexes:
        person_data =  pd.DataFrame()
        for i, channel in enumerate(data):
            person_data[i] = channel.loc[person]
        person_data = person_data.T
        yield person_data, person

def _flatten_data(data, labels, label):
    labels = labels[labels[labels.columns[0]] == label]
    index = labels.index
    flat_data = pd.DataFrame()
    for i, df in enumerate(data):
        flat_data[i] = df.loc[index].values.flatten()
    return flat_data.T

class _xgModels:
    '''
    Utility class for running XgenESeSS. This class will either run XgenESeSS
    locally or produce the list of commands to run on a cluster. We note that
    you may set the path of XgenESeSS in the yaml file. If running on a cluster
    then the commands will use the path use the XgenESeSS path in the yaml. If
    running on
    Attributes -
        TS_PATH(string)- path to file which has the rowwise multiline
            time series data
        NAME_PATH(string)-path to file with name of the variables
        LOG_PATH(string)-path to log file for xgenesess inference
        BEG(int) & END(int)- xgenesses run parameters (not hyperparameters,
            Beg is 0, End is whatever tempral memory is)
        NUM(int)-number of restarts (20 is good)
        PARTITION(float)-partition sequence
        XgenESeSS_PATH(str)-path to XgenESeSS
        RUN_LOCAL(bool)- whether to run XgenESeSS locally or produce a list of
        commands to run on a cluster.
    '''
    def __init__(self,
                 *,
                 BEG=0,
                 END=0,
                 NUM=40,
                 #PARTITION=[0.5],
                 RUN_LOCAL = True,
                 DERIVATIVE=0,
                 CAP_P=False):



        self.TS_PATH = RANDOM_NAME(clean=False)
        self.NAME_PATH = RANDOM_NAME(clean=False)
        self.FILEPATH = RANDOM_NAME(clean=False)
        self.BEG = BEG
        self.END = END
        self.NUM = NUM
        #self.PARTITION = PARTITION
        self.RUN_LOCAL = RUN_LOCAL
        self.DERIVATIVE = DERIVATIVE
        self._models = {}
        self._commands = []
        self._fitted = True
        self._indexes = True
        if CAP_P:
            self.p = ' -P '
        else:
            self.p = ' -p '

    def _get_commands(self):
        for INDEX, name in enumerate(self._indexes):
            model_file = RANDOM_NAME(clean=False)
            self._models[name] = model_file + 'model.json'
            xgstr = XgenESeSS_PATH +' -f ' + self.TS_PATH\
                 + " -k \"  :" + str(INDEX) +  " \"  -B " + str(self.BEG)\
                 + "  -E " +str(self.END) + ' -n ' +str(self.NUM)\
                 + ' -T symbolic' + ' -N '\
                 + self.NAME_PATH + ' -u '+ str(self.DERIVATIVE) +' -m -G 10000 -v 0 -A 1 -q -w '+  model_file
            yield xgstr


    def _setup_files(self, data):
        pd.DataFrame(data.columns).to_csv(self.FILEPATH, header=False, index=False, sep= '\n', line_terminator = '')
        pd.DataFrame(data.index).to_csv(self.NAME_PATH, header=False, index=False, sep= '\n', line_terminator = '')
        data.to_csv(self.TS_PATH, header=False, index=False, sep = ' ')
        self._indexes = data.index
        return self
            
    def get_model_file(self, variable_name):
        file = self._models[variable_name]
        file_exist = os.path.exists(file)
    
        if not os.path.exists(file) and not self._fitted:
            raise RuntimeError('Model files do not exit. Execute the calls returned by _get_commands method.')
        assert file_exist
                    

    
class _simulateModel:
    '''
    Use the subprocess library to call cynet on a model to process
    it and then run flexroc on it to obtain statistics: auc, tpr, fuc.
    Input -
        MODEL_PATH(string)- The path to the model being processed.
        DATA_PATH(string)- Path to the split file.
        RUNLEN(integer)- Length of the run.
        READLEN(integer)- Length of split data to read from begining
        CYNET_PATH - path to cynet binary.
        FLEXROC_PATH - path to flexroc binary.
    '''

    def __init__(self,*,
                 MODEL_PATH,
                 DATA_PATH,
                 RUNLEN,
                 READLEN=None,
                 DERIVATIVE=0,
                 CAP_P = False,
                 use_flex_roc = False):
        #print(CYNET_PATH)
        assert os.path.exists(CYNET_PATH), "cynet binary cannot be found."
        assert os.path.exists(FLEXROC_PATH), "roc binary cannot be found."
        assert os.path.exists(MODEL_PATH), "model file cannot be found."
        assert any(glob.iglob(DATA_PATH+"*")), \
            "split data files cannot be found."

        self.MODEL_PATH = MODEL_PATH
        self.DATA_PATH = DATA_PATH
        self.RUNLEN = RUNLEN
        self.CYNET_PATH = CYNET_PATH
        self.FLEXROC_PATH = FLEXROC_PATH
        self.RUNLEN = RUNLEN
        self.DERIVATIVE = DERIVATIVE
        self._use_flex_roc = use_flex_roc
        if CAP_P:
            self.p = ' -P '
        else:
            self.p = ' -p '

        if READLEN is None:
            self.READLEN = RUNLEN
        else:
            self.READLEN = READLEN

    def run(self,*,
            LOG_PATH=None,
            #PARTITION=0.5,
            DATA_TYPE='symbolic',
            FLEXWIDTH=1,
            FLEX_TAIL_LEN=-1,
            POSITIVE_CLASS_COLUMN=5,
            EVENTCOL=3,
            tpr_threshold=0.85,
            fpr_threshold=0.15):

        '''
        This function is intended to replace the cynrun.sh shell script. This
        function will use the subprocess library to call cynet on a model to process
        it and then run flexroc on it to obtain statistics: auc, tpr, fuc.
        Input -
           LOG_PATH (string)- Logfile from cynet run
           PARTITION (string)- Partition to use on split data
           FLEXWIDTH (int)-  Parameter to specify flex in flwxroc
           FLEX_TAIL_LEN (int)- tail length of input file to consider [0: all]
           POSITIVE_CLASS_COLUMN (int)- positive class column
           EVENTCOL (int)- event column
           tpr_threshold (float)- minimum tpr threshold
           fpr_threshold (float)- maximum fpr threshold

        Output -
            auc (float)- Area under the curve
            tpr (float)- True positive rate at specified maximum false positive rate
            fpr (float)- False positive rate at specified minimum true positive rate
        '''
        if FLEX_TAIL_LEN == -1:
            FLEX_TAIL_LEN = self.RUNLEN
        if LOG_PATH is None:
            LOG_PATH = RANDOM_NAME()
        cyrstr = self.CYNET_PATH + ' -J ' + self.MODEL_PATH\
            + ' -T ' + DATA_TYPE + ' -N '\
            + str(self.RUNLEN) + ' -x ' + str(self.READLEN)\
            + ' -l ' + LOG_PATH\
            + ' -w ' + self.DATA_PATH + ' -U ' + str(self.DERIVATIVE) + ' -H 0'
        subprocess.check_output(cyrstr, shell=True)
        if not self._use_flex_roc:
            try:
                log_data = pd.read_csv(LOG_PATH, sep = ' ', header = None).dropna(axis=1)
            except:
                return (np.nan, np.nan, np.nan)
            #print(log_data.loc[:,5:])
            multi_class = log_data.shape[1]>6
            if multi_class:
                auc_new = metrics.roc_auc_score(log_data[4], log_data.loc[:,5:], multi_class='ovr')
            else:
                auc_new = metrics.roc_auc_score(log_data[4], log_data.loc[:,6])

            #print(auc_new)

            #auc_new = metrics.auc(fpr, tpr)
            return auc_new, 0, 0

        flexroc_str = self.FLEXROC_PATH + ' -i ' + LOG_PATH\
            + ' -w ' + str(FLEXWIDTH) + ' -x '\
            + str(FLEX_TAIL_LEN) + ' -C '\
            + str(POSITIVE_CLASS_COLUMN) + ' -E ' + str(EVENTCOL)\
            + ' -t ' + str(tpr_threshold) + ' -f ' + str(fpr_threshold)
        #flexstr_arg = shlex.split(flexroc_str)
        output_str = subprocess.check_output(flexroc_str, shell=True)
        results = output_str.split()
        auc = float(results[1])
        tpr = float(results[7])
        fpr = float(results[13])


        return auc_new, tpr, fpr
    
