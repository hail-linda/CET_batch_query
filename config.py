# about captcha image
IMAGE_HEIGHT = 100
IMAGE_WIDTH = 180
CHAR_SETS = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNPQRSTUVWXYZ'
CLASSES_NUM = len(CHAR_SETS)
CHARS_NUM = 4
# for train
RECORD_DIR = './data'
TRAIN_FILE = 'train.tfrecords'
VALID_FILE = 'valid.tfrecords'
