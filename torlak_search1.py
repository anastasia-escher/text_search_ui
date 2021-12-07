import os
import codecs
from nltk import word_tokenize, sent_tokenize
import eel
from all_data import data
from texts import texts


@eel.expose
def get_data(query):
    answer = []
    query = query.lower()
    query_list = query.split()
    for file, sentences in data.items():
        for index, sent in enumerate(sentences):
            for item in query_list:
                tokens_list = sent.lower().split()
                for token in tokens_list:
                    if token.startswith(item):
                        if item in sent.lower():
                            s = ''
                            sent_list = word_tokenize(sent)
                            for word in sent_list:
                                if word in [',', '.', '!', '?', ':', '_', '-', ';']:
                                    s = s + word
                                elif word.lower().startswith(item) or word.lower() == item:
                                    s += " "
                                    s += f'<span style="color:red;">{word}</span> '
                                else:
                                    s += " "
                                    s += f'<span>{word}</span>'
                            b = f"<div id='{file}_sent_{index}' class='sentence {index}'><span class='{file} link' onclick='openFile(event)'> {file}</span>:  {s} <span class='expand {file} {index}' onclick='expand(event)'>[expand context]</span> </div>"
                            answer.append(b)

    return answer


@eel.expose
def expand_context(file, index, query):
    print(file)
    print(index)
    b = ''
    index = int(index)
    sentences = data[file]
    relevant_sentences = sentences
    if 5 <= index <= len(sentences) - 5:
        relevant_sentences = sentences[index - 5: index + 4]
    elif index < 5:
        relevant_sentences = sentences[: index + 7]
    elif index > len(sentences) - 5:
        relevant_sentences = sentences[index - 8:]
    for i, sent in enumerate(relevant_sentences):
        s = ''
        sent_list = word_tokenize(sent)
        for word in sent_list:
            if word in [',', '.', '!', '?', ':', '_', '-', ';']:
                s = s + word
            else:
                if word.startswith(query):
                    s += " "
                    s += f'<span style="color: red">{word}</span>'
                else:
                    s += " "
                    s += f'<span>{word}</span>'
        b += f"<span>{s}</span> "

    return f"<span class='{file} link' onclick='openFile(event)'> {file}</span>" + " " + b + "</div>"


@eel.expose
def open_file(file):
    print(file)
    text = texts[file]
    text_list = text.split('\n')
    a = ''
    for t in text_list:
        a += t
        a += "<br/>"
    return "<button onclick='back()' >Back</button><br/>" + a

@eel.expose
def get_data_with_context(query):
    print(query)
    answer = []
    query = query.lower()
    query_list = query.split()
    for file, sentences in data.items():
        for index, sent in enumerate(sentences):
            for item in query_list:
                tokens_list = sent.lower().split()
                for token in tokens_list:
                    if token.startswith(item):
                        if item in sent.lower():
                            s = ''
                            sent_list = word_tokenize(sent)
                            for word in sent_list:
                                if word in [',', '.', '!', '?', ':', '_', '-', ';']:
                                    s = s + word
                                elif word.lower().startswith(item) or word.lower() == item:
                                    s += " "
                                    s += f'<span style="color:red;">{word}</span> '
                                else:
                                    s += " "
                                    s += f'<span>{word}</span>'
                            b = f"<div id='{file}_sent_{index}' class='sentence {index}'><span class='{file} link' onclick='openFile(event)'> {file}</span>:  {s} <span class='expand {file} {index}' onclick='expand(event)'>[expand context]</span> </div>"
                            relevant_sentences = sentences
                            answ = f"<div id='{file}_sent_{index}' class='sentence {index}'><span class='{file} link' onclick='openFile(event)'> {file}</span>:"
                            if 5 <= index <= len(sentences) - 5:
                                relevant_sentences = sentences[index - 5: index + 4]
                            elif index < 5:
                                relevant_sentences = sentences[: index + 7]
                            elif index > len(sentences) - 5:
                                relevant_sentences = sentences[index - 8:]
                            for j, sen in enumerate(relevant_sentences):
                                string = ''
                                sen_list = word_tokenize(sen)
                                for token in sen_list:
                                    if token in [',', '.', '!', '?', ':', '_', '-', ';']:
                                        string = string + token
                                    else:
                                        string += " "
                                        string += f'<span>{token}</span>'
                                answ += f"<span>{string}</span> "
                            answ += "</div>"
                            answer.append(answ)

    return answer

eel.init('web')
eel.start('main.html', size=(700, 700))
