# coding: utf-8
# Copyright (C) 2011 Officience.  All rights reserved.
#
# ----------
#
# @version $Revision$
from difflib import SequenceMatcher
import re
from django.utils.encoding import smart_str
import errno
from suds import WebFault
from officience_xmltool.xmltool import settings
import urllib2
from suds.client import Client
from suds.sax.element import Element
from BeautifulSoup import BeautifulSoup

def call_method(hostname, service_name, method_name, arguments={},
                message_content=None, message_content_type='application/xml', protocol='http'):
    """
    Call the specified method of a REST service and returns the
    response.

    @param hostname network name of the machine that hosts the REST
           service.
    @param service_name name of the service that supports the method
           to be called.
    @param method_name name of the method to be called.
    @param arguments dictionary of arguments to be passed to the
           REST service's method.  Each key/value identifies the name
           of a parameter and its value.

    @param the content, i.e., message body, that the REST method
           returns.
    """
    #url = '%s://%s/%s/%s?' % (protocol, hostname, service_name, method_name)
    global message_body
    url = '%s://%s?' % (protocol, hostname)

#    arguments['api_key'] = settings.LBS_API_KEY
    url_arguments = encode_url_arguments(arguments)
#
#    hash = hmac.new(settings.LBS_SECRET_KEY,
#                    msg=url_arguments,
#                    digestmod=hashlib.sha1)
#
#    url_arguments += '&api_sig=%s' % hash.hexdigest()

    url += url_arguments
    request = urllib2.Request(url)
    print url

    if message_content is not None:
        request.add_header('Content-Type', 'text/xml')
        request.add_data(message_content)
        #print message_content

    handle = None
    try:
        handle = urllib2.urlopen(request)
        message_body = handle.read()
        status_code = 200
    except urllib2.HTTPError, error:
        message_body = error.read()
        status_code = error.code
    finally:
        if handle is not None:
            handle.close()
    return (status_code, message_body)

def encode_url_arguments(arguments):
    url_arguments = ''
    for (parameter_name, parameter_value) in arguments.iteritems():
        if parameter_value is not None:
            if url_arguments != '':
                url_arguments += '&'
            url_arguments += parameter_name + '=' + urllib2.quote(parameter_value)

    return url_arguments

def read_mandatory_parameter(arguments, parameter_name):
    return arguments[parameter_name][0]

def read_optional_parameter(arguments, parameter_name, parameter_default_value=None):
    try:
        return arguments[parameter_name][0]
    except:
        return parameter_default_value