from GeniaTaggerClient import GeniaTaggerClient
import os
from time import sleep
import pymysql

source_path = r"C:/Users/beko/Desktop/random pubmed files/"
target_path = r"C:/Users/beko/Desktop/random pubmed files/processed"
con = pymysql.connect('localhost', 'root', 'pass', 'testdb')

def run():
    tagger = GeniaTaggerClient()
    process_files(tagger)


def process_files(tagger):
    source_files = get_files()
    for file in source_files:
        body = get_file_body(file)
        tagger.send_message(body)
        tags = try_to_get_tags(tagger)
        processed_filename = os.path.join(target_path, file)
        f = open(processed_filename, "w+")
        for tag_for_word in tags:
            f.write('\t'.join(tag_for_word) + '\n')
        f.close()


def try_to_get_tags(tagger):
    tags = tagger.get_tags()
    try_count = 0
    while len(tags) == 0 or try_count < 5:
        sleep(2)
        tags = tagger.get_tags()
        try_count += 1
    return tags


def get_file_body(filename):
    source_filename = os.path.join(source_path, filename)
    f = open(source_filename, "r")
    return f.read()


def get_files():
    source_files = []
    for file in os.listdir(source_path):
        if file.endswith(".txt"):
            source_files.append(file)
    return source_files


def getTestSentence(filename="BB-cat-6417341.gt"):
    realTags = []
    words = []
    path = r"C:/Users/beko/Desktop/Yüksek Lisans/3. Dönem/Thesis/BB3_genia-tagger_test_resources/BB3/genia-tagger/test/BioNLP-ST-2016_BB-cat_test"
    path += "/" + filename
    f = open(path, "r")
    f1 = f.readlines()
    for line in f1:
        if line != '\n':
            lineAsArr = line.split(None)
            realTags.append(lineAsArr)
            words.append(lineAsArr[0])
    sentence = " ".join(words)
    return sentence, realTags

run()