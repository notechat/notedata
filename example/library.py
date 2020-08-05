from notedata.manage import DatasetManage
from notedata.manage.library import insert_library


def run1():
    insert_library()


def run2():
    dataset = DatasetManage()
    dataset.download("coco-annotations_trainval2017", path='./download/coco')


run1()
# run2()
