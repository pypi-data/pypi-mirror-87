#!//usr/bin/python3
'''
Package                Version
---------------------- --------------------
csvkit                 1.0.5
fuzzywuzzy             0.18.0
numpy                  1.19.4
p-tqdm                 1.3.3
tqdm                   4.54.0
pandas                 1.1.4
psycopg2-binary        2.8.6
pylint                 2.6.0
python-Levenshtein     0.12.0
SQLAlchemy             1.3.20
xlrd                   1.2.0
psutil

argparse pickle bz2 logging?
'''

import pandas as pd
import numpy as np
import time
import sys
import os
import os.path
import warnings
import argparse
import logging
import pickle
import psutil

from multiprocessing import Pool, freeze_support, cpu_count
from fuzzywuzzy import fuzz

from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

if os.name == "posix":
    from Levenshtein import distance
else:

    def distance(str1, str2):
        return levenshtein_ratio_and_distance(str1, str2)

    warnings.filterwarnings('ignore')

oldmethod = True
if oldmethod:
    from tqdm import tqdm
else:
    import functools
    import p_tqdm.p_tqdm as p_tqdm
    from p_tqdm import p_map

    def monkeypatch(cs) -> None:
        p_tqdm.Pool.map = functools.partial(p_tqdm.Pool.map, chunksize=cs)


# some globals
algo = None
calcTuples = None
tuplefn = None
xlfnAbgleich = None
agents = None
chunksize = None
no_abacus = None
no_names = None
threshold = None
filterOnAlgo = None
op = None
tablename = None
dbconnstr = None
baseDataDir = './data/'

resultValues = {
    'levi-C_Dist': 0,
    'levi-Dist_Lower': 1,
    'levi-Dist_Norm': 2,
    'levi-Dist_Lower_Norm': 3,
    'levi-Dist': 4,
    'levi-Ratio': 5,
    'fuzzy-Ratio': 6,
    'fuzzy-Partial_Ratio': 7,
    'fuzzy-Token_Sort_Ratio': 8,
    'fuzzy-Token_Set_Ratio': 9
}


# #########################################################################
def printGlobals():
    logging.info('running with:')
    logging.info(' agents      : %s', agents)
    logging.info(' chunks      : %s', chunksize)
    logging.info(' abacus      : %s', no_abacus)
    logging.info(' names       : %s', no_names)
    logging.info(' algo        : %s', algo)
    logging.info(' calcTuples  : %s', calcTuples)
    logging.info(' tuplefn     : %s', tuplefn)
    logging.info(' threshold   : %s', threshold)
    logging.info(' filterOnAlgo: %s', filterOnAlgo)
    logging.info(' op          : %s', op)
    logging.info(' tablename   : %s', tablename)
    logging.info(' dbconnstr   : %s', dbconnstr)
    logging.info(' baseDataDir : %s', baseDataDir)
    logging.info(' xlfnAbgleich: %s', xlfnAbgleich)


# ###########################################################################################################################################
def prepareParams():

    global algo
    global calcTuples
    global tuplefn
    global xlfnAbgleich
    global agents
    global chunksize
    global no_abacus
    global no_names
    global threshold
    global filterOnAlgo
    global op
    global tablename
    global dbconnstr

    parser = argparse.ArgumentParser()
    # Add long and short argument
    parser.add_argument("--info", "-i", help="print info", action='store_true')
    parser.add_argument("--agents",
                        "-a",
                        help="# of parallel workers, should be <= # of cpus")
    parser.add_argument("--chunksize", "-c", help="# elements per thread")
    parser.add_argument(
        "--no_abacus",
        "-n",
        help="[all|#]  load # or all values from abacus-xl-sheet")
    parser.add_argument(
        "--no_names",
        "-m",
        help="[all|#]  load # or all values from all 3 names-xl-sheets'")
    parser.add_argument("--algo", "-y", help="[all|algorithm]")
    parser.add_argument("--calcTuples",
                        "-r",
                        help="[y|n] calc new tuplesfile from xl-file?")
    parser.add_argument(
        "--tuplesfile",
        "-d",
        help="name of file to save or load. This filename will be used for result csv as well."
    )
    parser.add_argument(
        "--filterOnAlgo",
        "-f",
        help="[filter-algo|none] if all values are calculated, which one use for filtering?"
    )
    parser.add_argument("--threshold", "-t", help="Filter for output to csv.")
    parser.add_argument("--operator",
                        "-o",
                        help="[>|>=|<=|==] Operator for filter.")
    parser.add_argument("--xlfnAbgleich",
                        "-x",
                        help="xl filename for Abgleich")
    parser.add_argument("--tablename", "-z", help="tablename for database")
    parser.add_argument("--dbconnstr", "-s", help="database connection str")

    # Read arguments from the command line
    args = parser.parse_args()

    # Parameter checking
    if args.tablename:
        tablename = args.tablename
    else:
        tablename = 'comparison'
    logging.info("Set tablename to %s", tablename)

    if args.dbconnstr:
        dbconnstr = args.dbconnstr
    else:
        dbconnstr = 'postgresql+psycopg2://postgres:1qa2ws@localhost:15432/mydb'
    logging.info("Set dbconnstr to %s", dbconnstr)

    if args.agents:
        agents = args.agents
    else:
        agents = cpu_count()
    logging.info("Set agents to %s", agents)

    if args.chunksize:
        chunksize = args.agent
    else:
        chunksize = 100000
    logging.info("Set chunksize to %s", chunksize)

    if args.no_abacus:
        no_abacus = args.no_abacus
        if str(no_abacus).lower() == 'all':
            no_abacus = None
    else:
        no_abacus = 2
    logging.info("Set no_abacus to %s", no_abacus)

    if args.no_names:
        no_names = args.no_names
        if str(no_names).lower() == 'all':
            no_names = None
    else:
        no_names = 10
    logging.info("Set no_names to %s", no_names)

    if args.tuplesfile:
        tuplefn = args.tuplesfile
    else:
        tuplefn = 'test.data'
    logging.info("Set tuplefn to %s", tuplefn)

    if args.algo:
        algo = args.algo
    else:
        algo = 'all'
    logging.info("Set algo to %s", algo)

    if args.calcTuples:
        calcTuples = (str(args.calcTuples).lower() == 'y')
    else:
        calcTuples = True
    logging.info("Set calcTuples to %s", calcTuples)

    if args.threshold:
        agents = args.threshold
    else:
        threshold = 5
    logging.info("Set threshold to %s", threshold)

    if args.operator:
        op = args.operator
    else:
        op = '<'
    logging.info("Set operator to %s", op)

    if args.filterOnAlgo:
        filterOnAlgo = args.filterOnAlgo
        if filterOnAlgo is None:
            threshold = 0
            op = ''
        elif filterOnAlgo.lower() == 'none':
            threshold = 0
            op = ''
    else:
        filterOnAlgo = 'none'
        threshold = 'none'
        op = 'none'
    logging.info("Set filterOnAlgo to %s", filterOnAlgo)
    logging.info("   and threshold to %s", threshold)
    logging.info("   and operator  to %s", op)

    if args.xlfnAbgleich:
        xlfnAbgleich = args.xlfnAbgleich
    else:
        xlfnAbgleich = './input/Abgleich_KUSY_Vorlage.xlsx'
    logging.info("Set xlfnAbgleich to %s", xlfnAbgleich)

    if args.info:
        logging.info('algos          : ')
        for a in resultValues:
            logging.info('               : ', a)
        if not os.name == 'posix':
            logging.info('ACHTUNG: WINDOWS i.d.R. kein Levenshtein-Dist (C)')

        logging.info(
            '--------------------------------------------------------------------------------'
        )
        logging.info('Info: CPUs  = ', cpu_count())
        logging.info(
            'Example     : time python3 main.py 32 10000  all all Levenshtein-Dist y tuples.data fuzzy-Token_Set_Ratio 40 ">" '
        )
        logging.info(
            '              time python3 main.py 32 10000  10  all all              n tuples.data fuzzy-Token_Set_Ratio 40 ">" '
        )
        logging.info(
            '(time python3 main.py 32 100000 all all all  y  tuples.data  none  0 '
            ' 2>&1)|tee main.log')
        exit(1)

    logging.info('Number of arguments:' + str(len(sys.argv)) + 'arguments.')
    logging.info('Argument List:' + str(sys.argv))


# #############################################
def systeminfos():
    logging.info('---------------------------------------------')
    if agents > cpu_count():
        logging.info('ACHTUNG: Agents(' + str(agents) + ') > CPUs(' +
                     str(cpu_count()) + ')')
    else:
        logging.info('Agents(' + str(agents) + ')  OK. CPUs(' +
                     str(cpu_count()) + ')')

    logging.info('---------------------------------------------')

    logging.debug(psutil.virtual_memory())
    logging.debug(psutil.swap_memory())

    vm = psutil.virtual_memory().free
    sm = psutil.swap_memory().free
    all = bytes2human(vm + sm)
    if float(all[:-1]) < 70:
        logging.error(
            'Maybe you have to less memory available. Increase SWAP for huge datafiles! (%s)',
            all)
    else:
        logging.warning('Available memory OK! (%s)', all)

    logging.info('---------------------------------------------')


# ##########################################################################
# python impl (Levenshtein should be C)
# ##########################################################################
def levenshtein_ratio_and_distance(s: str, t: str, ratio_calc=False):
    """ levenshtein_ratio_and_distance:
        Calculates levenshtein distance between two strings.
        If ratio_calc = True, the function computes the
        levenshtein distance ratio of similarity between two strings
        For all i and j, distance[i,j] will contain the Levenshtein
        distance between the first i characters of s and the
        first j characters of t
    """
    # Initialize matrix of zeros
    rows = len(s) + 1
    cols = len(t) + 1
    distance = np.zeros((rows, cols), dtype=int)

    # Populate matrix of zeros with the indeces of each character of both strings
    for i in range(1, rows):
        for k in range(1, cols):
            distance[i][0] = i
            distance[0][k] = k

    # Iterate over the matrix to compute the cost of deletions,insertions and/or substitutions
    for col in range(1, cols):
        for row in range(1, rows):
            if s[row - 1] == t[col - 1]:
                # If the characters are the same in the two strings in a given position [i,j] then the cost is 0
                cost = 0
            else:
                # In order to align the results with those of the Python Levenshtein package, if we choose to calculate the ratio
                # the cost of a substitution is 2. If we calculate just distance, then the cost of a substitution is 1.
                if ratio_calc:
                    cost = 2
                else:
                    cost = 1
            distance[row][col] = min(
                distance[row - 1][col] + 1,  # Cost of deletions
                distance[row][col - 1] + 1,  # Cost of insertions
                distance[row - 1][col - 1] + cost)  # Cost of substitutions
    if ratio_calc:
        # Computation of the Levenshtein Distance Ratio
        Ratio = ((len(s) + len(t)) - distance[row][col]) / (len(s) + len(t))
        return Ratio.__round__(1)
    else:
        # logging.info(distance) # Uncomment if you want to see the matrix showing how the algorithm computes the cost of deletions,
        # insertions and/or substitutions
        # This is the minimum number of edits needed to convert string a to string b
        # return "The strings are {} edits away".format(distance[row][col])
        return distance[row][col]


# ##########################################################################
def trim_all_columns(df):
    """
    Trim whitespace from ends of each value across all series in dataframe
    """
    def trim_strings(x):
        return x.strip() if isinstance(x, str) else x
    return df.applymap(trim_strings)


# ##########################################################################
# https: // www.datacamp.com / community / tutorials / fuzzy - string - python
# ##########################################################################
def choose(ss):
    # pbar.update(1)

    Str1 = ss[0]
    Str2 = ss[1]
    res = []
    if algo == 'all':
        res.append(distance(Str1, Str2))
        res.append(distance(Str1.lower(), Str2.lower()))
        res.append(distance(Str1.replace(' ', ''), Str2.replace(' ', '')))
        res.append(
            distance(
                Str1.replace(' ', '').lower(),
                Str2.replace(' ', '').lower()))
        res.append(levenshtein_ratio_and_distance(Str1, Str2))
        res.append(levenshtein_ratio_and_distance(Str1, Str2, ratio_calc=True))
        res.append(fuzz.ratio(Str1.lower(), Str2.lower()))
        res.append(fuzz.partial_ratio(Str1.lower(), Str2.lower()))
        res.append(fuzz.token_sort_ratio(Str1, Str2))
        res.append(fuzz.token_set_ratio(Str1, Str2))
        return res
    else:
        x = {
            'levi-C_Dist':
            distance(Str1, Str2),
            'levi-Dist_Lower':
            distance(Str1.lower(), Str2.lower()),
            'levi-Dist_Norm':
            distance(Str1.replace(' ', ''), Str2.replace(' ', '')),
            'levi-Dist_Lower_Norm':
            distance(
                Str1.replace(' ', '').lower(),
                Str2.replace(' ', '').lower()),
            'levi-Dist':
            levenshtein_ratio_and_distance(Str1, Str2),
            'levi-Ratio':
            levenshtein_ratio_and_distance(Str1, Str2, ratio_calc=True),
            'fuzzy-Ratio':
            fuzz.ratio(Str1.lower(), Str2.lower()),
            'fuzzy-Partial_Ratio':
            fuzz.partial_ratio(Str1.lower(), Str2.lower()),
            'fuzzy-Token_Sort_Ratio':
            fuzz.token_sort_ratio(Str1, Str2),
            'fuzzy-Token_Set_Ratio':
            fuzz.token_set_ratio(Str1, Str2)
        }.get(algo, 'levi-Dist')
        res.append(x)
        return res


# ##########################################################################
def getNames(cnt):
    namesall = pd.read_excel(xlfnAbgleich,
                             sheet_name=['Sonstige', 'Extra', 'Verzeichnisse'],
                             header=None,
                             skiprows=1,
                             nrows=cnt,
                             usecols=[0])
    allnames = namesall['Extra'].append(namesall['Sonstige'].append(
        namesall['Verzeichnisse'], ignore_index=False),
        ignore_index=False)
    sortnames = allnames.sort_values(by=[0]).drop_duplicates()
    sortnames = trim_all_columns(sortnames)
    logging.info('sortnames: %s', sortnames.size)
    return sortnames


# ##########################################################################
def getAbacus(cnt):
    abacus = pd.read_excel(xlfnAbgleich,
                           sheet_name=['ABACUS_Bestand'],
                           header=None,
                           skiprows=1,
                           nrows=cnt,
                           usecols=[1])
    allabacus = abacus['ABACUS_Bestand']
    sortabacus = allabacus.sort_values(by=[1]).drop_duplicates()
    sortabacus = trim_all_columns(sortabacus)
    logging.info('sortabacus: %s', sortabacus.size)
    return sortabacus


# ##########################################################################
def gentuples(no_abacus, no_names):
    tuples = []
    startload = time.process_time()
    sortabacus = getAbacus(no_abacus)
    sortnames = getNames(no_names)
    endload = time.process_time()

    starttuples = time.process_time()
    i = 0
    for idxabacus, rowabacus in sortabacus.iterrows():
        if type(rowabacus[1]) is not str:
            logging.error('oopsi:' + str(idxabacus) + str(type(rowabacus[1])))
            continue
        if len(rowabacus[1]) == 0:
            logging.error('oopsi:' + str(idxabacus))
            continue
        i = i + 1
        j = 0
        if i % 10 == 0:
            logging.info('abacus-tuples: %i', i)
        for idxnames, rownames in sortnames.iterrows():
            if type(rownames[0]) is not str:
                logging.error('oopsi:' + str(idxnames) +
                              str(type(rownames[0])))
                continue
            if len(rownames[0]) == 0:
                logging.error('oopsi:' + str(idxnames))
                continue
            j = j + 1
            if j % 100000 == 0:
                logging.info('   names: %i', j)
            elements = [rownames[0], rowabacus[1]]
            tuples.append(elements)

    endtuples = time.process_time()

    logging.info('t elapsed load  : %i', endload - startload)
    logging.info('t elapsed tuples: %i', endtuples - starttuples)
    logging.info('tuples          : %i', len(tuples))
    return tuples


# ##########################################################################
def makeUniqueTuples(tuples):
    logging.info("HALLO")
    logging.info("%i %i %s %s", len(tuples), len(tuples[0]), type(tuples),
                 type(tuples[0]))
    print(tuples)
    newT = np.unique(np.array(tuples), axis=0)
    logging.info("%i %i %s %s", len(newT), len(newT[0]), type(newT),
                 type(newT[0]))
    print(newT)

    diff = tuples - newT
    print(diff)
    return newT


# ##########################################################################
def getTuples(no_abacus, no_names, tuplefn):
    logging.info('begin getTuples...')
    if calcTuples:
        tuples = gentuples(no_abacus, no_names)
        logging.info('write tuples...')
        writeObj(tuples, tuplefn)
    else:
        tuples = readObj(tuplefn)
        logging.info('read tuples: %i', len(tuples))

    logging.info("%i %i %s", len(tuples), len(tuples[0]), type(tuples))
    logging.info('end getTuples.')
    return tuples


# #########################################################################
def calcvalues(agents, chunksize, tuples):
    logging.info('begin calc...')
    startcalc = time.process_time()

    if oldmethod:
        # pbar = tqdm(total=len(tuples))
        with Pool(processes=agents) as pool:
            result = pool.map(choose, tuples, chunksize)
    else:
        monkeypatch(chunksize)
        result = p_map(choose, tuples, num_cpus=agents)

    endcalc = time.process_time()
    logging.info("%i %i %s", len(result), len(result[0]), type(result))
    logging.info('t elapsed calc : %i', endcalc - startcalc)
    return result


# # prepare/filter CSV-Array from result########################################################
def prepareFilterCSV(result, tuples, threshold, filterOnAlgo, op, algo):
    logging.info('write csv...')

    startwrite = time.process_time()
    finallist = []

    filtercnt = 0
    for index in range(len(result)):
        newdata = []
        filter = False
        for r in range(len(result[0])):
            # here filter
            if not(filterOnAlgo is None) and not (filterOnAlgo.lower() == 'none'):
                if algo.lower() == 'all':
                    cur = resultValues[filterOnAlgo]
                else:
                    cur = 0
                if cur == r:
                    val = result[index][r]
                    x = eval('val ' + op + ' threshold', {
                        'val': val,
                        'threshold': threshold
                    })
                    if x:
                        newdata.append(result[index][r])
                    else:
                        filtercnt += 1
                        filter = True
                        break
                else:
                    newdata.append(result[index][r])
            else:
                newdata.append(result[index][r])

        if filter:
            continue

        for t in range(len(tuples[0])):
            newdata.append(tuples[index][t])

        finallist.append(newdata)

    endwrite = time.process_time()

    logging.info('filter datasets: %i', filtercnt)
    logging.info('t elapsed write: %i', endwrite - startwrite)
    logging.info('result datasets: %i', len(finallist))

    return finallist


# #########################################################
def getHeaders():
    if algo.lower() == 'all':
        headers = [
            list(resultValues.keys())[0],
            list(resultValues.keys())[1],
            list(resultValues.keys())[2],
            list(resultValues.keys())[3],
            list(resultValues.keys())[4],
            list(resultValues.keys())[5],
            list(resultValues.keys())[6],
            list(resultValues.keys())[7],
            list(resultValues.keys())[8],
            list(resultValues.keys())[9], 'Names', 'AbacusName'
        ]
    else:
        headers = [algo, 'str1', 'str2']

    return headers


# ## Write CSV #######################################################
def write2CSV(finallist, csvfn):
    autolog(str(type(finallist)))
    headers = getHeaders()
    pd.DataFrame(finallist).to_csv(csvfn,
                                   index=True,
                                   header=list(headers),
                                   index_label='Idx')


# #########################################################################
def writeObj(df, dffn):
    # currently up to 4GB only
    autolog(str(type(df)))
    logging.debug("highest protocol: %s", pickle.HIGHEST_PROTOCOL)
    with open(dffn, 'wb') as fp:
        pickle.dump(df, fp, protocol=pickle.HIGHEST_PROTOCOL)


# #########################################################################
def readObj(dffn):
    # currently up to 4GB only
    autolog(str(dffn))
    with open(dffn, 'rb') as fp:
        return pickle.load(fp)


# #########################################################################
def autolog(message):
    "Automatically log the current function details."
    import inspect
    import logging
    # Get the previous frame in the stack, otherwise it would
    # be this function!!!
    func = inspect.currentframe().f_back.f_code
    # Dump the message + the name of this function to the log.
    logging.debug(
        ">>>%s: %s in %s:%i" %
        (message, func.co_name, func.co_filename, func.co_firstlineno))


# #########################################################################
def write2DF(finallist, dffn):
    autolog('Begin w2df')
    headers = getHeaders()

    logging.info("write df")
    data = pd.DataFrame(finallist, columns=list(headers))
    logging.info(data.head())
    logging.debug(data.info())
    writeObj(data, dffn)

    autolog('End w2df')


# #########################################################################
def write2Database(finallist, dbconnstr, tablename):
    autolog('Begin w2db')
    headers = getHeaders()

    engine = create_engine(dbconnstr)
    base = declarative_base()
    metadata = MetaData(engine, reflect=True)
    table = metadata.tables.get(tablename)
    if table is not None:
        logging.info(f'Deleting {tablename} table')
        base.metadata.drop_all(engine, [table], checkfirst=True)

    pd.DataFrame(finallist, columns=list(headers)).to_sql(con=engine,
                                                          name=tablename,
                                                          index=True,
                                                          index_label='Idx',
                                                          chunksize=200000)

    sql = 'SELECT count(*) FROM ' + tablename
    cnt = engine.execute(sql).fetchone()
    logging.info(sql + ' == ' + str(cnt))

    autolog('End w2db')


# #########################################################################
def setlogging():
    logfn = __file__ + '.log'
    file_handler = logging.FileHandler(filename=logfn)
    stdout_handler = logging.StreamHandler(sys.stdout)
    handlers = [file_handler, stdout_handler]

    logging.basicConfig(
        level=logging.DEBUG,
        format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
        handlers=handlers)
    logger = logging.getLogger('LOGGER_NAME')
    logger.setLevel(logging.DEBUG)
    logging.warning("logger: %s", logger)


# #########################################################################
def bytes2human(n):
    # http://code.activestate.com/recipes/578019
    # >>> bytes2human(10000)
    # '9.8K'
    # >>> bytes2human(100001221)
    # '95.4M'
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n


# #########################################################################
def checkDebugEnv():
    gettrace = getattr(sys, 'gettrace', None)
    if gettrace is None:
        logging.debug('No sys.gettrace')
    elif gettrace():
        logging.debug('Hmm, Big Debugger is watching me')
    else:
        logging.debug('Go!')


# #########################################################################
def sql2df():
    autolog('Begin- pandas')

    logging.info("read df")
    df = readObj('df.df')

    # writeObj(df.head(10000), 'mindf.df')
    # print(df.head())
    # print(df.info())

    maxall = df[[
        "fuzzy-Ratio", "fuzzy-Token_Sort_Ratio", "fuzzy-Token_Set_Ratio"
    ]].max(axis=1)
    minall = df[[
        "levi-C_Dist", "levi-Dist_Lower", "levi-Dist_Lower_Norm",
        "levi-Dist_Norm"
    ]].min(axis=1)
    levi_ratio = df['levi-C_Dist'] / df['AbacusName'].apply(len)

    df_add = pd.concat([maxall, minall, levi_ratio],
                       axis=1,
                       keys=['maxfuzzall', 'minleviall', 'levi_ratio'])
    df_ext = pd.concat([df, df_add], axis=1)

    df_ext['RANK_FUZZY'] = df_ext.groupby(['AbacusName'
                                           ])['maxfuzzall'].rank(pct=False)
    df_ext['RANK_LEVENSHTEIN_ALL'] = df_ext.groupby(
        ['AbacusName'])['minleviall'].rank(pct=False)
    df_ext['RANK_LEVENSHTEIN_DIST'] = df_ext.groupby(
        ['AbacusName'])['levi-C_Dist'].rank(pct=False)
    df_ext['RANK_LEVENSHTEIN_RATIO'] = df_ext.groupby(
        ['AbacusName'])['levi_ratio'].rank(pct=False)

    # wherefilter = df_ext[(df_ext["levi-C_Dist"] < 2) &
    #                     (df_ext["fuzzy-Ratio"] > 90)]

    writeObj(df_ext, 'df_ext.df')

    # print(df_ext.info())

    print("-------------------------------------")

    autolog('End - pandas')


# #########################################################################
def dftest():
    autolog('Begin- pandas')

    logging.debug("read df")
    # df_ext
    df = readObj('df_ext.data')
    # print(df.info())
    # print(type(df))
    logging.debug('start where')

    wherefilter = df[(df["levi-C_Dist"] < 2) & (df["fuzzy-Ratio"] > 90)]
    # wherefilter2 = df[   (df["levi-C_Dist"] < 30)      ]

    print(wherefilter)

    autolog('End - pandas')


# #### SQL Alchemy #####################################################################
def databaseTest3():
    autolog('Begin- dbtest3')

    engine = create_engine(dbconnstr)
    base = declarative_base()
    metadata = MetaData(engine, reflect=True)

    table = metadata.tables.get('ALL_MATCHING_RESULTS_EXT')
    if table is not None:
        logging.info('Deleting ALL_MATCHING_RESULTS_EXT table')
        base.metadata.drop_all(engine, [table], checkfirst=True)
    else:
        print('table does not exit!!')


# #########################################################################
def databaseTest2():
    autolog('Begin- read csv')

    csvfn = tuplefn + '.csv'
    data = pd.read_csv(csvfn)
    # Preview the first 5 lines of the loaded data
    logging.info(data.head())

    logging.debug(data.info())
    logging.info("write df")
    writeObj(data, 'df.data')

    logging.info("read df")
    newdf = readObj('df.data')
    logging.info(newdf.head())
    logging.debug(newdf.info())

    # assert(data == newdf)

    engine = create_engine(dbconnstr)
    base = declarative_base()
    metadata = MetaData(engine, reflect=True)
    table = metadata.tables.get(tablename)
    if table is not None:
        logging.info(f'Deleting {tablename} table')
        base.metadata.drop_all(engine, [table], checkfirst=True)

    logging.info(
        "to sql  %s",
        tablename,
    )
    data.to_sql(con=engine,
                name=tablename,
                index=False,
                chunksize=10000,
                method='multi')
    sql = 'SELECT count(*) FROM ' + tablename
    logging.info(engine.execute(sql).fetchone())

    autolog('End - DB test')


# #### SQL Alchemy #####################################################################
def databaseTest():
    autolog('Begin- read csv')

    engine = create_engine(dbconnstr)
    base = declarative_base()
    metadata = MetaData(engine, reflect=True)

    table = metadata.tables.get('ALL_MATCHING_RESULTS_EXT')
    if table is not None:
        logging.info('Deleting ALL_MATCHING_RESULTS_EXT table')
        base.metadata.drop_all(engine, [table], checkfirst=True)

    table = metadata.tables.get('TOP_N_MATCHES')
    if table is not None:
        logging.info('Deleting TOP_N_MATCHES table')
        base.metadata.drop_all(engine, [table], checkfirst=True)

    # sql='SELECT count(*) FROM ' + tablename
    # logging.info(engine.execute(sql).fetchone())

    sql1 = '''
                    CREATE TABLE "ALL_MATCHING_RESULTS_EXT" AS
                    SELECT
                    T.*
                    ,GREATEST("fuzzy-Ratio" ,GREATEST("fuzzy-Token_Sort_Ratio" , "fuzzy-Token_Set_Ratio")) AS "MAX_FUZZY"
                    FROM
                    "ALL_MATCHING_RESULTS" T
                '''

    sql2 = '''
                    CREATE TABLE "TOP_N_MATCHES" AS
                    SELECT
                    "AbacusName"  AS "NAME_ABACUS",
                    "Names"  AS "NAME_OFFICIAL",
                    RANK() OVER (PARTITION BY "AbacusName"  ORDER BY "MAX_FUZZY"  DESC) AS "RANK_FUZZY",
                    RANK() OVER (PARTITION BY "AbacusName" ORDER BY "levi-Dist") AS "RANK_LEVENSHTEIN_DIST",
                    RANK() OVER (PARTITION BY "AbacusName" ORDER BY "levi-Dist" /LENGTH("AbacusName")) AS "RANK_LEVENSHTEIN_RATIO"
                    , "levi-C_Dist"
                    , "levi-Dist"
                    , "levi-Ratio"
                    , "fuzzy-Ratio"
                    , "fuzzy-Partial_Ratio"
                    , "fuzzy-Token_Sort_Ratio"
                    , "fuzzy-Token_Set_Ratio"
                    FROM "ALL_MATCHING_RESULTS_EXT"
                '''

    sql3 = '''
                     SELECT count(*) FROM "TOP_N_MATCHES"
           '''

    sql4 = '''
                    SELECT * FROM "TOP_N_MATCHES"
                    where "levi-Dist" < 5
           '''

    # current sql
    '''
                    DROP TABLE "COMPARISON_EXT"
                    /

                    DROP TABLE "TOP_N_MATCHES_CMP"
                    /

                    CREATE TABLE "COMPARISON_EXT" AS
                    SELECT
                    T.*
                    ,GREATEST("fuzzy-Ratio" ,GREATEST("fuzzy-Token_Sort_Ratio" , "fuzzy-Token_Set_Ratio")) AS "MAX_FUZZY"
                    ,least ("levi-C_Dist" ,least ("levi-Dist_Lower" ,least ("levi-Dist_Lower_Norm" , "levi-Dist_Norm"))) AS "MIN_LEVI"
                    FROM
                    comparison T
                    /

                    DROP TABLE "TOP_N_MATCHES_CMP"
                    /

                    CREATE TABLE "TOP_N_MATCHES_CMP" AS
                        SELECT
                        "AbacusName"  AS "NAME_ABACUS",
                        "Names"  AS "NAME_OFFICIAL",
                        RANK() OVER (PARTITION BY "AbacusName"  ORDER BY "MAX_FUZZY"  DESC) AS "RANK_FUZZY",
                        RANK() OVER (PARTITION BY "AbacusName"  ORDER BY "MIN_LEVI"   ASC) AS "RANK_LEVENSHTEIN_ALL",
                        RANK() OVER (PARTITION BY "AbacusName"  ORDER BY "levi-Dist") AS "RANK_LEVENSHTEIN_DIST",
                        RANK() OVER (PARTITION BY "AbacusName"  ORDER BY "levi-Dist" /LENGTH("AbacusName")) AS "RANK_LEVENSHTEIN_RATIO"
                        , "levi-C_Dist"
                        , "levi-Dist_Lower"
                        , "levi-Dist_Lower_Norm"
                        , "levi-Dist_Norm"
                        , "levi-Dist"
                        , "levi-Ratio"
                        , "fuzzy-Ratio"
                        , "fuzzy-Partial_Ratio"
                        , "fuzzy-Token_Sort_Ratio"
                        , "fuzzy-Token_Set_Ratio"
                        FROM "COMPARISON_EXT"
                    /


                    SELECT count(*) FROM "TOP_N_MATCHES_CMP"
                    /

                    SELECT * FROM "TOP_N_MATCHES_CMP"
                    where "levi-Dist" < 5
    '''

    with engine.connect() as con:
        logging.info('exec 1')
        rs = con.execute(sql1)

        logging.info('exec 2')
        rs = con.execute(sql2)

        logging.info('exec 3')
        rs = con.execute(sql3)
        for row in rs:
            print(row)

        logging.info('exec 4')
        rs = con.execute(sql4)
        for row in rs:
            print(row)

    autolog('End - DB test')


# #########################################################################
def load_resource(r_pkg, r_dir, r_fn):
    from pkg_resources import resource_string, resource_exists

    if resource_exists(r_pkg, f'{r_dir}/{r_fn}'):
        r_data = resource_string(r_pkg, f'{r_dir}/{r_fn}')
        if not os.path.exists(r_dir):
            os.makedirs(r_dir)
        newFile = open(f'{r_dir}/{r_fn}', "wb")
        newFileByteArray = bytearray(r_data)
        newFile.write(newFileByteArray)
        newFile.close()

# #########################################################################
def setupEnvironment():
    # change to current dir
    if not os.path.exists('data'):
        os.makedirs('data')

    if not os.path.exists('docker/db-data'):
        os.makedirs('docker/db-data')

    if not os.path.exists('docker/db-up'):
        os.makedirs('docker/db-up')

    load_resource('abgleich_pkg', 'input', 'Abgleich_KUSY_Vorlage.xlsx')
    load_resource('abgleich_pkg', 'docker', 'docker-compose.yml')
    load_resource('abgleich_pkg', 'docker', 'do_csv_upload.sh')


# ###############################################################################
def mymain(_agents=cpu_count(),
           _chunksize    = 10000,
           _no_abacus    = 2,
           _no_names     = 20,
           _algo         = 'all',
           _calcTuples   = True,
           _tuplesfile   = 'comparison.tuples',
           _filterOnAlgo = None,
           _threshold    = None,
           _operator     = None,
           _xlfnAbgleich = './input/Abgleich_KUSY_Vorlage.xlsx',
           _tablename    = 'comparison',
           _dbconnstr    = 'postgresql+psycopg2://postgres:1qa2ws@localhost:15432/mydb'):
    global algo
    global calcTuples
    global tuplefn
    global xlfnAbgleich
    global agents
    global chunksize
    global no_abacus
    global no_names
    global threshold
    global filterOnAlgo
    global op
    global tablename
    global dbconnstr

    agents       = _agents
    chunksize    = _chunksize
    no_abacus    = _no_abacus
    no_names     = _no_names
    algo         = _algo
    calcTuples   = _calcTuples
    tuplefn      = _tuplesfile
    filterOnAlgo = _filterOnAlgo
    threshold    = _threshold
    op           = _operator
    xlfnAbgleich = _xlfnAbgleich
    tablename    = _tablename
    dbconnstr    = _dbconnstr

    main()


# ###############################################################################
def main():

    systeminfos()
    checkDebugEnv()
    printGlobals()

    # ########################
    # sql2df()
    # databaseTest3()
    # setupEnvironment()()
    # exit(99)
    # ########################

    # doit
    tuples = getTuples(no_abacus, no_names, f'{baseDataDir}/{tuplefn}')
    result = calcvalues(agents, chunksize, tuples)
    writeObj(result, f'{baseDataDir}/{tablename}.result')
    finallist = prepareFilterCSV(result, tuples, threshold, filterOnAlgo, op, algo)
    writeObj(finallist, f'{baseDataDir}/{tablename}.finallist')
    write2CSV(finallist, f'{baseDataDir}/{tablename}.csv')
    write2DF(finallist, f'{baseDataDir}/{tablename}.df')
    # finallist=readObj(   f'{tablename}.finallist')
    if os.name == 'posix':
        try:
            os.chdir('docker')
            os.system('./do_csv_upload.sh')
        except OSError:
            print("Something wrong with specified directory. Exception- ", sys.exc_info())
        finally:
            print("Current directory is-", os.getcwd())
            print('run do_csv_upload.sh manually!')
    else:
        logging.warning(f'system: {os.name}. load make take some time....')
        write2Database(finallist, dbconnstr, tablename)


# #########################################################################
# #########################################################################
if __name__ == "__main__":
    # for windows in combination with pool.map
    freeze_support()

    # define logging
    setlogging()

    # commandline params handling
    prepareParams()

    # change to current dir
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    main()
