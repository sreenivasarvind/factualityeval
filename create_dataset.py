#Script to extract data from PubMed Articles
import os
import re
from glob import glob
# import pandas as pd
import csv
import json
import requests
import logging
print("import")

logger = logging.getLogger(__name__)
logging.basicConfig(filename='logs.log', encoding='utf-8', level=logging.DEBUG)
def extract_citation(text):
    citations = re.findall(r'\[[0-9]+\](?=\.$)', text)
    citations = [citation for citation in citations if citation.strip()]
    return citations


def extract_citation_id(text):
    pattern = r"\b\d{5,}\b"
    matches = re.findall(pattern, text)
    if matches:
        return matches[0]


def get_ids(sentences):
    data={}
    count = 0
    all_citations=[]
    article_refs =[]
    # for sentences in full_texts:
    refs=[]
    article_citations=[]
    article_refs=[]
    for index,line in enumerate(sentences):
        if re.search("==== Refs", line):
            refs = sentences[index:]
            article_refs.append(refs)
        citation = extract_citation(line)
        if citation:
            data[line.split('(')[0]] = citation
            citations = []
            for cite in citation:
                citations.append((line,int(cite.strip('[]'))))
            article_citations.append(citations)
    if article_citations and article_refs:
        for value in article_citations:
            if len(article_refs[0])>value[0][1]:
                count+=1
                all_citations.append([value,article_refs[0][value[0][1]]])

                all_citations.append([article_citations[0][0][0],article_refs[0][article_citations[0][0][1]]])

    for citation in all_citations:
        citation[1]= extract_citation_id(citation[1])
    return all_citations

def extract_full_text(data):
  section=''
  text = ''
  for info in data['documents'][0]['passages']:
    current_section = info['infons']['section_type']
    if current_section == "REF":
      break
    if current_section!=section:
      section = current_section
      text+=info['infons']['section_type'] + ' \n '
    text+= info['text'] + ' \n '
  return text


def check_open_access(all_citations):
    # try:
    count=0
    data=''
    dataset = {}
    open_access = []
    for citation in all_citations:
        pubmed_id = citation[1]
        if pubmed_id:
            headers = {
                'Accept': 'application/json'
            }
            url = "https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_json/"+pubmed_id+"/unicode"
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                count+=1
                data = response.json()
                full_text = extract_full_text(data)
                print("citation: ", citation)
                dataset[citation[0][0][0]] = full_text
                open_access.append(pubmed_id)
                    
    if len(dataset) == 0:
        return False
    return dataset


if __name__ == "__main__":
    directories= glob("data/*/", recursive = True)
    citations = []
    # filenames=[]
    final_data ={}
    count=0
    id_count = 0
    for directory in directories:
        files = os.listdir(directory)
        files = files[13558:]
        print(len(files))
        for file in files:
            try:
                print(file)
                print('in try')
                path = directory+file
                st = open(path, "r",encoding="utf8", errors='ignore').read()
                def split_on_full_stops(text):
                    return re.split(r'(?<=[^A-Z].[.!?]) +(?=[A-Z])', text)
                sentences = '::'.join(split_on_full_stops(st))
                sentences = sentences.replace("\n","::")
                all_citations = get_ids(sentences.split("::"))
                dataset = check_open_access(all_citations)
                print("data:",dataset)
                if dataset:
                    final_data.update(dataset)

                count+=1
                percent = (count/len(files))*100
                logging.info(count)
                # logging.info(len(filenames))
                # logging.info(id_count)
                print("Percent completed: ",percent,"id count: ",id_count)
                with open("data.json", "w") as outfile:
                    json.dump(final_data, outfile)

            except Exception as e:
                logging.info(e)
                print(e)
                print('except')
                pass




