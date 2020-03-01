from notedata.dataset import *
from notedata.manage import dataset_manage

data = dataset_manage()

# get_electronics(dataset=data)
get_movielens(dataset=data)
get_adult_data(data)
get_porto_seguro_data(data)
get_bitly_usagov_data(data)
