import os
import pymysql
import json
import requests

con = pymysql.connect(host='localhost',
        user='root',
        password='pass',
        db='testdb',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)
source_path = r"C:/Users/beko/Desktop/random pubmed files"
files_to_save_path = source_path + "/processed/files_going_to_be_saved_to_db"
BIOPORTAL_URL = "http://data.bioontology.org"
BIOPORTAL_API_KEY = "f9ac9769-573d-4a6c-943a-5bafc350c91e"


def test():
    run()

def run():
    files = get_files_to_save_to_db()
    for file in files:
        try:
            if is_already_saved(file.replace('.txt', '')):
                continue
            else:
                body = get_file_body(file)
                article_id = int(file.replace('.txt', ''))
                save_article(article_id, body)
                phrases = get_noun_phrases_of_file(file)
                phrase_list = save_phrases(article_id, phrases)
                save_ontologies_of_phrases(phrase_list)

        except:
            print("An error occured")


def save_ontologies_of_phrases(phrase_list):
    for item in phrase_list:
        try:
            phrase = item[1]
            response = search_bioportal(phrase)
            ontologies = get_ontologies(phrase, response)
            ontologies = list(set(ontologies))
            with con:
                cur = con.cursor()
                for ontology in ontologies:
                    query = "SELECT * FROM phrase_ontology_map WHERE phrase_id = %s and ontology = %s"
                    args = (item[0], ontology)
                    cur.execute(query, args)
                    result = cur.fetchone()
                    if result is None:
                        query = "INSERT INTO phrase_ontology_map(phrase_id, ontology) VALUES (%s, %s)"
                        args = (item[0], ontology)
                        cur.execute(query, args)
                    con.commit()
        except:
            print("An error occured while saving ontologies")


def get_ontologies(phrase, result):
    ontologies = []
    # result = search_bioportal(phrase)
    if result["collection"] is None:
        return ontologies
    for item in result["collection"]:
        if item["links"] is None or item["links"]["ontology"] is None:
            continue
        ontologies.append(item["links"]["ontology"])
    return ontologies


def search_bioportal(term):
    params = {'q': term, "apikey": BIOPORTAL_API_KEY, "require_exact_match": "false"}
    r = requests.get(BIOPORTAL_URL + "/search", params=params)
    if r.status_code == 200:
        bioportal_obj = json.loads(r.text)
    return bioportal_obj


def save_phrases(article_id, phrases):
    phrase_list = []
    for phrase in phrases:
        with con:
            cur = con.cursor()
            query = "SELECT * FROM phrases WHERE description = %s"
            args = (phrase)
            cur.execute(query, args)
            result = cur.fetchone()
            phrase_id = 0
            if result is None:
                query = "INSERT INTO phrases(description) VALUES (%s)"
                args = (phrase)
                cur.execute(query, args)
                phrase_id = cur.lastrowid
            else:
                phrase_id = result["phrase_id"]

            query = "SELECT * FROM article_phrase_map WHERE article_id = %s AND phrase_id = %s"
            args = (article_id, phrase_id)
            cur.execute(query, args)
            result = cur.fetchone()
            if result is None:
                query = "INSERT INTO article_phrase_map(article_id, phrase_id) VALUES (%s, %s)"
                args = (article_id, phrase_id)
                cur.execute(query, args)

            con.commit()
            phrase_list.append((phrase_id, phrase))
    return phrase_list


def get_noun_phrases_of_file(filename):
    body = get_lines(os.path.join(files_to_save_path, filename))
    tags = [line.rstrip().split("\t") for line in body]
    noun_phrases = []
    noun_phrase = []
    for tag in tags:
        if len(tag) < 3:
            continue
        if tag[3] == "B-NP":
            if len(noun_phrase) > 0:
                noun_phrases.append(noun_phrase)
                noun_phrase = []
            noun_phrase.append(tag)
        elif tag[3] == "I-NP":
            noun_phrase.append(tag)
        else:
            if len(noun_phrase) > 0:
                noun_phrases.append(noun_phrase)
                noun_phrase = []

    phrase_list = []
    for phrase_combo in noun_phrases:
        phrase = ""
        for item in phrase_combo:
            phrase += " " + item[0]
        phrase = phrase.strip()
        phrase_list.append(phrase)
    return phrase_list


def save_article(article_id, body):
    query = "INSERT INTO articles(article_id, body) " \
            "VALUES (%s,%s)"
    args = (article_id, body)

    with con:
        cur = con.cursor()
        cur.execute(query, args)
        con.commit()


def get_file_body(filename):
    source_filename = os.path.join(source_path, filename)
    f = open(source_filename, "r")
    return f.read()


def is_already_saved(id):
    result = False
    if id in alread_processed:
        result = True
    return result


def get_files_to_save_to_db():
    source_files = []
    for file in os.listdir(files_to_save_path):
        if file.endswith(".txt"):
            source_files.append(file)
    return source_files


def get_lines(file_path):
    text = ""
    try:
        fp = open(file_path, "r")
        text = fp.readlines()
    finally:
        fp.close()
    return text


alread_processed = ['30796577',
'22210242',
'22187105',
'22173014',
'22154332',
'22079582',
'22024431',
'22001285',
'21983180',
'21982932',
'21970990',
'21963442',
'21945867',
'21944154',
'21928146',
'21903111',
'21864689',
'21861684',
'21840401',
'21839779',
'21833506',
'21800317',
'21738775',
'21693631',
'21674496',
'21657113',
'21616985',
'21551226',
'21508236',
'21500439',
'21461354',
'21440651',
'21396383',
'21319890',
'21319887',
'21318348',
'21316366',
'21308791',
'21258326',
'21246555',
'21172318',
'21161750',
'21054692',
'21047644',
'20974156',
'20933023',
'20874778',
'20736510',
'18985107',
'18633805',
'17408599',
'16797609',
'10771245']

test()