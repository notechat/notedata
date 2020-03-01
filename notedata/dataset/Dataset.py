import logging
import os
import pickle
import random

import numpy as np
import pandas as pd

from notedata.manage import DatasetManage
from notedata.manage.library import insert_adult_data, insert_porto_seguro, get_manage
from notedata.manage.library import insert_movielens, insert_bitly_usagov, insert_electronics
from notetool.tool import log, exists_file

logger = log(__name__)


def get_electronics(dataset: DatasetManage = None):
    class ElectronicsData:
        def __init__(self, dataset: DatasetManage = None, data_path=None):
            # 源文件保存目录
            self.dataset = get_manage(dataset)
            self.path_root = data_path or dataset.path_root + '/electronics/'

            # 源文件
            self.json_meta = self.path_root + '/meta_Electronics.json'
            self.json_reviews = self.path_root + '/reviews_Electronics_5.json'

            # 格式化文件
            self.pkl_meta = self.path_root + '/raw_data/meta.pkl'
            self.pkl_reviews = self.path_root + '/raw_data/reviews.pkl'

            # 结果文件
            self.pkl_remap = self.path_root + '/raw_data/remap.pkl'
            self.pkl_dataset = self.path_root + '/raw_data/dataset.pkl'

        def download_raw_0(self, overwrite=False):
            self.dataset.download('electronics-reviews', overwrite=overwrite)
            self.dataset.download('electronics-meta', overwrite=overwrite)

            logging.info("download done")
            logger.info("begin unzip file")

            os.system('cd ' + self.path_root + ' && gzip -d reviews_Electronics_5.json.gz')
            os.system('cd ' + self.path_root + ' && gzip -d meta_Electronics.json.gz')
            logging.info("unzip done")

        def convert_pd_1(self, overwrite=False):
            def to_df(file_path):
                with open(file_path, 'r') as fin:
                    df = {}
                    i = 0
                    for line in fin:
                        df[i] = eval(line)
                        i += 1
                    df = pd.DataFrame.from_dict(df, orient='index')
                    return df

            if exists_file(self.pkl_reviews, mkdir=True) and exists_file(self.pkl_meta, mkdir=True):
                return

            reviews_df = to_df(self.json_reviews)
            with open(self.pkl_reviews, 'wb') as f:
                pickle.dump(reviews_df, f, pickle.HIGHEST_PROTOCOL)

            meta_df = to_df(self.json_meta)
            meta_df = meta_df[meta_df['asin'].isin(reviews_df['asin'].unique())]
            meta_df = meta_df.reset_index(drop=True)
            with open(self.pkl_meta, 'wb') as f:
                pickle.dump(meta_df, f, pickle.HIGHEST_PROTOCOL)

        def remap_id_2(self, overwrite=False):
            random.seed(1234)
            if exists_file(self.pkl_remap, mkdir=True):
                return

            with open(self.pkl_reviews, 'rb') as f:
                reviews_df = pickle.load(f)
                reviews_df = reviews_df[['reviewerID', 'asin', 'unixReviewTime']]
            with open(self.pkl_meta, 'rb') as f:
                meta_df = pickle.load(f)
                meta_df = meta_df[['asin', 'categories']]
                meta_df['categories'] = meta_df['categories'].map(lambda x: x[-1][-1])

            def build_map(df, col_name):
                key = sorted(df[col_name].unique().tolist())
                m = dict(zip(key, range(len(key))))
                df[col_name] = df[col_name].map(lambda x: m[x])
                return m, key

            asin_map, asin_key = build_map(meta_df, 'asin')
            cate_map, cate_key = build_map(meta_df, 'categories')
            view_map, view_key = build_map(reviews_df, 'reviewerID')

            user_count, item_count, cate_count, example_count = \
                len(view_map), len(asin_map), len(cate_map), reviews_df.shape[0]
            logger.info('user_count: %d\t item_count: %d\t cate_count: %d\t example_count: %d' %
                        (user_count, item_count, cate_count, example_count))

            meta_df = meta_df.sort_values('asin')
            meta_df = meta_df.reset_index(drop=True)
            reviews_df['asin'] = reviews_df['asin'].map(lambda x: asin_map[x])
            reviews_df = reviews_df.sort_values(['reviewerID', 'unixReviewTime'])
            reviews_df = reviews_df.reset_index(drop=True)
            reviews_df = reviews_df[['reviewerID', 'asin', 'unixReviewTime']]

            cate_list = [meta_df['categories'][i] for i in range(len(asin_map))]
            cate_list = np.array(cate_list, dtype=np.int32)

            with open(self.pkl_remap, 'wb') as f:
                pickle.dump(reviews_df, f, pickle.HIGHEST_PROTOCOL)  # uid, iid
                pickle.dump(cate_list, f, pickle.HIGHEST_PROTOCOL)  # cid of iid line
                pickle.dump((user_count, item_count, cate_count, example_count),
                            f, pickle.HIGHEST_PROTOCOL)
                pickle.dump((asin_key, cate_key, view_key), f, pickle.HIGHEST_PROTOCOL)

        def build_dataset_3(self, overwrite=False):
            random.seed(1234)
            if exists_file(self.pkl_dataset, mkdir=True):
                return

            with open(self.pkl_remap, 'rb') as f:
                reviews_df = pickle.load(f)
                cate_list = pickle.load(f)
                user_count, item_count, cate_count, example_count = pickle.load(f)

            train_set = []
            test_set = []
            for reviewerID, hist in reviews_df.groupby('reviewerID'):
                pos_list = hist['asin'].tolist()

                def gen_neg():
                    neg = pos_list[0]
                    while neg in pos_list:
                        neg = random.randint(0, item_count - 1)
                    return neg

                neg_list = []
                for i in range(len(pos_list)):
                    neg_list.append(gen_neg())

                for i in range(1, len(pos_list)):
                    hist = pos_list[:i]
                    if i != len(pos_list) - 1:
                        train_set.append((reviewerID, hist, pos_list[i], 1))
                        train_set.append((reviewerID, hist, neg_list[i], 0))
                    else:
                        label = (pos_list[i], neg_list[i])
                        test_set.append((reviewerID, hist, label))

            random.shuffle(train_set)
            random.shuffle(test_set)

            assert len(test_set) == user_count

            with open(self.pkl_dataset, 'wb') as f:
                pickle.dump(train_set, f, pickle.HIGHEST_PROTOCOL)
                pickle.dump(test_set, f, pickle.HIGHEST_PROTOCOL)
                pickle.dump(cate_list, f, pickle.HIGHEST_PROTOCOL)
                pickle.dump((user_count, item_count, cate_count), f, pickle.HIGHEST_PROTOCOL)

        def init_data(self, overwrite=False):
            self.download_raw_0(overwrite=overwrite)

            self.convert_pd_1(overwrite=overwrite)

            self.remap_id_2(overwrite=overwrite)

            self.build_dataset_3(overwrite=overwrite)

    insert_electronics(dataset)
    electronic = ElectronicsData(dataset=dataset)
    electronic.init_data()


def get_movielens(dataset: DatasetManage = None):
    dataset = insert_movielens(dataset)

    # data = dataset.download('movielens-100k', overwrite=False)
    data = dataset.download('movielens-1m', overwrite=False)
    # data = dataset.download('movielens-10m', overwrite=False)
    # data = dataset.download('movielens-20m', overwrite=False)
    # data = dataset.download('movielens-25m', overwrite=False)
    # os.system('cd ' + file_path(data.path) + ' && unzip ' + file_name(data.path))


def get_adult_data(dataset: DatasetManage = None):
    dataset = insert_adult_data(dataset)
    data_train = dataset.download('adult-train', overwrite=False)
    data_test = dataset.download('adult-test', overwrite=False)

    print(data_test)
    train_data = pd.read_table(data_train.path, header=None, delimiter=',')
    test_data = pd.read_table(data_test.path, header=None, delimiter=',', error_bad_lines=False)

    # all_columns = ['age', 'workclass', 'fnlwgt', 'education', 'education-num', 'marital-status', 'occupation',
    #                'relationship', 'race', 'sex', 'capital-gain', 'capital-loss', 'hours-per-week', 'native-country',
    #                'label', 'type']
    #
    # continus_columns = ['age', 'fnlwgt', 'education-num', 'capital-gain', 'capital-loss', 'hours-per-week']
    # dummy_columns = ['workclass', 'education', 'marital-status', 'occupation', 'relationship', 'race', 'sex',
    #                  'native-country']
    #
    # train_data['type'] = 1
    # test_data['type'] = 2
    #
    # all_data = pd.concat([train_data, test_data], axis=0)
    # all_data.columns = all_columns
    #
    # all_data = pd.get_dummies(all_data, columns=dummy_columns)
    #
    # test_data = all_data[all_data['type'] == 2].drop(['type'], axis=1)
    # train_data = all_data[all_data['type'] == 1].drop(['type'], axis=1)
    #
    # train_data['label'] = train_data['label'].map(lambda x: 1 if x.strip() == '>50K' else 0)
    # test_data['label'] = test_data['label'].map(lambda x: 1 if str(x).strip() == '>50K.' else 0)
    #
    # for col in continus_columns:
    #     ss = StandardScaler()
    #     train_data[col] = ss.fit_transform(train_data[[col]].astype(np.float64))
    #     test_data[col] = ss.transform(test_data[[col]].astype(np.float64))
    #
    # train_y = train_data['label']
    # train_x = train_data.drop(['label'], axis=1)
    # test_y = test_data['label']
    # test_x = test_data.drop(['label'], axis=1)
    #
    # return train_x, train_y, test_x, test_y


def get_porto_seguro_data(dataset: DatasetManage = None):
    insert_porto_seguro(dataset)
    dataset.download('porto-seguro-train')
    dataset.download('porto-seguro-test')


def get_bitly_usagov_data(dataset: DatasetManage = None):
    insert_bitly_usagov(dataset)
    dataset.download('bitly-usagov')


data = DatasetManage()
# get_electronics(dataset=data)
get_movielens(dataset=data)
get_adult_data(data)
get_porto_seguro_data(data)
get_bitly_usagov_data(data)
