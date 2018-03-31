from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import os
import sys
from flask import Flask, render_template, request, jsonify
import json
import uuid

CHROMEDRIVER_PATH = os.path.abspath("./chromedriver")
PROFILES_PATH = './profiles.json'
SOURCES_PATH = './sources.json'

options = webdriver.ChromeOptions()
options.add_argument("headless")
driver = webdriver.Chrome(chrome_options=options, executable_path=CHROMEDRIVER_PATH)
app = Flask(__name__)


@app.route('/')
def hello():
    return render_template("index.html")

@app.route('/gather', methods=['POST'])
def gather_from_source():
    driver.get(request.form['urls'][0])
    delay = 2 # seconds
    try:
        myElem = WebDriverWait(driver, delay)
        print("Page is ready!")
    except TimeoutException:
        print("Loading took too much time!")

    headlines = driver.find_elements_by_css_selector(request.form['selectors'][0])
    result = []
    for hl in headlines:
        for word in request.form['keywords']:
            if word.lower() in hl.text:
                result.append(hl.text)

    print(result)
    return jsonify(result)

@app.route('/add/profile', methods=['POST'])
def handle_add_profile():
    name = request.form['name'].strip()

    if len(name) < 1:
        return None

    _id = uuid.uuid4().hex
    
    profiles = {'records': []}
    profile = {'id': _id, 'name': name}
    
    if os.path.isfile(PROFILES_PATH):
        profiles = json.load(open(PROFILES_PATH))
    
    profiles['records'].append(profile);

    with open(PROFILES_PATH, 'w') as f:
        json.dump(profiles, f)

    return jsonify(profile)


@app.route('/get/profiles', methods=['GET'])
def handle_get_profile():
    profiles = json.dumps({'records':[]})
    if os.path.isfile(PROFILES_PATH):
        profiles = json.load(open(PROFILES_PATH))
    return jsonify(profiles)

@app.route('/remove/profile', methods=['POST'])
def handle_remove_profile():
    _id = request.form['id'].strip()
    print(_id)
    if len(_id) > 0:
        profiles = json.load(open(PROFILES_PATH))

    for i in range(len(profiles['records'])):
        if profiles['records'][i]['id'] == _id:
            del profiles['records'][i]
            break

    with open(PROFILES_PATH, 'w') as f:
        json.dump(profiles, f)

    return jsonify(profiles)

@app.route('/add/source', methods=['POST'])
def handle_add_source():
    source = {  'id': uuid.uuid4().hex,
                'name': request.form['name'].strip(),
                'urls': request.form['urls'].split(","),
                'selectors': request.form['selectors'].split(";"),
                'keywords': request.form['keywords'].split(",")}

    
    if os.path.isfile(SOURCES_PATH):
        sources = json.load(open(SOURCES_PATH))

    if request.form['id'] not in sources:
        sources[request.form['id']] = []

    sources[request.form['id']].append(source)

    with open(SOURCES_PATH, 'w') as f:
        json.dump(sources, f)

    return jsonify(sources)

@app.route('/get/sources/<pid>', methods=['GET'])
def handle_get_sources(pid):
    
    sources = {pid:[]}
    pid_sources = []

    if os.path.isfile(SOURCES_PATH):
        sources = json.load(open(SOURCES_PATH))

    if pid in sources:
        pid_sources = sources[pid]

    return jsonify(pid_sources)

@app.route('/remove/sources/<pid>/<sid>', methods=['GET'])
def hand_remove_source(pid, sid):

    sources = {pid: []}

    if os.path.isfile(SOURCES_PATH):
        sources = json.load(open(SOURCES_PATH))

    for i in range(len(sources[pid])):
        if sources[pid][i].id == sid:
            del sources[pid][i]
            break

    with open(SOURCES_PATH, 'w') as f:
        json.dump(sources, f)

    return jsonify(sources)

if __name__ == '__main__':
    app.run(port=3000)
    driver.quit()
