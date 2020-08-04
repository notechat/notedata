import json

from tqdm import tqdm

from notedata.manage.core import DatasetManage


def check():
    dataset = DatasetManage()
    dataset.create()

    data = dataset.select_all()
    d1 = json.loads(json.loads(data[0][3]))
    print(d1)
    print(d1['source'])


def insert_library():
    lines = []
    # iris
    lines.extend([
        {'name': 'iris',
         'category': 'dataset',
         'describe': 'iris数据集',
         'urls': {'source': 'https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data'},
         "path": 'iris/iris.data'}])

    # electronics
    lines.extend([
        {'name': 'electronics-reviews',
         'category': 'dataset',
         'urls': {
             "source": "http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Electronics_5.json.gz"
         },
         'path': 'electronics/reviews_Electronics_5.json.gz'},
        {'name': 'electronics-meta',
         'category': 'dataset',
         'urls': {
             "source": "http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/meta_Electronics.json.gz"
         },
         'path': 'electronics/meta_Electronics.json.gz'}])

    # movielens
    lines.extend([
        {'name': 'movielens-100k', 'category': 'dataset',
         'urls': {"source": "http://files.grouplens.org/datasets/movielens/ml-100k.zip"},
         'path': 'movielens/ml-100k.zip'
         },
        {'name': 'movielens-1m', 'category': 'dataset',
         'urls': {"source": "http://files.grouplens.org/datasets/movielens/ml-1m.zip"},
         'path': 'movielens/ml-1m.zip'
         },
        {'name': 'movielens-10m', 'category': 'dataset',
         'urls': {"source": "http://files.grouplens.org/datasets/movielens/ml-10m.zip"},
         'path': 'movielens/ml-10m.zip'
         },
        {'name': 'movielens-20m', 'category': 'dataset',
         'urls': {"source": "http://files.grouplens.org/datasets/movielens/ml-20m.zip"},
         'path': 'movielens/ml-20m.zip'
         },
        {'name': 'movielens-25m', 'category': 'dataset',
         'urls': {"source": "http://files.grouplens.org/datasets/movielens/ml-25m.zip"},
         'path': 'movielens/ml-25m.zip'
         }])

    # adult_data
    lines.extend([
        {
            'name': 'adult-train', 'category': 'dataset',
            'urls': {
                'source': 'https://raw.githubusercontent.com/1007530194/data/master/recommendation/data/adult.data.txt'
            },
            "path": 'adult-data/adult.train.txt'
        }, {
            'name': 'adult-test', 'category': 'dataset',
            'urls': {
                'source': 'https://raw.githubusercontent.com/1007530194/data/master/recommendation/data/adult.test.txt'
            },
            "path": 'adult-data/adult.test.txt'
        }
    ])

    # porto_seguro
    lines.extend([
        {
            'name': 'porto-seguro-train', 'category': 'dataset',
            'urls': {
                'source': 'https://raw.githubusercontent.com/1007530194/data/master/recommendation/data/porto_seguro_train.csv'
            },
            "path": 'porto-seguro/porto_seguro_train.csv'
        }, {
            'name': 'porto-seguro-test', 'category': 'dataset',
            'urls': {
                'source': 'https://raw.githubusercontent.com/1007530194/data/master/recommendation/data/porto_seguro_test.csv'
            },
            "path": 'porto-seguro/porto_seguro_test.csv'
        }
    ])

    # porto_seguro
    lines.extend([
        {
            'name': 'bitly-usagov', 'category': 'dataset',
            'urls': {
                'source': 'https://raw.githubusercontent.com/1007530194/data/master/datasets/bitly_usagov/example.txt'
            },
            "path": 'bitly-usagov/bitly_usagov_train.csv'
        }
    ])
    # coco
    lines.extend([
        {
            'name': 'coco-val2017',
            'category': 'dataset',
            'urls': {
                'source': 'http://images.cocodataset.org/zips/val2017.zip',
                'lanzou': 'https://wws.lanzous.com/b01hkb8fi'
            },
            "path": 'coco/val2017.zip'
        },
        {
            'name': 'coco-annotations_trainval2017',
            'category': 'dataset',
            'urls': {
                'source': "http://images.cocodataset.org/annotations/annotations_trainval2017.zip",
                'lanzou': 'https://wws.lanzous.com/b01hkb86j'
            },
            "path": 'coco/annotations_trainval2017.zip'
        }
    ])

    dataset = DatasetManage()
    dataset.create()
    for line in tqdm(lines):
        dataset.insert(line)
        dataset.update(line)
