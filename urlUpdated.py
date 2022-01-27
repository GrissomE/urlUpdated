import time, os, hashlib, json, re, requests
import requests
from bs4 import BeautifulSoup
from twilio.rest import Client

def log(text):
    print(f'{time.strftime("%Y %m %d - %H:%M:%S")}: {text}')

def error(text, exception):
    log(f'{text} while {exception.with_traceback}')

def load_json(filename):
    try: 
        file_abs_path = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(file_abs_path, filename), encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        error(f'Failed to load file {filename}', e)

def write_json(filename, contents):
    try: 
        file_abs_path = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(file_abs_path, filename), 'w') as file:
            json.dump(contents, file)
    except Exception as e:
        error(f'Failed to write file {filename}', e)

def send_sms(text):
    account_sid = secrets["SID"]
    auth_token  = secrets["Key"]
    from_num    = secrets["From"]
    dest        = secrets["To"]

    try: 
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            to=dest, 
            from_=from_num,
            body=text)
        
        log(f'Notified {message.sid}')
    except Exception as e:
        error(f'Failed sending SMS', e)

def parse_page(page):
    soup = BeautifulSoup(page, 'html.parser')
    return soup.getText()

def get_page(url):
    #Chrome User Agent
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}
    page = requests.get(url, headers=headers)
    bs = parse_page(page.text)
    return bs.encode('utf-8')

def init_url(url, url_hash, hashes):
    response = get_page(url)
    page_hash = hashlib.sha256(response).hexdigest()
    return update_hash(url_hash, page_hash, hashes)

def update_hash(url_hash, page_hash, hashes):
    hashes[url_hash] = page_hash
    return True

def check_url(url, url_hash, hashes):
    try:
        response = get_page(url)
        page_hash = hashlib.sha256(response).hexdigest()

        if page_hash != hashes[url_hash]:
                domain_name = (re.search(r'://([A-Za-z_0-9.-]+).*', url))
                message = f'{domain_name.group(1)} changed: \n\n{url}'
                send_sms(message)
                return update_hash(url_hash, page_hash, hashes)
        else: return False
            
    except Exception as e:
        error(f'Failed checking URL: {url}', e)

if __name__ == "__main__":
    secrets = load_json('twilio.json')
    hashes  = load_json('hashes.json')
    urls    = load_json('urls.json')
    updated_hash = False

    for url in urls:
        url_hash = hashlib.sha256(url.encode('utf-8')).hexdigest()
        
        if url_hash in hashes:
            updated_hash |= check_url(url, url_hash, hashes)
        else: 
            updated_hash |= init_url(url, url_hash, hashes)

    if updated_hash:
        write_json('hashes.json', hashes)