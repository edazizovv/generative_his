
import datetime
import wikipediaapi

try:
    import cPickle as pickle
except ImportError:  # Python 3.x
    import pickle

wiki_wiki = wikipediaapi.Wikipedia('en')

now = datetime.datetime.now()
date = '{0}_{1}'.format(now.strftime("%B"),
                        now.day)


page_py = wiki_wiki.page(date)

for sec in page_py.sections:
    if sec.title == 'Events':
        break
    else:
        continue

collected = {'title': [],
             'show_item': [],
             'neuro_item': [],
             'images': [],
             }

image_generator = ...
stock_images_dir = './images/{image}.png'
qa_model = ...
qa_questions = [...]

for period in sec.sections:
    title = period.title
    show_items = period.text.split('\n')
    neuro_items = [x[x.index('– ')+2:] for x in period.text.split('\n')]
    for j in range(len(show_items)):
        show_item = show_items[j]
        neuro_item = neuro_items[j]

        images = image_generator.generate(neuro_item)

        collected['title'].append(title)
        collected['show_item'].append(show_item)
        collected['neuro_item'].append(neuro_item)

        cat = 'full'
        collected_images = []
        for image in images:
            collected_image = '{cat}_image'.format(cat=cat)
            image.save(stock_images_dir.format(image=collected_image))
            collected_images.append(collected_image)

        collected['images'].append(collected_images)

        for cat in qa_questions:
            neuro_cat = qa_model.answer(cat, neuro_item)

            collected['title'].append(title)
            collected['show_item'].append(show_item)
            collected['neuro_item'].append(neuro_cat)

            collected_images = []
            for image in images:
                collected_image = '{cat}_image'.format(cat=cat)
                image.save(stock_images_dir.format(image=collected_image))
                collected_images.append(collected_image)

            collected['images'].append(collected_images)

with open('collected.p', 'wb') as fp:
    pickle.dump(collected, fp, protocol=pickle.HIGHEST_PROTOCOL)
