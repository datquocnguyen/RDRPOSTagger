# RDRPOSTagger

[![Python 3.4](https://img.shields.io/badge/python-3.4-blue.svg)](https://www.python.org/downloads/release/python-360/) 
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) 

A Rule-based Part-of-Speech and Morphological Tagging Toolkit<br>
https://github.com/datquocnguyen/RDRPOSTagger

1. [Introduction](#1-introduction)
2. [Train RDRPOSTagger on a gold standard training corpus](#2-train-rdrpostagger-on-a-gold-standard-training-corpus)
3. [Use pre-trained POS and morphological tagging models](#3-use-pre-trained-pos-and-morphological-tagging-models)
4. [Combine RDRPOSTagger with an external initial tagger](#4-combine-rdrpostagger-with-an-external-initial-tagger)
5. [Speed up tagging process with an implementation in Java](#speed-up-tagging-process-with-an-implementation-in-java)
- [References](#references)

## News

- 22/06/2019: Ported to Python 3.4+ & Released 300+ pre-trained UPOS, XPOS and morphological tagging models for about 80 languages from [UD v2.4](http://universaldependencies.org/).

- 24/05/2017: Released version [1.2.4](https://github.com/datquocnguyen/RDRPOSTagger/tree/python2.7) with pre-trained Universal POS tagging models for 40+ languages from UD v2.0. This is the last version with Python 2.7 support.


## 1. Introduction

RDRPOSTagger is a robust and easy-to-use toolkit for POS and morphological tagging. It employs an error-driven methodology to automatically construct tagging rules in the form of a binary tree.

- RDRPOSTagger obtains fast training & tagging speed. For example, on the English Penn WSJ sections 22-24, it achieves tagging speeds of **8K** and **90K words/second** computed for <u>single</u> threaded implementations in **Python** and **Java**, respectively (a computer with Core2Duo 2.4GHz and 3GB of memory). See more results in our *AI Communications* article.

- RDRPOSTagger obtains a competitive performance in comparison to the state-of-the-art results. It now supports pre-trained UPOS, XPOS and morphological tagging models for about 80 languages. See HERE for details.

The general architecture and experimental results of RDRPOSTagger can be found in our following papers:

- Dat Quoc Nguyen, Dai Quoc Nguyen, Dang Duc Pham and Son Bao Pham. [RDRPOSTagger: A Ripple Down Rules-based Part-Of-Speech Tagger](http://www.aclweb.org/anthology/E14-2005). In *Proceedings of the Demonstrations at the 14th Conference of the European Chapter of the Association for Computational Linguistics* (EACL), pp. 17-20, 2014. [[.PDF](http://www.aclweb.org/anthology/E14-2005)] [[].bib](http://rdrpostagger.sourceforge.net/13eacl2014.bib)]

- Dat Quoc Nguyen, Dai Quoc Nguyen, Dang Duc Pham and Son Bao Pham. [A Robust Transformation-Based Learning Approach Using Ripple Down Rules for Part-Of-Speech Tagging](http://content.iospress.com/articles/ai-communications/aic698). *AI Communications* (AICom), vol. 29, no. 3, pp. 409-422, 2016. [[.PDF](http://arxiv.org/pdf/1412.4021.pdf)] [[.bib](http://rdrpostagger.sourceforge.net/AICom.bib)]

<u>**Please CITE**</u> either the EACL or the AICom paper whenever RDRPOSTagger is used to produce published results or incorporated into other software.


## 2. Train RDRPOSTagger on a gold standard training corpus

<u>NOTICES:</u>

- In terms of implementation, the training process has been implemented in Python while the tagging process has been implemented in both Python and Java. There is a multi-threaded mode with faster tagging speed for the Python implementation. See Section 5 for details of using the Java implementation.

- RDRPOSTagger requires an initial tagger. The internal initial tagger developed within RDRPOSTagger uses a lexicon to assign a tag for each word. See Section 4 for combining RDRPOSTagger with an external initial tagger.

- RDRPOSTagger assumes that each line in the gold standard training corpus is a sequence of WORD/TAG pairs separated by whitespace characters. See sample training and test sets in folder data.

Assume that Python 3.4+ is already set to run in command line or terminal (e.g. adding Python to the environment variable ‘path’ in Windows OS).

- We train RDRPOSTagger on the gold standard training corpus by executing:

  ```sh
  pSCRDRtagger$ python RDRPOSTagger.py train PATH-TO-GOLD-STANDARD-TRAINING-CORPUS
  ```

  <u>Example 1</u>:
  ```sh
  pSCRDRtagger$ python RDRPOSTagger.py train ../data/goldTrain
  ```

  Note that the actual command starts from `python`. Here `pSCRDRtagger$` is simply used to denote the current source package `pSCRDRtagger`.

  A lexicon `.DICT` file and a model `.RDR` file, for example `goldTrain.DICT` and `goldTrain.RDR`, will be generated in the same directory containing the gold standard training corpus.

- To employ the trained model for POS tagging on a raw unlabeled text corpus, we perform:

  ```sh
  pSCRDRtagger$ python RDRPOSTagger.py tag PATH-TO-TRAINED-RDR-MODEL PATH-TO-LEXICON PATH-TO-RAW-TEXT-CORPUS
  ```

  <u>Example 2</u>:
  ```sh
  pSCRDRtagger$ python RDRPOSTagger.py tag ../data/goldTrain.RDR ../data/goldTrain.DICT ../data/rawTest
  ```

  A `.TAGGED file`, in this case `rawTest.TAGGED`, will be generated in the same directory containing the raw text corpus.

  <u>To obtain faster tagging process in Python</u>: set a higher value for variable `NUMBER_OF_PROCESSES` in module `Config.py` in package `Utility`.

- To evaluate tagging accuracy, we employ module `Eval.py` in package `Utility`:

  ```sh
  Utility$ python Eval.py PATH-TO-TAGGED-TEST-CORPUS PATH-TO-GOLD-TEST-CORPUS
  ```

  <u>Example 3</u>:
  ```sh
  Utility$ python Eval.py ../data/rawTest.TAGGED ../data/goldTest
  ```

- **NOTE:** Use `RDRPOSTagger4En.py` and `RDRPOSTagger4Vn.py` in case of retraining tagging models for English with Penn Treebank POS tags and for Vietnamese with VietTreebank (or VLSP) POS tags, respectively.


## 3. Use pre-trained POS and morphological tagging models

- Pre-trained POS and morphological tagging models from our AI Communications paper:


  Language | Corpus | Model | Lexicon
  ---------|--------|-------|--------
  English | Penn WSJ section 00-18 [M93] | `../Models/POS/English.RDR` | `../Models/POS/English.DICT`
  French | French Treebank [A03] | `../Models/POS/French.RDR` | `../Models/POS/French.DICT`
  German | TIGER Corpus [B04] | `../Models/POS/German.RDR` | `../Models/POS/German.DICT`
  Hindi | Hindi Treebank [P09] | `../Models/POS/Hindi.RDR` | `../Models/POS/Hindi.DICT`
  Italian | ISDT Treebank [B13] | `../Models/POS/Italian.RDR` | `../Models/POS/Italian.DICT`
  Thai | ORCHID Corpus [S97] | `../Models/POS/Thai.RDR` | `../Models/POS/Thai.DICT`
  Vietnamese | VLSP 2013 POS-annotated corpus [N09] | `../Models/POS/Vietnamese.RDR` | `../Models/POS/Vietnamese.DICT`

  Language | Corpus | Model | Lexicon
  ---------|--------|-------|--------
  Bulgarian | BulTreeBank-Morph [S04] | `../Models/MORPH/Bulgarian.RDR` | `../Models/MORPH/Bulgarian.DICT`
  Czech | Prague Dependency Treebank 2.5 [B12] | `../Models/MORPH/Czech.RDR` | `../Models/MORPH/Czech.DICT`
  Dutch | Lassy Small Corpus [N13] | `../Models/MORPH/Dutch.RDR` | `../Models/MORPH/Dutch.DICT`
  French | French Treebank [A03] | `../Models/MORPH/French.RDR` | `../Models/MORPH/French.DICT`
  German | TIGER Corpus [B04] | `../Models/MORPH/German.RDR` | `../Models/MORPH/German.DICT`
  Portuguese | Tycho Brahe Corpus [G10] | `../Models/MORPH/Portuguese.RDR` | `../Models/MORPH/Portuguese.DICT`
  Spanish | IULA LSP Treebank [M12] | `../Models/MORPH/Spanish.RDR` | `../Models/MORPH/Spanish.DICT`
  Swedish | Stockholm—Ume°a Corpus 3.0 [S12] | `../Models/MORPH/Swedish.RDR` | `../Models/MORPH/Swedish.DICT`

- 300+ UPOS, XPOS and FEATS (i.e. morphological) tagging models for about 80 languages available in folder [ud-treebanks-v2.4](https://github.com/datquocnguyen/RDRPOSTagger/tree/master/Models).

- To use a pre-trained model, we perform:

  ```sh
  pSCRDRtagger$ python RDRPOSTagger.py tag PATH-TO-PRETRAINED-RDR-MODEL PATH-TO-LEXICON PATH-TO-RAW-TEXT-CORPUS
  ```

  <u>Example 4</u>:
  ```sh
  pSCRDRtagger$ python RDRPOSTagger.py tag ../Models/POS/German.RDR ../Models/POS/German.DICT ../data/GermanRawTest
  ```

  <u>Example 5</u>:
  ```sh
  pSCRDRtagger$ python RDRPOSTagger.py tag ../Models/MORPH/German.RDR ../Models/MORPH/German.DICT ../data/GermanRawTest
  ```

  NOTE that each line in the input raw text corpus represents a word-segmented sentence. For programming with RDRPOSTagger, please follow code lines 92-98 in module `RDRPOSTagger.py` in package `pSCRDRTagger`. Here is an example:

  ```python
  r = RDRPOSTagger()

  # Load the POS tagging model for French

  r.constructSCRDRtreeFromRDRfile("../Models/POS/French.RDR")

  # Load the lexicon for French

  DICT = readDictionary("../Models/POS/French.DICT")

  # Tag a tokenized/word-segmented sentence

  r.tagRawSentence(DICT, "Cette annonce a fait l' effet d' une véritable bombe .")```

- NOTE: Use `RDRPOSTagger4En.py` and `RDRPOSTagger4Vn.py` for running pre-trained English and Vietnamese POS tagging models in folder `../Models/POS`, respectively.


## 4. Combine RDRPOSTagger with an external initial tagger

- In case of using output from an external initial tagger, to train RDRPOSTagger we perform:

  ```sh
  pSCRDRtagger$ python ExtRDRPOSTagger.py train PATH-TO-GOLD-STANDARD-TRAINING-CORPUS PATH-TO-TRAINING-CORPUS-INITIALIZED-BY-EXTERNAL-TAGGER
  ```

  <u>Example 6</u>:
  ```sh
  pSCRDRtagger$ python ExtRDRPOSTagger.py train ../data/goldTrain ../data/initTrain
  ```

  Here the initialized training corpus `initTrain` is generated by using the external initial tagger to perform tagging on the raw corpus which consists of the raw text extracted from the gold standard training corpus `goldTrain`.

  A model `.RDR` file, for example `initTrain.RDR`, will be generated in the same directory containing the initialized training corpus.

- To use the trained model for retagging a test corpus where words already are initially tagged by the external initial tagger:

  ```sh
  pSCRDRtagger$ python ExtRDRPOSTagger.py tag PATH-TO-TRAINED-RDR-MODEL PATH-TO-TEST-CORPUS-INITIALIZED-BY-EXTERNAL-TAGGER
  ```

  <u>Example 7</u>:
  ```sh
  pSCRDRtagger$ python ExtRDRPOSTagger.py tag ../data/initTrain.RDR ../data/initTest
  ```

## 5. Speed up tagging process with an implementation in Java

- Compile: jSCRDRTagger$ javac -encoding UTF-8 RDRPOSTagger.java

- To use a pre-trained model for tagging a raw text corpus:

  ```sh
  jSCRDRTagger$ java RDRPOSTagger PATH-TO-PRETRAINED-RDR-MODEL PATH-TO-LEXICON PATH-TO-RAW-TEXT-CORPUS
  ```

  <u>Example 8</u>:
  ```sh
  jSCRDRTagger$ java RDRPOSTagger ../Models/POS/German.RDR ../Models/POS/German.DICT ../data/GermanRawTest
  ```

   <u>Example 9</u>:
   ```sh
   jSCRDRTagger$ java RDRPOSTagger ../Models/MORPH/German.RDR ../Models/MORPH/German.DICT ../data/GermanRawTest
   ```

  RDRPOSTagger has two additional parameters specialized for POS tagging in English and Vietnamese:

  <u>Example 10</u>:
  ```sh
  jSCRDRTagger$ java RDRPOSTagger en ../Models/POS/English.RDR ../Models/POS/English.DICT ../data/en/rawTest
  ```

  <u>Example 11</u>:
  ```sh
  jSCRDRTagger$ java RDRPOSTagger vn ../Models/POS/Vietnamese.RDR ../Models/POS/Vietnamese.DICT ../data/vn/rawTest
  ```

- In case of using an external initial tagger:

  ```sh
  jSCRDRTagger$ java RDRPOSTagger ex PATH-TO-TRAINED-RDR-MODEL PATH-TO-TEST-CORPUS-INITIALIZED-BY-EXTERNAL-TAGGER
  ```

  <u>Example 12</u>:
  ```sh
  jSCRDRTagger$ java RDRPOSTagger ex ../data/initTrain.RDR ../data/initTest
  ```


## References

[M93] M. P. Marcus, M. A. Marcinkiewicz, and B. Santorini. Building a Large Annotated Corpus of English: The Penn Treebank. *Computational Linguistics*, 19(2):313– 330, 1993. http://www.cis.upenn.edu/~treebank/

[A03] A. Abeillé, L. Clément, and F. Toussenel. Building a Treebank for French. In *Treebanks*, volume 20 of Text, Speech and Language Technology, pages 165– 187. 2003. http://www.llf.cnrs.fr/en/Gens/Abeille/French-Treebank-fr.php

[B04] S. Brants, S. Dipper, P. Eisenberg, S. Hansen-Schirra, E. K¨onig, W. Lezius, C. Rohrer, G. Smith, and H. Uszkoreit. TIGER: Linguistic Interpretation of a German Corpus. *Research on Language and Computation*, 2(4):597–620, 2004. http://www.ims.uni-stuttgart.de/forschung/ressourcen/korpora/tiger.en.html

[P09] M. Palmer, R. Bhatt, B. Narasimhan, O. Rambow, D. M. Sharma, and F. Xia. Hindi Syntax: Annotating Dependency, Lexical Predicate-Argument Structure, and Phrase Structure. In *Proceedings of 7th International Conference on Natural Language Processing*, pages 261–268, 2009. http://verbs.colorado.edu/hindiurdu/index.html

[B13] C. Bosco, S. Montemagni, and M. Simi. Converting Italian Treebanks: Towards an Italian Stanford Dependency Treebank. In *Proceedings of the 7th Linguistic Annotation Workshop and Interoperability with Discourse*, pages 61–69, 2013. http://medialab.di.unipi.it/wiki/ISDT

[S97] V. Sornlertlamvanich, T. Charoenporn, and H. Isahara. ORCHID: Thai Part-Of-Speech Tagged Corpus, 1997. URL http://culturelab.in.th/files/orchid.html

[N09] P. T. Nguyen, X. L. Vu, T. M. H. Nguyen, V. H. Nguyen, and H. P. Le. Building a Large Syntactically-Annotated Corpus of Vietnamese. In *Proceedings of the Third Linguistic Annotation Workshop*, pages 182–185, 2009. http://vlsp.vietlp.org:8080/

[S04] K. Simov, P. Osenova, A. Simov, and M. Kouylekov. Design and Implementation of the Bulgarian HPSGbased Treebank. *Research on Language and Computation*, 2:495–522, 2004. http://www.bultreebank.org

[B12] E. Bejcek, J. Panevová, J. Popelka, P. Stranák, M. Sevcíková, J. Stepánek, and Z. Zabokrtský. Prague Dependency Treebank 2.5 - a Revisited Version of PDT 2.0. In *Proceedings of 24th International Conference on Computational Linguistics*, pages 231–246, 2012. https://ufal.mff.cuni.cz/pdt2.5/

[N13] G. Noord, G. Bouma, F. Eynde, D. Kok, J. Linde, I. Schuurman, E. Sang, and V. Vandeghinste. Large Scale Syntactic Annotation of Written Dutch: Lassy. In *Essential Speech and Language Technology for Dutch, Theory and Applications of Natural Language Processing*, pages 147–164, 2013. http://www.let.rug.nl/~vannoord/Lassy/

[G10] C. Galves and P. Faria. Tycho Brahe Parsed Corpus of Historical Portuguese, 2010. http://www.tycho.iel.unicamp.br/~tycho/corpus/en/index.html.

[M12] M. Marimon, B. Fisas, N. Bel, M. Villegas, J. Vivaldi, S. Torner, M. Lorente, and S. Vázquez. The IULA Treebank. In *Proceedings of the eighth international conference on Language Resources and Evaluation*, pages 1920–1926, 2012. https://www.iula.upf.edu/recurs01_tbk_uk.htm

[S12] SUC-3.0. The Stockholm—Ume°a Corpus (SUC) 3.0, 2012. URL http://spraakbanken.gu.se/eng/resource/suc3


----
Last updated: June 22, 2019
