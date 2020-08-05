from notedata.manage import DatasetManage
from notedata.manage.library import insert_library


def run1():
    insert_library()


def run2():
    dataset = DatasetManage()
    dataset.download("coco-annotations_trainval2017", path='./download/coco')


def run3():
    data = DatasetManage()
    sources = data.select_pd()

    lines = ['|序号|分类|名称|描述|', '|:-:|:-:|:-:|:-:|']
    for i, source in enumerate(sources.to_dict(orient='records')):
        line = "|{i}|{category}|{name}|{describe}|".format(i=i,
                                                           name=source['name'],
                                                           category=source['category'],
                                                           describe=source['describe'])
        lines.append(line)

    text = open('README.md', 'r').read()
    text = text.replace("$dataset_table$", '\n'.join(lines))
    open('../README.md', 'w').write(text)


run1()
# run2()
run3()
