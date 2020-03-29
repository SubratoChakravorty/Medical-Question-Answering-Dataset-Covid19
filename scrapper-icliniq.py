from bs4 import BeautifulSoup
import requests
import json

def preprocess_text(text):
    '''

    :param text:
    :return:
    '''
    assert isinstance(text, str)
    return text.replace('\n',' ').strip()


def get_question_answers(url,tokens=None):
    '''
    Fetches the doctor-patient conversation from the input url and returns the data as a dictionary
    :param url: icliniq question url from which data needs to be fetched
    :param tokens: list of tokens out of which atleast one should be present in the conversation
    :return: returns doctor-patient conversation as dictionary
    '''

    assert isinstance(url, str), 'url must be of type string'

    source = requests.get(url).text
    data = BeautifulSoup(source, 'lxml')
    response = dict()

    article_head = data.find('h1', class_='article-details-heading')
    article_head_text = preprocess_text(article_head.text)

    #print(article_head_text)
    response['article_head'] = article_head_text

    # ques_div = data.find('div',class_='alert alert-default border corner qContent')
    # ques_text = preprocess_text(ques_div.text)
    # response['question'] = ques_text

    conv_divs = data.find('div',class_='col-lg-12 col-sm-12 col-md-12 col-xs-12 p-0 articleConDiv')
    all_divs = conv_divs.find_all('div', class_=['alert alert-default border corner qContent', 'answerDiv'])

    qna_text = []
    for block in all_divs:
        class_name = " ".join(block['class'])
        #print(" ".join(block['class']))

        if class_name == 'alert alert-default border corner qContent':
            qna_text.append(('patient', preprocess_text(block.text.replace('Patient\'s Query',""))))
        if class_name == 'answerDiv':
            sub_block = block.find('div', class_='ansExtCon')
            qna_text.append(('doctor', preprocess_text(sub_block.text)))
        #print(preprocess_text(block.text))

    response['qna'] = qna_text

    # #print(ques_text.replace('Patient\'s Query',""))
    
    return response

def print_response(resp):
    '''

    :param resp:
    :return:
    '''

    print('Article Head: ', resp['article_head'])
    print('qna')
    for elem in resp['qna']:
        print(elem)


# print(get_question_answers('https://www.icliniq.com/qa/covid-19/i-have-cough-with-no-travel-history-is-this-a-symptoms-of-covid-19'))

root_url = 'https://www.icliniq.com/'
source_urls = ['https://www.icliniq.com/qa/coronavirus','https://www.icliniq.com/qa/coronavirus?page=2','https://www.icliniq.com/qa/covid-19']

urls = set()
for source_url in source_urls:
    source = requests.get(source_url).text
    data = BeautifulSoup(source, 'lxml')

    url_divs = data.find_all('div', class_='alert alert-default border corner post-health-issue')
    for div in url_divs:
        urls.add(root_url + div.a.attrs['href'])

responses = []
print(len(urls))
for url in urls:
    response = (get_question_answers(url))
    print_response(response)
    print(len(response['qna']))

# if responses:
#     with open(f'iCliniqData.json','w') as js:
#         json.dump(responses, js)