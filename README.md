## RDRPOSTagger ##

![enrdr3](https://user-images.githubusercontent.com/2412555/48744741-94d82480-ecbc-11e8-89dc-200ea85c96e4.png)

**RDRPOSTagger** is a robust and easy-to-use toolkit for POS and morphological tagging. It employs an error-driven approach to automatically construct tagging rules in the form of a binary tree.

- RDRPOSTagger obtains very fast tagging speed and achieves a competitive accuracy in comparison to the state-of-the-art results. See experimental results including performance speed and tagging accuracy for 13 languages in our *AI Communications* article.

- RDRPOSTagger now supports pre-trained UPOS, XPOS and morphological tagging models for about 80 languages. See folder `Models` for more details.

- See [USAGE.md](USAGE.md) for full details on how to train and use the tagger.

The general architecture and experimental results of RDRPOSTagger can be found in our following papers:

- Dat Quoc Nguyen, Dai Quoc Nguyen, Dang Duc Pham and Son Bao Pham. [RDRPOSTagger: A Ripple Down Rules-based Part-Of-Speech Tagger](http://www.aclweb.org/anthology/E14-2005). In *Proceedings of the Demonstrations at the 14th Conference of the European Chapter of the Association for Computational Linguistics*, EACL 2014, pp. 17-20, 2014. [[.PDF]](http://www.aclweb.org/anthology/E14-2005) [[.bib]](http://www.aclweb.org/anthology/E14-2005.bib)

- Dat Quoc Nguyen, Dai Quoc Nguyen, Dang Duc Pham and Son Bao Pham. [A Robust Transformation-Based Learning Approach Using Ripple Down Rules for Part-Of-Speech Tagging](http://content.iospress.com/articles/ai-communications/aic698). *AI Communications* (AICom), vol. 29, no. 3, pp. 409-422, 2016. [[.PDF]](http://arxiv.org/pdf/1412.4021.pdf) [[.bib]](http://rdrpostagger.sourceforge.net/AICom.bib)

**Please CITE** either the EACL or the AICom paper whenever RDRPOSTagger is used to produce published results or incorporated into other software.

**Current release (41MB .zip file containing about 330 pre-trained tagging models) is available to download at:** [https://github.com/datquocnguyen/RDRPOSTagger/archive/master.zip](https://github.com/datquocnguyen/RDRPOSTagger/archive/master.zip)

**Find more information about RDRPOSTagger at:** [http://rdrpostagger.sourceforge.net/](http://rdrpostagger.sourceforge.net/)

In addition, you might want to try my neural network-based toolkit [jPTDP](https://github.com/datquocnguyen/jPTDP) for joint POS tagging and dependency parsing.