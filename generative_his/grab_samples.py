
import datetime
import wikipediaapi

try:
    import cPickle as pickle
except ImportError:  # Python 3.x
    import pickle

from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline


wiki_wiki = wikipediaapi.Wikipedia('en')

collected = {'title': [],
             'show_item': [],
             'neuro_item': [],
             }
now = datetime.datetime.now()
for i in range(365):
    print("Iteration: {0}".format(i + 1))
    no = now + datetime.timedelta(days=1)

    date = '{0}_{1}'.format(no.strftime("%B"),
                            no.day)

    page_py = wiki_wiki.page(date)

    for sec in page_py.sections:
        if sec.title == 'Events':
            break
        else:
            continue

    # qa_questions = ['What happened?',
    #                 'Describe it',
    #                 "What's the matter?"]

    # qa_model_name = "deepset/roberta-base-squad2"
    # qa_nlp = pipeline('question-answering', model=qa_model_name, tokenizer=qa_model_name)

    for period in sec.sections:
        title = period.title
        show_items = period.text.split('\n')
        neuro_items = [x[x.index('– ')+2:] for x in period.text.split('\n')]
        for j in range(len(show_items)):
            show_item = show_items[j]
            neuro_item = neuro_items[j]

            collected['title'].append(title)
            collected['show_item'].append(show_item)
            collected['neuro_item'].append(neuro_item)
            """
            for cat in qa_questions:

                QA_input = {
                    'question': cat,
                    'context': neuro_item
                }
                neuro_cat = qa_nlp(QA_input)

                collected['title'].append(title)
                collected['show_item'].append(show_item)
                collected['neuro_item'].append(neuro_cat)
            """
with open('NONO.p', 'wb') as fp:
    pickle.dump(collected, fp, protocol=pickle.HIGHEST_PROTOCOL)
