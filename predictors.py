import requests
from bs4 import BeautifulSoup as bs
from lxml.html import fromstring
import numpy as np
import pandas as pd
import re, os
import json
import time
from timeit import default_timer as timer
import datetime
from io import StringIO
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def secretomep(fasta, proxy=None):
    post_rq_header = {
        'Host': 'services.healthtech.dtu.dk',
        'Origin': 'https://services.healthtech.dtu.dk',
        'Referer': 'https://services.healthtech.dtu.dk/services/SecretomeP-1.0/1-Submission.php',

        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
    }
    get_rq_header = {

        'Referer': 'https://services.healthtech.dtu.dk/services/SignalP-4.1/1-Submission.php',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
    }
    form_data = {
        'configfile': '/var/www/html/services/SecretomeP-1.0/webface.cf',
        'SEQSUB': '(binary)'
    }
    with requests.Session() as session:
        session.head('https://services.healthtech.dtu.dk/services/SecretomeP-1.0/1-Submission.php')
        if proxy is None:
            response = session.post(
                url='https://services.healthtech.dtu.dk/cgi-bin/webface2.fcgi',
                files={'SEQSUB': str.encode(fasta)},
                data=form_data,
                headers=post_rq_header,
                timeout=20,
                allow_redirects=False
            )
        else:
            response = session.post(
                url='https://services.healthtech.dtu.dk/cgi-bin/webface2.fcgi',
                files={'SEQSUB': str.encode(fasta)},
                data=form_data,
                headers=post_rq_header,
                timeout=20,
                allow_redirects=False,
                proxies={"http": proxy, "https": proxy}
            )

        loc = response.headers['Location']
        jobid = re.findall('jobid=(\w+)', loc)[0]
        sec_resp_url = f'https://services.healthtech.dtu.dk/cgi-bin/webface2.cgi?jobid={jobid}&wait=20'
        if proxy is not None:
            return sec_resp_url
        print(f"Results available at {sec_resp_url}")
        session.close()
    print(f'\rCurrent Status: queued...', end='')

    while True:
        time.sleep(30)
        ajax_response = requests.get(
            url=f'https://services.healthtech.dtu.dk/cgi-bin/webface2.cgi?ajax=1&jobid={jobid}')
        status = re.findall('status:(\w+)', ajax_response.text.replace('"', ''))[0]
        print(f'\rCurrent Status: {status}...', end='')
        if status in ['sanitized', 'killed']:
            return None
        elif status == 'finished':
            break

    time.sleep(5)
    results_response = requests.get(
        url=sec_resp_url
    )
    return results_response.text

def signalp(fasta):
    post_rq_header = {
        'Host': 'services.healthtech.dtu.dk',
        'Origin': 'https://services.healthtech.dtu.dk',
        'Referer': 'https://services.healthtech.dtu.dk/services/SignalP-4.1/1-Submission.php',

        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
    }
    get_rq_header = {

        'Referer': 'https://services.healthtech.dtu.dk/services/SignalP-4.1/1-Submission.php',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
    }
    form_data = {
        'configfile': '/var/www/html/services/SignalP-4.1/webface.cf',
        'SEQPASTE': '',
        'SEQSUB': '(binary)',
        'orgtype': 'euk',
        'Dcut-type': 'default',
        'Dcut-noTM': '0.45',
        'Dcut-TM': '0.50',
        'graphmode': '',
        'format': 'short',
        'method': 'best',
        'minlen': '',
        'trunc': ''
    }

    with requests.Session() as session:
        session.head('https://services.healthtech.dtu.dk/services/SignalP-4.1/1-Submission.php')

        response = session.post(
            url='https://services.healthtech.dtu.dk/cgi-bin/webface2.cgi',
            files={'SEQSUB': str.encode(fasta)},
            data=form_data,
            headers=post_rq_header,
            timeout=20,
            allow_redirects=False
        )

        loc = response.headers['Location']
        jobid = re.findall('jobid=(\w+)', loc)[0]
        print(f'SignalP results at: https://services.healthtech.dtu.dk/cgi-bin/webface2.cgi?jobid={jobid}&wait=20')
        session.close()
    print(f'\rCurrent Status: queued', end='')

    while True:
        time.sleep(30)
        ajax_response = requests.get(
            url=f'https://services.healthtech.dtu.dk/cgi-bin/webface2.cgi?ajax=1&jobid={jobid}')
        status = re.findall('status:(\w+)', ajax_response.text.replace('"', ''))[0]
        print(f'\rCurrent Status: {status}', end='')
        if status == 'sanitized':
            return None
        elif status == 'finished':
            break
    time.sleep(5)
    results_response = requests.get(
        url=f'https://services.healthtech.dtu.dk/cgi-bin/webface2.cgi?jobid={jobid}'
    )
    return results_response.text

def phobius(fasta):
    post_rq_header = {
        'Host': 'phobius.sbc.su.se',
        'Origin': 'https://phobius.sbc.su.se',
        'Referer': 'https://phobius.sbc.su.se/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
    }
    form_data = {
        'format': 'short'
    }
    response = requests.post(
        url='https://phobius.sbc.su.se/cgi-bin/predict.pl',
        files={'protfile': str.encode(fasta)},
        data=form_data,
        headers=post_rq_header,
        timeout=20,
    )
    return response.text

def topcons(fasta):
    wsdl_url = "https://topcons.net/pred/api_submitseq/?wsdl"
    myclient = Client(wsdl_url, cache=None)
    retValue = myclient.service.submitjob(fasta)
    if len(retValue) >= 1:
        strs = retValue[0]
        jobid = strs[0]
        result_url = strs[1]
        numseq = strs[2]
        errinfo = strs[3]
        warninfo = strs[4]
    strs = retValue[0]
    result_url = strs[1]
    print(f'Topcons results url at: {result_url}\nAwaiting response')
    response_url = f"https://topcons.net/static/result/{jobid}/{jobid}/query.result.txt"
    # https://topcons.net/pred/result/rst_0o0qubgj/
    while True:
        try:
            response = requests.get(response_url)
            if response.status_code == 200:
                break
        except:
            # print("Exception sleep for 2 mins")
            time.sleep(120)
            continue
    return response.text

def tmhmm(fasta):
    post_rq_header = {
        'Host': 'services.healthtech.dtu.dk',
        'Origin': 'https://services.healthtech.dtu.dk',
        'Referer': 'https://services.healthtech.dtu.dk/services/TMHMM-2.0/1-Submission.php',

        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
    }

    form_data = {
        'configfile': '/var/www/html/services/TMHMM-2.0/webface.cf',
        'seqfile': '(binary)',
        'outform': '-short'
    }

    # print("Sending data to TMHMM")
    with requests.Session() as session:
        session.head('https://services.healthtech.dtu.dk/services/TMHMM-2.0/1-Submission.php')

        response = session.post(
            url='https://services.healthtech.dtu.dk/cgi-bin/webface2.fcgi',
            files={'seqfile': str.encode(fasta)},
            data=form_data,
            headers=post_rq_header,
            timeout=20,
            allow_redirects=False
        )
        loc = response.headers['Location']
        jobid = re.findall('jobid=(\w+)', loc)[0]
        tmhmm_resp_url = f'https://services.healthtech.dtu.dk/cgi-bin/webface2.cgi?jobid={jobid}&wait=20'
        print(f'TMHMM results at: {tmhmm_resp_url}')
        session.close()
    print(f'\rCurrent Status: queued...', end='')
    while True:
        time.sleep(30)
        ajax_response = requests.get(
            url=f'https://services.healthtech.dtu.dk/cgi-bin/webface2.cgi?ajax=1&jobid={jobid}')
        status = re.findall('status:(\w+)', ajax_response.text.replace('"', ''))[0]
        print(f'\rCurrent Status: {status}...', end='')
        if status == 'finished':
            print()
            break

    time.sleep(5)
    results_response = requests.get(
        url=tmhmm_resp_url
    )
    return results_response.text

# def deepsig(fasta):
#
#     post_rq_header = {
#         'Host': 'deepsig.biocomp.unibo.it',
#         'Origin': 'https://deepsig.biocomp.unibo.it',
#         'Referer': 'https://deepsig.biocomp.unibo.it/deepsig/default/index',
#
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
#     }
#     # get_rq_header = {
#     #
#     #     'Referer': 'https://services.healthtech.dtu.dk/services/SignalP-4.1/1-Submission.php',
#     #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
#     # }
#     form_data = {
#         'configfile': '/var/www/html/services/SignalP-4.1/webface.cf',
#         'sequence': fasta,
#         'deepsig_kingdom': 'euk',
#         'deepsig': 'on',
#     }
#
#     print(f"Sending sequence to DeepSig")
#     with requests.Session() as session:
#         session.head('https://deepsig.biocomp.unibo.it/deepsig/default/index')
#
#         response = session.post(
#             url='https://deepsig.biocomp.unibo.it/deepsig/default/index',
#             # files={'SEQSUB': str.encode(fasta)},
#             data=form_data,
#             headers=post_rq_header,
#             # allow_redirects=False
#         )
#         return response.headers
#         time.sleep(60)
#         resp = requests.get("https://deepsig.biocomp.unibo.it/deepsig/default/downloadjob")
#         session.close()
#         return resp.text
#     #     return response.status_code
#     #     loc = response.headers['Location']
#     #     jobid = re.findall('jobid=(\w+)', loc)[0]
#     #     print(f'SignalP results at: https://services.healthtech.dtu.dk/cgi-bin/webface2.cgi?jobid={jobid}&wait=20')
#     # print(f'\rCurrent Status: queued', end='')
#
#     while True:
#         time.sleep(30)
#         ajax_response = requests.get(
#             url=f'https://services.healthtech.dtu.dk/cgi-bin/webface2.cgi?ajax=1&jobid={jobid}')
#         status = re.findall('status:(\w+)', ajax_response.text.replace('"', ''))[0]
#         print(f'\rCurrent Status: {status}', end='')
#         if status == 'finished':
#             print()
#             break
#     time.sleep(5)
#     results_response = requests.get(
#         url=f'https://services.healthtech.dtu.dk/cgi-bin/webface2.cgi?jobid={jobid}'
#     )
#     return results_response.text

def outcyte(fasta):
    CHROMEDRIVER_PATH = os.path.join(os.path.abspath(os.path.join(os.getcwd(), os.pardir)),
                                     'Web_Driver','chromedriver.exe')

    chrome_options = Options()
    chrome_options.add_argument("--headless")


    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,
                              chrome_options=chrome_options
                              )
    driver.implicitly_wait(10)
    driver.get(r"http://www.outcyte.com/analyse/")
    input_box = driver.find_element_by_name('seq')
    driver.execute_script('arguments[0].value=arguments[1]', input_box, fasta)
    submit = driver.find_element_by_xpath('//*[@id="seqInputForm"]/input[2]')
    submit.click()
    element = WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="predictions"]/div/div/table')))
    table = driver.find_element_by_xpath('//*[@id="predictions"]/div/div/table')
    table_data = table.text
    driver.close()
    driver.quit()
    return table_data

def deepsig(fasta):
    CHROMEDRIVER_PATH = os.path.join(os.path.abspath(os.path.join(os.getcwd(), os.pardir)),
                                     'Web_Driver','chromedriver.exe')

    chrome_options = Options()
    chrome_options.add_argument("--headless")


    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,
                              chrome_options=chrome_options
                              )
    driver.implicitly_wait(10)
    driver.get(r"https://deepsig.biocomp.unibo.it/deepsig/default/index")
    time.sleep(2)
    driver.find_element_by_link_text('Continue').click()
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    input_box = driver.find_element_by_xpath('//*[@id="subtab_sequence"]')
    driver.execute_script('arguments[0].value=arguments[1]', input_box, fasta)
    submit = driver.find_element_by_xpath('//*[@id="content"]/div[4]/form/table/tbody/tr[3]/td[2]/input')
    submit.click()
    element = WebDriverWait(driver, 1000).until(
        EC.presence_of_element_located((By.LINK_TEXT, 'Display results')))
        # EC.presence_of_element_located((By.XPATH, '//*[@id="c657836691101"]/div/div/a')))
    # element.click()
    # time.sleep(2)
    # job_id = driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[3]/div[2]')
    driver.get(r"https://deepsig.biocomp.unibo.it/deepsig/default/downloadjob")
    a = driver.page_source
    driver.close()
    driver.quit()
    return a


def get_proxies():
    url = "https://proxy-orbit1.p.rapidapi.com/v1/"

    headers = {
        'x-rapidapi-host': "proxy-orbit1.p.rapidapi.com",
        'x-rapidapi-key': "d63a75820dmshaed84677795732bp1a16b5jsn39ee9d0351ab"
    }

    response = requests.request("GET", url, headers=headers)
    proxy = json.loads(response.text)
    # print(proxy)
    # print(proxy['curl'])
    # print(proxy['post'])
    return  proxy['curl']

if __name__ == '__main__':
    pass