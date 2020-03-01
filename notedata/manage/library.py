from notedata.manage import Dataset, DatasetManage

__all__ = ['insert_iris', 'insert_electronics', 'insert_movielens', 'insert_adult_data', 'insert_porto_seguro',
           'insert_bitly_usagov', 'dataset_manage', 'dataset_manage2']


def dataset_manage2(dataset: DatasetManage = None):
    return dataset or DatasetManage()


def dataset_manage(dataset: DatasetManage = None):
    return dataset or DatasetManage()


def insert_iris(dataset: DatasetManage = None):
    dataset = dataset_manage(dataset)
    dataset.insert(
        Dataset(name='iris',
                urls='https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data',
                path='iris/iris.data'))
    return dataset


def insert_electronics(dataset: DatasetManage = None):
    dataset = dataset_manage(dataset)
    dataset.insert(
        Dataset(name='electronics-reviews',
                urls="http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Electronics_5.json.gz",
                path='electronics/reviews_Electronics_5.json.gz'))

    dataset.insert(
        Dataset(name='electronics-meta',
                urls="http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/meta_Electronics.json.gz",
                path='electronics/meta_Electronics.json.gz'))
    return dataset


def insert_movielens(dataset: DatasetManage = None):
    dataset = dataset_manage(dataset)
    dataset.insert(Dataset(name='movielens-1m',
                           urls="http://files.grouplens.org/datasets/movielens/ml-1m.zip",
                           path='movielens/ml-1m.zip'))

    dataset.insert(Dataset(name='movielens-100k',
                           urls="http://files.grouplens.org/datasets/movielens/ml-100k.zip",
                           path='movielens/ml-100k.zip'))
    dataset.insert(Dataset(name='movielens-1m',
                           urls="http://files.grouplens.org/datasets/movielens/ml-1m.zip",
                           path='movielens/ml-1m.zip'))
    dataset.insert(Dataset(name='movielens-10m',
                           urls="http://files.grouplens.org/datasets/movielens/ml-10m.zip",
                           path='movielens/ml-10m.zip'))
    dataset.insert(Dataset(name='movielens-20m',
                           urls="http://files.grouplens.org/datasets/movielens/ml-20m.zip",
                           path='movielens/ml-20m.zip'))

    dataset.insert(Dataset(name='movielens-25m',
                           urls="http://files.grouplens.org/datasets/movielens/ml-25m.zip",
                           path='movielens/ml-25m.zip'))
    return dataset


def insert_adult_data(dataset: DatasetManage = None):
    dataset = dataset_manage(dataset)

    dataset.insert(
        Dataset(name='adult-train',
                urls="https://raw.githubusercontent.com/1007530194/data/master/recommendation/data/adult.data.txt",
                path='adult-data/adult.train.txt'))
    dataset.insert(
        Dataset(name='adult-test',
                urls="https://raw.githubusercontent.com/1007530194/data/master/recommendation/data/adult.test.txt",
                path='adult-data/adult.test.txt'))
    return dataset


def insert_porto_seguro(dataset: DatasetManage = None):
    dataset = dataset_manage(dataset)

    dataset.insert(Dataset(name='porto-seguro-train',
                           urls="https://raw.githubusercontent.com/1007530194/data/master/recommendation/data/porto_seguro_train.csv",
                           path='porto-seguro/porto_seguro_train.csv'))
    dataset.insert(Dataset(name='porto-seguro-test',
                           urls="https://raw.githubusercontent.com/1007530194/data/master/recommendation/data/porto_seguro_test.csv",
                           path='porto-seguro/porto_seguro_test.csv'))
    return dataset


def insert_bitly_usagov(dataset: DatasetManage = None):
    dataset = dataset_manage(dataset)

    dataset.insert(Dataset(name='bitly-usagov',
                           urls="https://raw.githubusercontent.com/1007530194/data/master/datasets/bitly_usagov/example.txt",
                           path='bitly-usagov/bitly_usagov_train.csv'))
    return dataset
