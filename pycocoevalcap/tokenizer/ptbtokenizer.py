#!/usr/bin/env python
# 
# File Name : ptbtokenizer.py
#
# Description : Do the PTB Tokenization and remove punctuations.
#
# Creation Date : 29-12-2014
# Last Modified : Thu Mar 19 09:53:35 2015
# Authors : Hao Fang <hfang@uw.edu> and Tsung-Yi Lin <tl483@cornell.edu>

import os
import sys
import subprocess
import tempfile
import itertools

# path to the stanford corenlp jar
#STANFORD_CORENLP_3_4_1_JAR = '/home/bibabo_walmart/workspace/coco-caption/pycocoevalcap/spice/lib/stanford-corenlp-3.6.0.jar'
STANFORD_CORENLP_3_4_1_JAR = 'stanford-corenlp-3.6.0.jar'
# punctuations to be removed from the sentences
PUNCTUATIONS = ["''", "'", "``", "`", "-LRB-", "-RRB-", "-LCB-", "-RCB-", \
        ".", "?", "!", ",", ":", "-", "--", "...", ";"] 

class PTBTokenizer:
    """Python wrapper of Stanford PTBTokenizer"""

    def tokenize(self, captions_for_image):
        cmd = ['java', '-cp', STANFORD_CORENLP_3_4_1_JAR, \
                'edu.stanford.nlp.process.PTBTokenizer', \
                '-preserveLines', '-lowerCase']
        print cmd
        # ======================================================
        # prepare data for PTB Tokenizer
        # ======================================================
        final_tokenized_captions_for_image = {}
        image_id = [k for k, v in captions_for_image.items() for _ in range(len(v))]
        sentences = '\n'.join([c['caption'].replace('\n', ' ') for k, v in captions_for_image.items() for c in v])

        # ======================================================
        # save sentences to temporary file
        # ======================================================
        #path_to_jar_dirname=os.path.dirname(os.path.abspath(__file__))
        path_to_jar_dirname="/home/bibabo_walmart/workspace/coco-caption/pycocoevalcap/spice/lib"
        tmp_file = tempfile.NamedTemporaryFile(delete=False, dir=path_to_jar_dirname)
        tmp_file.write(sentences)
        tmp_file.close()

        # ======================================================
        # tokenize sentence
        # ======================================================
        print cmd
        print path_to_jar_dirname
        print tmp_file.name

        cmd.append(os.path.basename(tmp_file.name))
        print "token 0"
        p_tokenizer = None
        try: 
            p_tokenizer = subprocess.Popen(cmd, cwd=path_to_jar_dirname, \
                stdout=subprocess.PIPE)
        except:
            print "Unexpected error:", sys.exc_info()[0]

        #p_tokenizer = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        print "token 1"
        token_lines = p_tokenizer.communicate(input=sentences.rstrip())[0]
        print "token 2"
        lines = token_lines.split('\n')
        # remove temp file
        os.remove(tmp_file.name)
        print "token 3"

        # ======================================================
        # create dictionary for tokenized captions
        # ======================================================
        for k, line in zip(image_id, lines):
            if not k in final_tokenized_captions_for_image:
                final_tokenized_captions_for_image[k] = []
            tokenized_caption = ' '.join([w for w in line.rstrip().split(' ') \
                    if w not in PUNCTUATIONS])
            final_tokenized_captions_for_image[k].append(tokenized_caption)

        return final_tokenized_captions_for_image
