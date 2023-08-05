from email.message import EmailMessage
import mimetypes
from email.utils import getaddresses
from email.utils import make_msgid
import chardet


class MiniMail():
    '''
    MiniMail is class to create a mail body.
    
    MiniMail is an inherit class from email.message.EmailMessage,
    which can be sent by smtplib of python, or the class MiniPostMan afterward.
    chardet is the only extend module, which is to recognize the encoding of file.
    '''    
    
    def __init__(self, from_ = '', to = '', subject ='', gid = 'aipython', prefix = 'mmail'):
        '''
        To initialize instance.
        
        from, to, subject :   refer to RFC822, https://tools.ietf.org/html/rfc822.html#section-4.5, which are mini requirement for email
        gid : as part identification for content-id in email
        mmail : used in html template, as format id.
        '''
        self._mail = EmailMessage()
        self._from = from_
        self._to = to
        self._subject = subject
        self._gid = gid
        self._prefix = prefix + '_'
        self._encode_confidence = 0.5
        self._embedded = ['audio', 'video', 'image']
    
    def add_text(self, content, encoding = 'utf-8'):
        '''
        Add plain text content in email.
        
        content : string, plain text content
        encoding : string, charset of content
        '''
        self._mail.set_content(content, charset = encoding)
        
        
    def add_html(self, html, cids, body = None):
        '''
        Add html to email or an instance of EmailMessage.
        
        html : string, the html content
        cids : list or dict, resrouces for html, which made by make_cid_list() or make_cid_dict(), in which are objects with the keys of 
                attachment, maintype, subtype, cid, filename, encoding.
        body : can be EmailMessage, or payload of email
        '''
        if body == None :
            body = self._mail
        body.add_alternative(html, subtype = 'html') #add_alternative is method of EmailMessage
        payload = body.get_payload() #legcy method of EmailMessage, to obtain content of email
        cid_list = self.sorting_cids(cids) if cids else []
        for l in cid_list:
            #different MIME maintye need different parameters
            if l['maintype'] in self._embedded: #audio, video, image are inline cotent of html
                payload[-1].add_related(l['attachment'], l['maintype'], l['subtype'], cid = l['cid'])
            elif l['maintype'] == 'text':  #for plain text content
                payload[-1].add_attachment(l['attachment'], subtype = l['subtype'], \
                                           charset = l['encoding'] if l['encoding'] != None else 'utf-8', \
                                        cid = l['cid'], filename = l['filename'] )
            else:  #for binary content and others which are not standard MIME type
                payload[-1].add_attachment(l['attachment'], maintype = l['maintype'], subtype = l['subtype'], \
                                        filename = l['filename'])

    
    def add_html_auto(self, html, sources = None, body = None):
        '''
        An easy way to call add_html().
        
        html : string, the html template, in which the refer will like mmail_0, mmail is self._prefix, 0 is the index of fmt list,
            e.g. fmt = {'mmail_0' : 'abc', 'mmail_1' : 'def'}, then after html formating, 
            mmail_0 will be replaced by abc, mmail_1 will be replaced by def.
        src_list : list, resoruce path of files which will be refered in html
        body : email.message, can be an instance of EmailMessage, or payload of email
        '''        
        fmt = {}
        cids = None
        if type(sources) == list:
            cids = self.make_cid_list(sources)  #prepare contents data
            for l in range(len(cids)):
                fmt[self._prefix + str(l)] = cids[l]['cid']  #prepare the refer pair in html. e.g. 'mmail_0' : 'abc'
        elif type(sources) == dict:
            cids = self.make_cid_dict(sources)
            for k, l in cids.items():
                fmt[k] = l['cid']
            
        if fmt:
            html = html.format(**fmt)  #format, using dict data
        self.add_html(html, cids, body)        
        
    def get_encoding(self, b):
        '''
        Get the content encoding, using module chardet to detect.
        
        b : byte, the content of file
        '''
        encoding = chardet.detect(b)
        if float(encoding['confidence']) > self._encode_confidence:
            return encoding['encoding']
        else:
            return 'binary'   #if can not be recognized, tagging as binary

    def get_MEMF(self, file):
        '''
        Get mimetype, encoding, opening mode, filename of filepath.
        
        file : string, file path
        '''
        mtype = mimetypes.guess_type(file, strict = False)[0].split('/')
        encoding = self.get_file_encoding(file)
        mode = 'r' + ('b' if encoding == 'binary' else '')
        encoding = encoding if encoding != 'binary' else None
        filename = file.split('/')[-1]
        return mtype, encoding, mode, filename

    def get_file_encoding(self, file):
        '''
        Get encoding of file.
        
        file : string, file path
        '''
        with open(file, 'rb') as f:
            encoding = self.get_encoding(f.read())
        return encoding
    
    def add_attachment(self, files, body = None):
        '''
        Add files as attachment into email or an instance of EmailMessage.
        
        files : list, files to attach
        body : email.message, can be an instance of EmailMessage, or payload of email
        '''
        body = self._mail if body == None else body
        cid_list = self.make_cid_list(files)
        for l in cid_list:
            if l['maintype'] == 'text':  #for plain text content
                    body.add_attachment(l['attachment'], subtype = l['subtype'],\
                                        charset = l['encoding'] if l['encoding'] != None else 'utf-8', \
                                            cid = l['cid'], filename = l['filename'] )
            else:  #for binary content and others which are not standard MIME type
                    body.add_attachment(l['attachment'], maintype = l['maintype'], subtype = l['subtype'], \
                                            filename = l['filename'])

    def add_email(self, mail, body = None):
        '''
        Add mail as attachment into email or an instance of EmailMessage.
        
        mail : email.message or .eml, email to attach
        '''
        body = self._mail if body == None else body
        body.add_attachment(mail)    
    
    def make_cid_list(self, files):
        '''
        Prepare files data for cid.
        
        File data have bytes of file, maintype, subtype, cid, filename, encoding.        
        files : list
        '''
        cid_list = []
        for file in files:
            mtype, encoding, mode, filename = self.get_MEMF(file)
            with open(file, mode, encoding = encoding) as f:
                fdata = f.read()
                cid_list.append({'attachment': fdata, 'maintype' : mtype[0], 'subtype' : mtype[1], \
                             'cid': make_msgid(domain = self._gid)[1:-1], 'filename' : filename, 'encoding' : encoding})
        return cid_list
    
    
    def make_cid_dict(self, files):
        '''
        Prepare files data for cid.
        
        File data have bytes of file, maintype, subtype, cid, filename, encoding.        
        files : dict
        '''
        cid_dict = {}
        for key, file in files.items():
            mtype, encoding, mode, filename = self.get_MEMF(file)
            with open(file, mode, encoding = encoding) as f:
                fdata = f.read()
                cid_dict[key] = {'attachment': fdata, 'maintype': mtype[0], 'subtype': mtype[1],\
                              'cid': make_msgid(domain = self._gid)[1:-1], 'filename' : filename, 'encoding' : encoding}
        return cid_dict 
    
    
    def sorting_cids(self, cids):
        '''
        Soring cids, to make self._embedded type at first in cids, after that other type.
        
        cids : data set from cid_list() or cid_dict()
        '''
        cid_list1 = [] #to store self._embedded types
        cid_list2 = [] #to store other types
        if type(cids) == list:  #cids is list
            for l in cids:
                #different MIME maintye need different parameters
                if l['maintype'] in self._embedded: #audio, video, image are inline cotent of html
                    cid_list1.append(l)
                else:
                    cid_list2.append(l)
                
        elif type(cids) == dict:  #cids is dictionary
            for _, l in cids.items():
                if l['maintype'] in self._embedded: #audio, video, image are inline cotent of html
                    cid_list1.append(l)
                else:
                    cid_list2.append(l)
        
        return cid_list1 + cid_list2  #combines to one list
       
    
    def set_property(self, property_, value):
        '''
        General method to assign value to inner properties.
        
        property_ : string, name of property
        value : all kind of types
        '''
        property_ = '_' + property_
        self.__dict__[property_] = value
        
    def get_property(self, property_):
        '''
        General method to get value of inner properties.
        
        property_ : string, name of property 
        '''
        return self.__dict__['_' + property_]
    
    def get_addresses(self):
        '''
        Get all email addresses in email.
        '''
        tos = self._mail.get_all('to', [])
        ccs = self._mail.get_all('cc', [])
        resent_tos = self._mail.get_all('resent-to', [])
        resent_ccs = self._mail.get_all('resent-cc', [])
        addresses = []
        for t in getaddresses(tos + ccs + resent_tos + resent_ccs):
            addresses.append(t[1])
        return addresses        
    
    def get_mail(self):
        '''
        Get total email body.
        '''
        self._mail['From'] = self._from
        self._mail['To'] = self._to
        self._mail['Subject'] = self._subject
        return self._mail
    

    
######################################################
import smtplib
import re

class MiniPostMan:
    '''
    MiniPostMan fulfills lite function to send email, of which inner core is stmplib, standard module of python.
    '''
    
    def __init__(self, host='', useremail='', pwd='', debuglevel = 0):
        '''
        initialization of class, setting required properties.
        
        host : string, the smtp server url
        usermail : string, account to login host, email address of sender is ok
        pwd ： password of login
        debuglevel : set the debug output level
        '''
        self._host = host
        self._user = useremail
        self._pwd = pwd
        self._debuglevel = 0
    
    def email_valid(self, addresses):
        '''
        To validate email address。
        
        addresses : list, with email addresses
        '''
        patten = pattern = r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$' #reg patten
        if isinstance(addresses,list):
            for addr in addresses:
                if not re.search(patten, addr):
                    print('email error')
                    return False
        else:
            if not re.search(patten, addresses):
                print('email error')
                return False
        return True
    
    def quick_send(self, receiver, subject='hello', content=''):
        '''
        Lite method to send a text email.
        
        receiver : string, email address of receiver
        subject : string, subject of email
        content : string, message
        '''
        if self.email_valid(receiver):
            msg = EmailMessage()
            msg['Subject'] = subject
            msg['From'] = f'{self._user}<{self._user}>'
            msg['To'] = receiver
            
            try:
                smtpObj = smtplib.SMTP(self._host)
                smtpObj.set_debuglevel(self._debuglevel)
                smtpObj.login(self._user, self._pwd)
                smtpObj.sendmail(self._user, receiver, msg.as_string())                
                print('sent email')
                smtpObj.quit()
                return Ture
            except smtplib.SMTPException as err:
                print('failed:', err)
                return False
    
    def get_addresses(self, mail):
        '''
        Get all addresses in mail.
        
        mail : email.message, an instance of email.messages
        '''
        tos = mail.get_all('to', [])
        ccs = mail.get_all('cc', [])
        resent_tos = mail.get_all('resent-to', [])
        resent_ccs = mail.get_all('resent-cc', [])
        addresses = []
        for t in getaddresses(tos + ccs + resent_tos + resent_ccs):
            addresses.append(t[1])
        return addresses   
    
    def send_mail(self, mail, method = 'smtp'):
        '''
        Send email.
        
        mail : email.message, an instance of email.messages
        method : string, send method, smtp or ssl
        '''
        if self.email_valid(self.get_addresses(mail)):
            try:
                if method == 'ssl':
                    smtpObj = smtplib.SMTP_SSL(self._host)
                else: #default smtp mothod
                    smtpObj = smtplib.SMTP(self._host)
                    
                smtpObj.set_debuglevel(self._debuglevel)
                smtpObj.login(self._user, self._pwd)
                smtpObj.send_message(mail)
                smtpObj.quit()
                return True
            except smtplib.SMTPException as err:
                print('failed', err)
                return False

    
    def set_property(self, property_, value):
        '''
        General method to assign value to inner properties.
        
        property_ : string, name of property
        value : all kind of types
        '''
        property_ = '_' + property_
        self.__dict__[property_] = value