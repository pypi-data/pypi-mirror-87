# -*- coding: utf-8 -*-
#!/usr/bin/env python

import re
from kolibri.settings import resources_path
from kolibri.stopwords import get_stop_words
stopwords=get_stop_words('en')

import os

PACKAGE = 'corpora'
DATA_DIR = resources_path
GAZ_DIR = os.path.join(DATA_DIR, PACKAGE)

filename_job_functions = os.path.join(GAZ_DIR, 'gazetteers/Job_Functions.txt')
filename_disclaimer = os.path.join(GAZ_DIR, 'gazetteers/disclaimers.txt')

functions=open(filename_job_functions).readlines()
disclaimers=open(filename_disclaimer).readlines()
function_re = ''
for funct in functions:
    function_re += funct.strip('\n') + '|'

function_re = function_re[:-1]

function_re = '(?P<signature>(([A-Z][a-z]+\s?)+)?(\s?[\|,]\s?)?({})(.+)?)'.format(function_re)

class EmailMessage(object):
    """
    An email message represents a parsed email body.
    """

    def __init__(self, language='en', split_pattern=None):
        self.fragments = []
        self.fragment = None
        self.found_visible = False
        self.language=language
        self.salutations=[s.strip() for s in open(os.path.join(GAZ_DIR, 'gazetteers', self.language, 'salutations.txt')).readlines() if s.strip()!=""]
        self.split_pattern=split_pattern
        self.closings=[c.strip() for c in open(os.path.join(GAZ_DIR, 'gazetteers', self.language, 'email_closing.txt')).readlines()  if c.strip()!=""]

    def read(self, text):
        """ Creates new fragment for each line
            and labels as a signature, quote, or hidden.
            Returns EmailMessage instance
        """
        self.fragments=[]
        self.text = text.replace('\r\n', '\n')
        regex = r"(From|To)\s*:[A-Za-z\s\/@\.:,;\&\?\\\(\)'\"\*[\]<>#\/\+-]+?(Subj(ect)?)\s?:|From\s*:[\w @\.:,;\&\(\)'\"\*[\]<>#\/\+-]+?(Sent|Date)\s?:(\s*\d+(\s|\/)(\w+|\d+)(\s|\/)\d+(\s|\/)?(\d+:\d+)?)?|From\s*:[\w @\.:,;\&\(\)'\"\*[\]<>#\/\+-]+?(Sent\s+at)\s?:(\s*\d+\s\w+\s\d+\s?\d+:\d+)?|From\s*:[\w @\.:,;\&\?\\\(\)'\"\*[\]<>#\/\+-]+?(CC)\s?:|From\s*:[\w @\.:,;\&\?\\\(\)'\"\*[\]<>#\/\+-]+?(To)\s?:"
        if self.split_pattern:
            regex=r""+self.split_pattern
        starts = [m.start(0) for m in re.finditer(regex, self.text, re.MULTILINE | re.UNICODE)]

        if len(starts) < 1:
            self.fragments.append(Fragment(self.text, self.salutations, self.closings))

        else:
            if starts[0] > 0:
                starts.insert(0, 0)
            lines = [self.text[i:j] for i, j in zip(starts, starts[1:] + [None])]

            for line in lines:
                if self.split_pattern:
                    line=re.sub(self.split_pattern, '', line)
                if line.strip()!='':
                    self.fragments.append(Fragment(line, self.salutations, self.closings))

        return self


class Fragment(object):
    """ A Fragment is a part of
        an Email Message, labeling each part.
    """

    def __init__(self, email_text, salutations, closings):
        self.salutations = salutations
        self.closings = closings
        self.body = email_text.strip()
        self.is_forwarded_message = self._get_forwarded()
        self.headers = self._get_header()
        self.attachement = self._get_attachement()
        self.salutation = self._get_salutation()
        self.disclaimer = self._get_disclaimer()
        self.signature = self._get_signature()

        self._content = email_text


    def _get_attachement(self):
        pattern = r'(?P<attachement>(^\s*[a-zA-Z0-9_,\. -]+\.(png|jpeg|docx|doc|xlsx|xls|pdf|pptx|ppt))|Attachments\s?:\s?([a-zA-Z0-9_,\. -]+\.(png|jpeg|docx|doc|xlsx|xls|pdf|pptx|ppt)))'
        groups = re.search(pattern, self.body, re.IGNORECASE)
        attachement = ''
        if not groups is None:
            if "attachement" in groups.groupdict().keys():
                attachement = groups.groupdict()["attachement"]
                self.body=self.body[len(attachement):].strip()
        return attachement

    def _get_salutation(self):
        # Notes on regex:
        # Max of 5 words succeeding first Hi/To etc, otherwise is probably an entire sentence
        salutation_opening_statements = self.salutations

        pattern = r'(?P<salutation>(^(- |\s)*\b(('+r'|'.join(salutation_opening_statements)+r')\b,?\.?\s*)+))'

        groups = re.match(pattern, self.body, re.IGNORECASE)
        salutation = ''
        if groups is not None:
            if "salutation" in groups.groupdict().keys():
                salutation = groups.groupdict()["salutation"]
                self.body = self.body[len(salutation):].strip()
        return salutation

    def _get_header(self):
        regex = r"From\s*:[\w @\.:,;\&\?\\\(\)'\"\*[\]<>#\/\+-]+?(Subj(ect)?)\s?:|From\s*:[\w @\.:,;\&\(\)'\"\*[\]<>#\/\+-]+?(Sent|Date)\s?:(\s*\d+(\s|\/)(\w+|\d+)(\s|\/)\d+(\s|\/)?(\d+:\d+)?)?|From\s*:[\w @\.:,;\&\(\)'\"\*[\]<>#\/\+-]+?(Sent\s+at)\s?:(\s*\d+\s\w+\s\d+\s?\d+:\d+)?|From\s*:[\w @\.:,;\&\?\\\(\)'\"\*[\]<>#\/\+-]+?(CC)\s?:|From\s*:[\w @\.:,;\&\?\\\(\)'\"\*[\]<>#\/\+-]+?(To)\s?:"

        pattern = r"(?P<header_text>("+regex+"))"

        groups = re.search(pattern, self.body, + re.DOTALL)
        header_text = None
        if groups is not None:
            if "header_text" in groups.groupdict().keys():
                header_text = groups.groupdict()["header_text"]
                self.body=self.body[len(header_text):].strip()
        return header_text

    def _get_disclaimer(self):
        disclaimer_openings = disclaimers

        pattern = r"\s*(?P<disclaimer_text>(" + "|".join(disclaimer_openings)+ ")(\s*\w*))"

        groups = re.search(pattern, self.body, re.MULTILINE)
        disclaimer_text = None
        if groups is not None:
            if "disclaimer_text" in groups.groupdict().keys():
                found = groups.groupdict()["disclaimer_text"]
                disclaimer_text = self.body[self.body.find(found):]
                self.body = self.body[:self.body.find(disclaimer_text)].strip()

        return disclaimer_text

    def _get_signature(self):
        # note - these openinged statements *must* be in lower case for
        # sig within sig searching to work later in this func

        # TODO DRY
        self.signature=''
        sig_opening_statements_small = self.closings
        sig_opening_statements = self.closings

        pattern = r'(?P<signature>(?<!^)\b(' + '|'.join(sig_opening_statements ) + r')\b(.)*)'
        pattern2 = r'(?P<signature>(?<!^)\b(' + '|'.join(sig_opening_statements_small ) + r')\b(.)*)'

        groups = re.search(pattern, self.body, re.IGNORECASE + re.DOTALL)
        signature = None
        if groups:
            if "signature" in groups.groupdict().keys():
                signature1 = groups.groupdict()["signature"]
                # search for a sig within current sig to lessen chance of accidentally stealing words from body
                tmp_sig = signature1
                for s in sig_opening_statements_small:
                    if tmp_sig.lower().find(s) == 0:
                        tmp_sig = tmp_sig[len(s):]
                groups = re.search(pattern2, tmp_sig, re.IGNORECASE + re.DOTALL)
                remaing=""
                signature2=""
                if groups:
                    signature2 = groups.groupdict()["signature"]
                    remaing=tmp_sig[:tmp_sig.find(signature2)].lower().replace(',','').replace('-', '')
                    for statement in sig_opening_statements:
                        remaing=remaing.replace(statement.lower(), '')
                    for stp in stopwords:
                        remaing=re.sub(r'\b'+stp+r'\b', '', remaing)
                if len(remaing.strip().split())>1:
                    signature=signature2
                else:
                    signature=signature1
                self.body = self.body[:self.body.find(signature)].strip()
        else:
            groups = re.search(function_re, self.body, re.DOTALL)

            if groups is not None and "signature" in groups.groupdict().keys():
                signature = groups.groupdict()["signature"]
                # search for a sig within current sig to lessen chance of accidentally stealing words from body
                tmp_sig = signature
                for s in sig_opening_statements_small:
                    if tmp_sig.lower().find(s) == 0:
                        tmp_sig = tmp_sig[len(s):]
                groups = re.search(pattern2, tmp_sig, re.IGNORECASE + re.DOTALL)
                if groups:
                    signature = groups.groupdict()["signature"]
                self.body = self.body[:self.body.find(signature)].strip()
                if len(self.body.strip())==0:
                    self.body=self.signature
                    self.signature=''
        return signature

    def _get_forwarded(self):

        pattern = '(?P<forward_text>([- ]* Forwarded Message [- ]*|[- ]* Forwarded By [- ]*|[- ]*Original Message[- ]*))'
        groups = re.search(pattern, self.body, re.DOTALL)
        forward = None
        if groups is not None:
            if "forward_text" in groups.groupdict().keys():
                forward = groups.groupdict()["forward_text"]

        if forward is not None:
            self.body = self.body.replace(forward, '')

        return forward is not None

    @property
    def content(self):
        return self._content.strip()
