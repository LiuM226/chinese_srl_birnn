# encoding:utf-8
import re
import os
import csv
import time
import pickle
import numpy as np
import pandas as pd

csv_name = ["char", "left", "right", "pos", "lpos", "rpos", "rel", "dis", "label"]

#getBatch
def nextBatch(dataSet, start_index, batch_size=128):
    X = dataSet['char']
    X_left = dataSet['left']
    X_right = dataSet['right']
    X_pos = dataSet['pos']
    X_lpos = dataSet['lpos']
    X_rpos = dataSet['rpos']
    X_rel = dataSet['rel']
    X_dis = dataSet['dis']
    y = dataSet['label']

    last_index = start_index + batch_size
    X_batch = list(X[start_index:min(last_index, len(X))])
    X_left_batch = list(X_left[start_index:min(last_index, len(X))])
    X_right_batch = list(X_right[start_index:min(last_index, len(X))])

    X_pos_batch = list(X_pos[start_index:min(last_index, len(X))])
    X_lpos_batch = list(X_lpos[start_index:min(last_index, len(X))])
    X_rpos_batch = list(X_rpos[start_index:min(last_index, len(X))])

    X_rel_batch = list(X_rel[start_index:min(last_index, len(X))])
    X_dis_batch = list(X_dis[start_index:min(last_index, len(X))])
    y_batch = list(y[start_index:min(last_index, len(X))])
    if last_index > len(X):
        left_size = last_index - (len(X))
        for i in range(left_size):
            index = np.random.randint(len(X))
            X_batch.append(X[index])
            X_left_batch.append(X_left[index])
            X_right_batch.append(X_right[index])
            X_pos_batch.append(X_pos[index])
            X_lpos_batch.append(X_lpos[index])
            X_rpos_batch.append(X_rpos[index])
            X_rel_batch.append(X_rel[index])
            X_dis_batch.append(X_dis[index])
            y_batch.append(y[index])
    X_batch = np.array(X_batch)
    X_left_batch = np.array(X_left_batch)
    X_right_batch = np.array(X_right_batch)
    X_pos_batch = np.array(X_pos_batch)
    X_lpos_batch = np.array(X_lpos_batch)
    X_rpos_batch = np.array(X_rpos_batch)
    X_rel_batch = np.array(X_rel_batch)
    X_dis_batch = np.array(X_dis_batch)
    y_batch = np.array(y_batch)

    batches = {}
    batches['char'] = X_batch
    batches['left'] = X_left_batch
    batches['right'] = X_right_batch
    batches['pos'] = X_pos_batch
    batches['lpos'] = X_lpos_batch
    batches['rpos'] = X_rpos_batch
    batches['rel'] = X_rel_batch
    batches['dis'] = X_dis_batch
    batches['label'] = y_batch
    return batches

#getRandomBatch
def nextRandomBatch(dataSet, batch_size=128):
    X = dataSet['char']
    X_left = dataSet['left']
    X_right = dataSet['right']
    X_pos = dataSet['pos']
    X_lpos = dataSet['lpos']
    X_rpos = dataSet['rpos']
    X_rel = dataSet['rel']
    X_dis = dataSet['dis']
    y = dataSet['label']

    X_batch = []
    X_left_batch = []
    X_right_batch = []
    X_pos_batch = []
    X_lpos_batch = []
    X_rpos_batch = []
    X_rel_batch = []
    X_dis_batch = []
    y_batch = []
    for i in range(batch_size):
        index = np.random.randint(len(X))
        X_batch.append(X[index])
        X_left_batch.append(X_left[index])
        X_right_batch.append(X_right[index])
        X_pos_batch.append(X_pos[index])
        X_lpos_batch.append(X_lpos[index])
        X_rpos_batch.append(X_rpos[index])
        X_rel_batch.append(X_rel[index])
        X_dis_batch.append(X_dis[index])
        y_batch.append(y[index])
    X_batch = np.array(X_batch)
    X_left_batch = np.array(X_left_batch)
    X_right_batch = np.array(X_right_batch)
    X_pos_batch = np.array(X_pos_batch)
    X_lpos_batch = np.array(X_lpos_batch)
    X_rpos_batch = np.array(X_rpos_batch)
    X_rel_batch = np.array(X_rel_batch)
    X_dis_batch = np.array(X_dis_batch)
    y_batch = np.array(y_batch)

    batches = {}
    batches['char'] = X_batch
    batches['left'] = X_left_batch
    batches['right'] = X_right_batch
    batches['pos'] = X_pos_batch
    batches['lpos'] = X_lpos_batch
    batches['rpos'] = X_rpos_batch
    batches['rel'] = X_rel_batch
    batches['dis'] = X_dis_batch
    batches['label'] = y_batch
    return batches

# use "0" to padding the sentence
def padding(sample, seq_max_len):
    for i in range(len(sample)):
        if len(sample[i]) < seq_max_len:
            sample[i] += [0 for _ in range(seq_max_len - len(sample[i]))]
    return sample

#prepare data as feature[seqtence[word]]
def prepare(chars, lefts, rights, poss, lposs, rposs, rels, diss, labels, seq_max_len, is_padding=True):
    X = []
    X_left = []
    X_right = []
    X_pos = []
    X_lpos = []
    X_rpos = []
    X_rel = []
    X_dis = []
    y = []

    tmp_x = []
    tmp_left = []
    tmp_right = []
    tmp_pos = []
    tmp_lpos = []
    tmp_rpos =[]
    tmp_rel = []
    tmp_dis = []
    tmp_y = []

    for record in zip(chars, lefts, rights, poss, lposs, rposs, rels, diss, labels):
        c = record[0]
        lc = record[1]
        rc = record[2]
        p = record[3]
        lp = record[4]
        rp = record[5]
        rl = record[6]
        d = record[7]
        l = record[8]
        # empty line
        if c == -1:
            if len(tmp_x) <= seq_max_len:
                X.append(tmp_x)
                X_left.append(tmp_left)
                X_right.append(tmp_right)
                X_pos.append(tmp_pos)
                X_lpos.append(tmp_lpos)
                X_rpos.append(tmp_rpos)
                X_rel.append(tmp_rel)
                X_dis.append(tmp_dis)
                y.append(tmp_y)
            tmp_x = []
            tmp_left = []
            tmp_right = []
            tmp_pos = []
            tmp_lpos = []
            tmp_rpos =[]
            tmp_rel = []
            tmp_dis = []
            tmp_y = []
        else:
            tmp_x.append(c)
            tmp_left.append(lc)
            tmp_right.append(rc)
            tmp_pos.append(p)
            tmp_lpos.append(lp)
            tmp_rpos.append(rp)
            tmp_rel.append(rl)
            tmp_dis.append(int(d))
            tmp_y.append(l)
    if is_padding:
        X = np.array(padding(X, seq_max_len))
        X_left = np.array(padding(X_left, seq_max_len))
        X_right = np.array(padding(X_right, seq_max_len))
        X_pos = np.array(padding(X_pos, seq_max_len))
        X_lpos = np.array(padding(X_lpos, seq_max_len))
        X_rpos = np.array(padding(X_rpos, seq_max_len))
        X_rel = np.array(padding(X_rel, seq_max_len))
        X_dis = np.array(padding(X_dis, seq_max_len))
    else:
        X = np.array(X)
        X_left = np.array(X_left)
        X_right = np.array(X_right)
        X_pos = np.array(X_pos)
        X_lpos = np.array(X_lpos)
        X_rpos = np.array(X_rpos)
        X_rel = np.array(X_rel)
        X_dis = np.array(X_dis)
    y = np.array(padding(y, seq_max_len))
    return X, X_left, X_right, X_pos, X_lpos, X_rpos, X_rel, X_dis, y

#loac dictionary
def loadMap(token2id_filepath):
    if not os.path.isfile(token2id_filepath):
        print "file not exist, building map"
        buildMap()

    token2id = {}
    id2token = {}
    with open(token2id_filepath) as infile:
        for row in infile:
            row = row.rstrip().decode("utf-8")
            token = row.split('\t')[0]
            token_id = int(row.split('\t')[1])
            token2id[token] = token_id
            id2token[token_id] = token
    return token2id, id2token

#save dictionary
def saveMap(id2char, id2pos, id2label):
    with open("char2id", "wb") as outfile:
        for idx in id2char:
            outfile.write(id2char[idx] + "\t" + str(idx) + "\r\n")
    with open("pos2id", "wb") as outfile:
        for idx in id2pos:
            outfile.write(id2pos[idx] + "\t" + str(idx) + "\r\n")
    with open("label2id", "wb") as outfile:
        for idx in id2label:
            outfile.write(id2label[idx] + "\t" + str(idx) + "\r\n")
    print "saved map between token and id"

#build dictionary
def buildMap(train_path="train.in"):
    df_train = pd.read_csv(train_path, delimiter='\t', quoting=csv.QUOTE_NONE, skip_blank_lines=False, header=None, names=csv_name)
    
    chars = list(set(df_train["char"][df_train["char"].notnull()]))
    poses = list(set(df_train["pos"][df_train["pos"].notnull()]))
    labels = list(set(df_train["label"][df_train["label"].notnull()]))

    char2id = dict(zip(chars, range(1, len(chars) + 1)))
    pos2id = dict(zip(poses, range(1, len(poses) + 1)))
    label2id = dict(zip(labels, range(1, len(labels) + 1)))

    id2char = dict(zip(range(1, len(chars) + 1), chars))
    id2pos = dict(zip(range(1, len(poses) + 1), poses))
    id2label = dict(zip(range(1, len(labels) + 1), labels))

    id2char[0] = "<PAD>"
    id2pos[0] = "<PAD>"
    id2label[0] = "<PAD>"

    char2id["<PAD>"] = 0
    pos2id["<PAD>"] = 0
    label2id["<PAD>"] = 0

    id2char[len(chars) + 1] = "<NEW>"
    id2pos[len(chars) + 1] = "<NEW>"
    char2id["<NEW>"] = len(chars) + 1
    pos2id["<NEW>"] = len(poses) + 1

    saveMap(id2char, id2pos, id2label)

    return char2id, id2char, pos2id, id2pos, label2id, id2label

#get train data
def getTrain(train_path, val_path, train_val_ratio=0.99, use_custom_val=False, seq_max_len=200):
    char2id, id2char, pos2id, id2pos, label2id, id2label = buildMap(train_path)
    #read input file
    df_train = pd.read_csv(train_path, delimiter='\t', quoting=csv.QUOTE_NONE, skip_blank_lines=False, header=None, names=csv_name)

    # map the word, pos and label into id
    df_train["char_id"] = df_train.char.map(lambda x: -1 if str(x) == str(np.nan) else char2id[x])
    df_train["left_id"] = df_train.left.map(lambda x: -1 if str(x) == str(np.nan) else char2id[x])
    df_train["right_id"] = df_train.right.map(lambda x: -1 if str(x) == str(np.nan) else char2id[x])
    df_train["rel_id"] = df_train.rel.map(lambda x: -1 if str(x) == str(np.nan) else char2id[x])
    
    df_train["pos_id"] = df_train.pos.map(lambda x: -1 if str(x) == str(np.nan) else pos2id[x])
    df_train["lpos_id"] = df_train.lpos.map(lambda x: -1 if str(x) == str(np.nan) else pos2id[x])
    df_train["rpos_id"] = df_train.rpos.map(lambda x: -1 if str(x) == str(np.nan) else pos2id[x])
    
    df_train["label_id"] = df_train.label.map(lambda x: -1 if str(x) == str(np.nan) else label2id[x])

    # convert the data in maxtrix
    X, X_left, X_right, X_pos, X_lpos, X_rpos, X_rel, X_dis, y = prepare(df_train["char_id"], df_train["left_id"], df_train["right_id"],
        df_train["pos_id"], df_train["lpos_id"], df_train["rpos_id"],
        df_train["rel_id"], df_train["dis"], df_train["label_id"], seq_max_len)

    # shuffle the samples
    num_samples = len(X)
    indexs = np.arange(num_samples)
    np.random.shuffle(indexs)
    X = X[indexs]
    X_left = X_left[indexs]
    X_right = X_right[indexs]
    X_pos = X_pos[indexs]
    X_lpos = X_lpos[indexs]
    X_rpos = X_rpos[indexs]
    X_rel = X_rel[indexs]
    X_dis = X_dis[indexs]
    y = y[indexs]

    #get dev data
    if val_path != None:
        X_train = X
        X_left_train = X_left
        X_right_train = X_right
        X_pos_train = X_pos
        X_lpos_train = X_lpos
        X_rpos_train = X_rpos
        X_rel_train = X_rel
        X_dis_train = X_dis
        y_train = y
        X_val, X_left_val, X_right_val, X_pos_val, X_lpos_val, X_rpos_val, X_rel_val, X_dis_val, y_val = getTest(val_path, is_validation=True, seq_max_len=seq_max_len)
    print "train size: %d, validation size: %d" % (len(X_train), len(y_val))

    #return train data
    train_data = {}
    train_data['char'] = X_train
    train_data['left'] = X_left_train
    train_data['right'] = X_right_train
    train_data['pos'] = X_pos_train
    train_data['lpos'] = X_lpos_train
    train_data['rpos'] = X_rpos_train
    train_data['rel'] = X_rel_train
    train_data['dis'] = X_dis_train
    train_data['label'] = y_train

    #return dev data
    val_data = {}
    val_data['char'] = X_val
    val_data['left'] = X_left_val
    val_data['right'] = X_right_val
    val_data['pos'] = X_pos_val
    val_data['lpos'] = X_lpos_val
    val_data['rpos'] = X_rpos_val
    val_data['rel'] = X_rel_val
    val_data['dis'] = X_dis_val
    val_data['label'] = y_val

    return train_data, val_data

#get test data
def getTest(test_path="test.in", is_validation=False, seq_max_len=200):
    char2id, id2char = loadMap("char2id")
    pos2id, id2pos = loadMap("pos2id")
    label2id, id2label = loadMap("label2id")
    #read input file
    df_test = pd.read_csv(test_path, delimiter='\t', quoting=csv.QUOTE_NONE, skip_blank_lines=False, header=None, names=csv_name)

    #map str to id
    def mapFunc(x, token2id):
        if str(x) == str(np.nan):
            return -1
        elif x.decode("utf-8") not in token2id:
            return token2id["<NEW>"]
        else:
            return token2id[x.decode("utf-8")]

    #get ids for feature
    df_test["char_id"] = df_test.char.map(lambda x: mapFunc(x, char2id))
    df_test["left_id"] = df_test.left.map(lambda x: mapFunc(x, char2id))
    df_test["right_id"] = df_test.right.map(lambda x: mapFunc(x, char2id))
    df_test["rel_id"] = df_test.rel.map(lambda x: mapFunc(x, char2id))
    df_test["pos_id"] = df_test.pos.map(lambda x: mapFunc(x, pos2id))
    df_test["lpos_id"] = df_test.lpos.map(lambda x: mapFunc(x, pos2id))
    df_test["rpos_id"] = df_test.rpos.map(lambda x: mapFunc(x, pos2id))
    df_test["label_id"] = df_test.label.map(lambda x: -1 if str(x) == str(np.nan) else label2id[x])

    #prepare data
    X_test, X_left_test, X_right_test, X_pos_test, X_lpos_test, X_rpos_test, X_rel_test, X_dis_test, y_test = prepare(
        df_test["char_id"], df_test["left_id"], df_test["right_id"], 
        df_test["pos_id"], df_test["lpos_id"], df_test["rpos_id"], 
        df_test["rel_id"], df_test["dis"], df_test["label_id"], seq_max_len)
    if is_validation:
        return X_test, X_left_test, X_right_test, X_pos_test, X_lpos_test, X_rpos_test, X_rel_test, X_dis_test, y_test
    else:
        return X_test, X_left_test, X_right_test, X_pos_test, X_lpos_test, X_rpos_test, X_rel_test, X_dis_test

#regular B/I/S/E flag for a line
def regularName(beginIndex, lastIndex, line):
    if beginIndex == lastIndex - 1:
        line[beginIndex] = 'S-' + line[beginIndex]
        return
    line[beginIndex] = 'B-' + line[beginIndex]
    for i in range(beginIndex + 1, lastIndex - 1):
        line[i] = 'I-' + line[i]
    line[lastIndex - 1] = 'E-' + line[lastIndex - 1]

#regular B/I/S/E flag for a dataSet
def regularPred(preds_lines):
    for i in range(len(preds_lines)):
        preds_line = preds_lines[i]
        
        lastname = ''
        beginIndex = -1
        names_line = []
        labels_line = []
        for j in range(len(preds_line)):
            item = preds_line[j]
            word, pos, label = item.split('/')[0], item.split('/')[1], item.split('/')[-1]
            
            flag, name = label[:label.find('-')], label[label.find('-')+1:]
            if label == 'O' or label == 'rel':
                if lastname != '':
                    regularName(beginIndex, j, names_line)
                lastname = ''
                names_line.append(label)
            elif flag == 'S' or flag == 'I' or flag == 'B' or flag == 'E':
                if name != lastname: # take only name
                    if lastname != '':
                        regularName(beginIndex, j, names_line)
                    lastname = name
                    beginIndex = j
                names_line.append(name)
            else:
                name = label
                if name != lastname:
                    if lastname != '':
                        regularName(beginIndex, j, names_line)
                    lastname = name
                    beginIndex = j
                names_line.append(name)

            labels_line.append(label)

            if j == len(preds_line) - 1:
                if lastname != '':
                    regularName(beginIndex, j+1, names_line)

        for j in range(len(preds_line)):
            item = preds_line[j]
            word, pos = item.split('/')[0], item.split('/')[1]
            name = names_line[j]
            preds_line[j] = word.strip('\n') + '/' + pos.strip('\n') + '/' + name.strip('\n')

#calc_f1 as calc_f1.py
def calc_f1(preds_lines, id2label, gold_file, outfile):
    case_true, case_recall, case_precision = 0, 0, 0
    golds_lines = open(gold_file, 'r').read().strip().split('\n')
    golds = [gold.split() for gold in golds_lines]
    preds = []
    for i in range(len(preds_lines)):
        preds_line = preds_lines[i]
        golds_line = golds_lines[i]
        str_preds_line = []
        str_preds = [str(id2label[val].encode("utf-8")) for val in preds_line]
        for t in range(len(str_preds)):
            str_preds_line.append(golds[i][t] + '/' + str_preds[t])
        preds.append(str_preds_line)
    regularPred(preds)
    assert len(golds) == len(preds), "length of prediction file and gold file should be the same."
    outputFile = open(outfile, 'w')
    for line in preds:
        for item in line:
            word, tlabel, label = item.split('/')[0], item.split('/')[-2], item.split('/')[-1]
            outputFile.write(word + '\t\t' + tlabel + '\t\t' + label + '\n')
        outputFile.write('\n')
    outputFile.close()
    for gold, pred in zip(golds, preds):
        lastname = ''
        keys_gold, keys_pred = {}, {}
        for item in gold:
            word, label = item.split('/')[0], item.split('/')[-1]
            flag, name = label[:label.find('-')], label[label.find('-')+1:]
            if flag == 'O' or flag == 'rel':
                continue
            if flag == 'S':
                if name not in keys_gold:
                    keys_gold[name] = [word]
                else:
                    keys_gold[name].append(word)
            else:
                if flag == 'B':
                    if name not in keys_gold:
                        keys_gold[name] = [word]
                    else:
                        keys_gold[name].append(word)
                    lastname = name
                elif flag == 'I' or flag == 'E':
                    assert name == lastname, "the I-/E- labels are inconsistent with B- labels in gold file."
                    keys_gold[name][-1] += ' ' + word
        lastname = ''
        for item in pred:
            word, label = item.split('/')[0], item.split('/')[-1]
            flag, name = label[:label.find('-')], label[label.find('-')+1:]
            if flag == 'O' or flag == 'rel':
                continue
            if flag == 'S':
                if name not in keys_pred:
                    keys_pred[name] = [word]
                else:
                    keys_pred[name].append(word)
            else:
                if flag == 'B':
                    if name not in keys_pred:
                        keys_pred[name] = [word]
                    else:
                        keys_pred[name].append(word)
                    lastname = name
                elif flag == 'I' or flag == 'E':
                    if name != lastname:
                        if lastname not in keys_pred:
                            keys_pred[lastname] = ['error']
                        else:
                            keys_pred[lastname][-1] = 'error'
                    else:
                        if name not in keys_pred:
                            keys_pred[name] = ['error']
                        else:
                            keys_pred[name][-1] += ' ' + word
        
        for key in keys_gold:
            case_recall += len(keys_gold[key])
        errors = 0
        for key in keys_pred:
            case_precision += len(keys_pred[key])
            for word in keys_pred[key]:
                if word == 'error':
                    errors += 1
        case_precision -= errors

        for key in keys_pred:
            if key in keys_gold:
                for word in keys_pred[key]:
                    if word != 'error' and word in keys_gold[key]:
                        case_true += 1
                        keys_gold[key].remove(word) # avoid replicate words
    if case_recall == 0:
        case_recall = 1
    if case_precision == 0:
        case_precision = 1
    recall = 1.0 * case_true / case_recall
    precision = 1.0 * case_true / case_precision
    f1 = 2.0 * recall * precision / (recall + precision)
    return recall, precision, f1, errors
