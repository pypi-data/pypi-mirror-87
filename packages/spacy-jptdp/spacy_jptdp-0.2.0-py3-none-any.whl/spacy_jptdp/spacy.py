#! /usr/bin/python3 -i
# coding=utf-8

import os,time,pickle,numpy
from spacy.symbols import POS,DEP,HEAD
from spacy.tokens import Doc
from spacy.language import Language

PACKAGE_DIR=os.path.abspath(os.path.dirname(__file__))
DOWNLOAD_DIR=os.path.join(PACKAGE_DIR,"models")
MODEL_URL="https://raw.githubusercontent.com/KoichiYasuoka/spaCy-jPTDP/master/treebanks/"
SPACY_V3=hasattr(Language,"component")
tm=time.time()

class jptdpParser(object):
  name="jPTDP"
  def __init__(self,treebank,vocab):
    self.jptdp=load_jptdp(treebank)
    self.vocab=vocab
  def __call__(self,doc):
    import tempfile
    vs=self.vocab.strings
    r=vs.add("ROOT")
    pos=[]
    heads=[]
    deps=[]
    with tempfile.NamedTemporaryFile("w",encoding="utf-8") as f:
      for s in doc.sents:
        print("".join(["\t".join([str(i+1),str(t)]+["_"]*7+["_" if t.whitespace_ else "SpaceAfter=No"])+"\n" for i,t in enumerate(s)])+"\n",file=f,flush=True)
      for s in self.jptdp.Predict(f.name):
        for t in s:
          if t.id>0:
            pos.append(vs.add(t.pred_pos))
            deprel=t.pred_relation
            head=t.pred_parent_id
            if deprel=="root" or deprel=="ROOT" or head==0:
              heads.append(0)
              deps.append(r)
            else:
              heads.append(head-t.id)
              deps.append(vs.add(deprel))
    a=numpy.array(list(zip(pos,deps,heads)),dtype="uint64")
    doc.from_array([POS,DEP,HEAD],a)
    if SPACY_V3:
      return doc
    doc.is_tagged=True
    doc.is_parsed=True
    return doc

def progress(block_count,block_size,total_size):
  t=time.time()
  p=100.0*block_count*block_size/total_size
  if p<1:
    t=-1
  elif p>=100:
    p=100
    t-=tm
  else:
    t=(t-tm)*(100-p)/p
  b=int(p/2)
  if b==50:
    s="="*50
  else:
    s=("="*b)+">"+(" "*(49-b))
  if t<0:
    u="   "
  elif t<3600:
    u=time.strftime("%M:%S   ",time.gmtime(t))
  elif t<86400:
    u=time.strftime("%H:%M:%S   ",time.gmtime(t))
  else:
    u=time.strftime("%d+%H:%M:%S   ",time.gmtime(t))
  print("\r ["+s+"] "+str(int(p))+"% "+u,end="")

def download_jptdp(treebank):
  import urllib.request,tarfile
  global tm
  tm=time.time()
  os.makedirs(DOWNLOAD_DIR,exist_ok=True)
  f,h=urllib.request.urlretrieve(MODEL_URL+treebank+".tar.gz",reporthook=progress)
  with tarfile.open(f) as z:
    z.extractall(DOWNLOAD_DIR)
  print("")

def load_jptdp(treebank):
  d=os.path.join(DOWNLOAD_DIR,treebank)
  if not os.path.isdir(d):
    download_jptdp(treebank)
  import pickle
  fn=os.path.join(d,"model.params")
  with open(fn,"rb") as f:
    words,w2i,c2i,pos,rels,stored_opt=pickle.load(f,encoding="bytes")
  with open(fn,"rb") as f:
    words,w2i,_,pos,rels,stored_opt=pickle.load(f,encoding="utf-8",errors="ignore")
  from spacy_jptdp.learner import jPosDepLearner
  parser=jPosDepLearner(words,pos,rels,w2i,c2i,stored_opt)
  parser.Load(fn.replace(".params",""))
  return parser

def load_spacy(treebank):
  i=treebank.find("_")
  j=treebank if i<1 else treebank[0:i]
  try:
    exec("import spacy.lang."+j+" as p")
    exec("q=p."+locals()["p"].__all__[0])
    return locals()["q"]()
  except:
    from spacy.lang.xx import MultiLanguage
    return MultiLanguage()

def load(treebank):
  nlp=load_spacy(treebank)
  if SPACY_V3:
    nlp.add_pipe("sentencizer")
    Language.component("jPTDP",func=jptdpParser(treebank,nlp.vocab))
    nlp.add_pipe("jPTDP")
  else:
    nlp.add_pipe(nlp.create_pipe("sentencizer"))
    nlp.add_pipe(jptdpParser(treebank,nlp.vocab))
  nlp.meta["lang"]=treebank+"_jPTDP"
  return nlp

