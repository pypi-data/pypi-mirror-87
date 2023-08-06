import sys, json, pkg_resources
from pandas import read_csv

from datetime import datetime
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from hangul.crf import CRF

class WordSegmenter:

    tags = ['0', '1']
    n_tags = len(tags)
    crf = CRF(n_tags, sparse_target = True, supports_masking = False,
        sequence_lengths = None, transitions=None)
    custom_objects={'CRF': CRF,
                    'loss': crf.loss,
                    'crf_loss': crf.loss,
                   'viterbi_accuracy': crf.accuracy}
    tag2idx = {t: i for i, t in enumerate(tags)}
    tag2idx['充'] = 1 

    def __init__(self):
        modelFile = pkg_resources.resource_filename(__name__, "models/model_th5.hdf5")
        word2idxFile = pkg_resources.resource_filename(__name__, "data/word2idx0.json")
        self._model = load_model(modelFile, custom_objects=WordSegmenter.custom_objects)
        self._layer = self._model.get_layer(index=0)
        self._max_len = self._layer.output_shape[1]
        with open(word2idxFile, 'r') as afile:
            self.word2idx = json.load(afile)
        self._infile = None
        self._passage = None
        now = datetime.now()
        suffix = now.strftime("_%y%j_%H%M")
        self._outfile = "segmented" + suffix  + ".txt"
        self._testli = list()
        self.passageSegmented = ''

    def infile(self, fileName):
        self._infile = fileName

    def outfile(self, fileName):
        self._outfile = fileName

    def inputAsString(self, aStr):
        self._passage = aStr

    @property
    def testli(self):
        return self._testli

    @property
    def max_len(self):
        return self._max_len

    @max_len.setter
    def max_len(self, v):
        self._max_len = v

    @property
    def passage(self):
        return self._passage

    @staticmethod
    def lettersNonoffs(seq):
      simpleseq = []
      onoff = []
      space = True
      for i in range(len(seq)):
        ch = seq[i]
        if ch == ' ':
            space = True
            continue
        if space:
            onoff.append('1')
        else:
            onoff.append('0')
        simpleseq.append(ch)
        space = False
        if not len(simpleseq) == len(onoff):
          print("Calculation seriously flawed! Stop processing!")
          print("simpleseq", str(len(simpleseq)))
          print("onoff", str(len(onoff)))
          print(seq)
          break
      return simpleseq, onoff

    @staticmethod
    def cutintopieces(kul, lnth):
        ans = [0]
        last = 0
        j = 1
        kullen = len(kul)
        for i in range(0, kullen):
            if kul[i] == ' ':
                if i > j * lnth - 1:
                    if ans[-1] != last:
                        ans.append(last)
                    j += 1
                last = i
        if i > j * lnth - 1:
            ans.append(last)
        ans.append(kullen)
        return ans

    @staticmethod
    def halve(aLine):
        kili = len(aLine) // 2 + 1
        return [aLine[:kili], aLine[kili:]]

    @staticmethod
    def halveLines(lis, threshold):
        lis2 = list()
        for ln in lis:
            if len(ln) > threshold:
                lis2.extend(WordSegmenter.halve(ln))
            else:
                lis2.append(ln)
        return lis2

    def doSegment(self):
        self._testli = list()
        if self._infile == None:
            if self.passage == None:
                sys.exit("\tOops! No passage has been given for this software to segment!\n\
\tPlease specify a file or a string with infile(aFile) or\n\
\tinputAsString(\"대전까지가는데몇시간걸리지?\")")
            points = WordSegmenter.cutintopieces(self.passage, self.max_len)
            for i in range(0, len(points) - 1):
                st = points[i]
                end = points[i + 1]
                ls, oos = WordSegmenter.lettersNonoffs(self.passage[st:end])
                self.testli.append(list(zip(ls, oos)))
            self.passageSegmented = self.segmentproper(self.testli)
        else:
            df = read_csv(self._infile, header=None, sep="\n", encoding = "utf-8",
                    error_bad_lines=True)
            for _, j in df.iterrows():
                points = WordSegmenter.cutintopieces(j[0], self.max_len)
                for i in range(0, len(points) - 1):
                    st = points[i]
                    end = points[i + 1]
                    ls, oos = WordSegmenter.lettersNonoffs(j[0][st:end])
                    self.testli.append(list(zip(ls, oos)))
            self.passageSegmented = self.segmentproper(self.testli)
            with open(self._outfile, "w") as outFile:
                outFile.write(self.passageSegmented)

    def reconstruct(self, dfarr):
        aStr = ''
        for i in range(len(dfarr)):
            b = dfarr[i]
            for j in range(min(self.max_len - 1, len(self.testli[i]))):
                ch = self.testli[i][j][0]
                if b[j][WordSegmenter.tag2idx['1']] == 1.0:
                    aStr += ' '
                aStr += ch
            aStr += '\n'
        return aStr

    def segmentproper(self, aList):
        sentences = aList[:]
        maxlen = max([len(s) for s in sentences])
        while maxlen > self.max_len:
            sentences = WordSegmenter.halveLines(sentences, self.max_len)
            maxlen = len(sentences)
            
        X = list()
        for s in sentences:
            anX = list()
            for w in s[:self.max_len]:
                val = self.word2idx.get(w[0])
                if val is None:
                    val = len(self.word2idx) - 1 # assimilate alien characters to a rare character
                anX.append(val)
            X.append(anX)
        X = pad_sequences(maxlen=self.max_len, sequences=X, padding="post",
                value=self.word2idx['充'])
        arr = self._model.predict(X,verbose=0)
        return self.reconstruct(arr)

    @property
    def segmentedOutput(self):
        return self.passageSegmented
