from bs4 import BeautifulSoup
import requests


def preprocess_text(text):
    '''

    :param text:
    :return:
    '''
    assert isinstance(text, str)
    return text.replace('\n',' ').strip()


def get_question_answers(url,  tokens = None):
    '''
    returns a dictionary of question and its answers fetched from the url
    :param tokens:
    :param url: HealthTap url of the question
    :return: dictionary
    output format
    {
    question: "Question"
    doctors:[
        {name:'Name',
        answer:'answer'
        }
        ]
    }
    '''
    if tokens is None:
        tokens = []
    assert isinstance(url, str), 'url must be of type string'

    source = requests.get(url).text
    # print(source)
    data = BeautifulSoup(source, 'lxml')
    # print(data)
    response = dict()
    response['answers'] = []
    data1 = data.find('div', class_='questions-container')
    flag = False
    # block type 1
    if data1 is None:
        data2 = data.find('div', class_='main-col')
        # extract question
        ques_data = data.find('h1', class_='question-header')
        ques = preprocess_text(ques_data.a.text)
        for token in tokens:
            if token in ques.lower():
                flag = True
                break

        response['question'] = ques
        # extract answer and doc names
        ans_data = data2.find_all('div', class_='answer-section')
        for block in ans_data:
            ans_block = dict()
            text = preprocess_text(block.find('div', class_='answer-body').text)
            for token in tokens:
                if token in text.lower():
                    flag = True
                    break
            ans_block['text'] = text
            doc_name = block.find('a',class_='author-header').text
            ans_block['doctor name'] = preprocess_text(doc_name)
            response['answers'].append(ans_block)

        if tokens is None:
            return response
        if flag:
            return response

        return None


    # block type 2
    ques_data = data.find('div', class_='question-text')
    ques = preprocess_text(ques_data.h1.text)
    response['question'] = ques
    for token in tokens:
        if token in ques.lower():
            flag = True
            break
    response['answers'] = []
    data1 = data1.find_all('div', class_="question-container delayed_image_container new_mobile_layout inline-container")
    for block in data1:
        ans_block = {}
        answer = block.find('div', class_='no-my-question-content')
        text = answer.h2.text
        for itr, elem in enumerate(answer.find_all('div', class_='answer_text')):
            text += elem.text
        text = preprocess_text(text)
        for token in tokens:
            if token in text.lower():
                flag = True
                break
        ans_block['text'] = text
        doc_name = block.find('div', class_='doctor-info').text
        ans_block['doctor name'] = preprocess_text(doc_name)
        response['answers'].append(ans_block)

    if tokens is None:
        return response
    if flag:
        return response

    return None

urls = list()
root_url = 'https://www.healthtap.com/'
page_no = '1'
source_url = 'https://www.healthtap.com/marketing/recent?page='+page_no
source = requests.get(source_url).text
data = BeautifulSoup(source, 'lxml')
data = data.find('div',class_='topic-column full-width-column')
urls = [elem.a['href'] for elem in data.find_all('p')]
texts = [elem.text for elem in data.find_all('p')]
urls = [root_url + elem for elem in urls]
responses = []
for id, url in enumerate(urls):
    print("url no: ",id,url)
    response = get_question_answers(url,['covid','corona','virus'])
    if response:
        print('Question: ',response['question'])
        print('Answers: ', response['answers'])
        responses.append(response)
import json
if responses:
    with open('HealthTapRecentPage'+page_no+'.json','w') as js:
        json.dump(responses, js)



url = 'https://www.healthtap.com/user_questions/7141393-my-husband-works-everywhere-including-a-short-trip-to-east-london-last-week-he-s-showing-symptoms-o'
source = requests.get(url).text
# print(source)
data = BeautifulSoup(source, 'lxml')
# print(data)
response = dict()
response['answers'] = []
data1 = data.find('div', class_='questions-container')
data1 = data1.find_all('div', class_="question-container delayed_image_container new_mobile_layout inline-container")
# for block in data1:
#         # answer = data1.find('div',class_=)
#         doc_name = block.find('div',class_='doctor-info').text
#         print(doc_name.replace('\n',''))
# print(get_question_answers(url))