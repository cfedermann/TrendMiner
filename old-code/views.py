"""
Django views for the MUSING Service reputation application.

Defines the views for the MUSING Service reputation section.

"""
import codecs
import datetime
import logging
import os
import tempfile
import urllib2

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from subprocess import call
from time import sleep
from traceback import format_exc
from xml.etree import ElementTree as ET

from reputation.forms import RateCompanyForm
from settings import BASE_FOLDER, LOG_HANDLER, LOG_LEVEL

# Setup logging support.
logging.basicConfig(level=LOG_LEVEL)
LOGGER = logging.getLogger('reputation.views')
LOGGER.addHandler(LOG_HANDLER)


def rate_company_from_url(source_url):
    """Computes the company ratings for the given source URL ZIP file."""
    if not source_url.lower().endswith('.zip'):
        result = "ERROR: file is not a ZIP file at URL {0}".format(
          source_url)
        LOGGER.info("result: {0}".format(result))
        return result

    source_file = os.path.split(source_url)[1]
    LOGGER.info("source_file: {0}".format(source_file))

    perl_folder = '{0}/reputation/perl'.format(BASE_FOLDER)
    tmp_folder = tempfile.mktemp(dir=perl_folder)
    tmp_name = os.path.split(tmp_folder)[1]
    LOGGER.info("tmp_folder: {0}, tmp_name: {1}".format(tmp_folder, \
      tmp_name))

    retcode = call(['mkdir', tmp_name], cwd=perl_folder)
    LOGGER.info("mkdir call: {0}".format(retcode))
    
    # We try up to five times to retrieve the ZIP file from the given URL.
    file_handle = open('{0}/{1}'.format(tmp_folder, source_file), 'wb')
    wget_successful = False
    for i in range(5):
        try:
            url_handle = urllib2.urlopen(source_url)
            content = url_handle.read()
            url_handle.close()
            file_handle.write(content)
            wget_successful = True

        except:
            LOGGER.info("urlopen exception: {0}".format(format_exc()))
            sleep(1)
            continue

        if wget_successful:
            break

    file_handle.close()

    if wget_successful:
        retcode = call(['unzip', '-o', source_file], cwd=tmp_folder)
        LOGGER.info("unzip call: {0}".format(retcode))
    
        retcode = call(['perl -I {0} ../om-xml.pl'.format(
          perl_folder)], cwd=tmp_folder, shell=True)
        LOGGER.info("perl call: {0}".format(retcode))

        try:
            _file = '{0}/om.xml'.format(tmp_folder)
            _handle = codecs.open(_file, 'r', 'utf-8')
            _result = _handle.read()
            _handle.close()

            result = _result
            LOGGER.info("result: {0}".format(result.encode('utf-8')))

        except:
            LOGGER.info(format_exc())
            result = format_exc()

    else:
        result = "ERROR: could not retrieve file from URL {0}".format(
          source_url)
        LOGGER.info("result: {0}".format(result))

    retcode = call(['rm -rf {0}'.format(tmp_folder)], shell=True)
    LOGGER.info("rm call: {0}".format(retcode))
    return result


def rate_company_from_string(zip_bytearray):
    """Computes the company ratings for the base64-encoded, ZIP-compressed
    byte array."""
    source_file = 'bytearray.zip'
    LOGGER.info("source_file: {0}".format(source_file))

    perl_folder = '{0}/reputation/perl'.format(BASE_FOLDER)
    tmp_folder = tempfile.mktemp(dir=perl_folder)
    tmp_name = os.path.split(tmp_folder)[1]
    LOGGER.info("tmp_folder: {0}, tmp_name: {1}".format(tmp_folder, \
      tmp_name))

    retcode = call(['mkdir', tmp_name], cwd=perl_folder)
    LOGGER.info("mkdir call: {0}".format(retcode))
    
    LOGGER.info("len(zip_bytearray): {0}".format(len(zip_bytearray)))

    # We try up to five times to retrieve the ZIP file from the given URL.
    file_handle = open('{0}/{1}'.format(tmp_folder, source_file), 'wb')
    file_handle.write(zip_bytearray)
    file_handle.close()

    retcode = call(['unzip', '-o', source_file], cwd=tmp_folder)
    LOGGER.info("unzip call: {0}".format(retcode))

    retcode = call(['perl -I {0} ../om-xml.pl'.format(
      perl_folder)], cwd=tmp_folder, shell=True)
    LOGGER.info("perl call: {0}".format(retcode))

    try:
        _file = '{0}/om.xml'.format(tmp_folder)
        _handle = codecs.open(_file, 'r', 'utf-8')
        _result = _handle.read()
        _handle.close()

        result = _result
        LOGGER.info("result: {0}".format(result.encode('utf-8')))

    except:
        LOGGER.info(format_exc())
        result = format_exc()

    retcode = call(['rm -rf {0}'.format(tmp_folder)], shell=True)
    LOGGER.info("rm call: {0}".format(retcode))
    return result


@login_required
def rate_company(request):
    """Rates the given companies."""
    result = None
    entities = []

    if request.method == 'POST':
        form = RateCompanyForm(request.POST)

        if form.is_valid():
            url_handle = urllib2.urlopen(form.cleaned_data['source_url'])
            zip_bytearray = url_handle.read()
            url_handle.close()

            result = rate_company_from_string(zip_bytearray)
            _handle = codecs.open('/tmp/foobar.xml', 'w', 'utf-8')
            _handle.write(result)
            _handle.close()

            # Read in result XML as ElementTree object.
            result_tree = ET.fromstring(result)
            
            entities = []
            for entity in result_tree.findall('entity'):
                name = entity.find('name').text
                source_name = entity.find('source_name').text
                source_id = entity.find('source_id').text
                source_title = entity.find('source_title').text
                
                if entity.find('pub_date/month').text and \
                  entity.find('pub_date/day').text and \
                  entity.find('pub_date/year').text:
                    pub_date = "{0}/{1}/{2}".format(
                      entity.find('pub_date/month').text,
                      entity.find('pub_date/day').text,
                      entity.find('pub_date/year').text)
                else:
                    pub_date = None
                
                if entity.find('pub_time/hour').text and \
                  entity.find('pub_time/minute').text:
                    pub_time = "{0}:{1}".format(
                      entity.find('pub_time/hour').text,
                      entity.find('pub_time/minute').text)
                else:
                    pub_time = None

                if entity.find('ticker_time/ticker_hour').text and \
                  entity.find('ticker_time/ticker_minute').text:
                    ticker_time = "{0}:{1}".format(
                      entity.find('ticker_time/ticker_hour').text,
                      entity.find('ticker_time/ticker_minute').text)
                else:
                    ticker_time = None
                
                ticker_string = entity.find('ticker_string').text
                polarity = int(entity.find('polarity').text)

                empty = range(4-polarity)
                full = range(polarity)
                
                entities.append({'name': name, 'polarity': polarity,
                  'pub_date': pub_date, 'ticker_string': ticker_string,
                  'pub_time': pub_time, 'ticker_time': ticker_time,
                  'source_name': source_name, 'source_id': source_id,
                  'source_title': source_title, 'empty': empty,
                  'full': full})
            
#            result = rate_company_from_url(form.cleaned_data['source_url'])

    else:
        form = RateCompanyForm()

    result_len = 0
    filename = None
    if result:
        result_len = len(result)
        
        filename = datetime.datetime.now().strftime("%Y%m%d")
        handle = open('/tmp/{0}.xml'.format(filename), 'w')
        handle.write(result)
        handle.close()
    
    template_info = {'form': form, 'result': result, 'result_xml_file': filename,
      'result_xml_size': result_len, 'dictionary_file': 'foo', 'dictionary_size': 2435356,
      'entities': entities}
    return render_to_response('reputation/rate_company.html', template_info,
      context_instance=RequestContext(request))

def download(request, filename):
    """
    Downloads the result of a company rating process.
    """
    content = open('/tmp/{0}.xml'.format(filename), 'r').read()
    response = HttpResponse(content, mimetype='text/xml')
    response['Content-Disposition'] = 'attachment; filename={0}.xml'.format(
      filename)
    return response
