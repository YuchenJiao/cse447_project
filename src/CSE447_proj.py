#!/usr/bin/env python
import os
import random
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter


class MyModel:
    """
    This is a starter model to get you started. Feel free to modify this file.
    """

    @classmethod
    def load_training_data(cls):
        path = 'data/train'
        file_name = os.listdir(path)[0]
        train_file = os.path.join(path, file_name)
        return train_file

    @classmethod
    def load_test_data(cls, fname):
        data = []
        with open(fname) as f:
            for line in f:
                inp = line[:-1]  # the last character is a newline
                data.append(inp)
        return data

    @classmethod
    def write_pred(cls, preds, fname):
        with open(fname, 'wt') as f:
            for p in preds:
                f.write('{}\n'.format(p))

    def run_train(self, data, work_dir):
        sentences = []
        with open(data, 'r') as f:
            sentences = f.readlines()
        
        chars = {}
        char_num = 0
        for sentence in sentences:
            for char in sentence:
                char_num += 1
                if char != '\n' and char != ' ':
                    try:
                        chars[char] = chars[char] + 1
                    except:
                        chars[char] = 1
        temp = []
        UNK_num = 0
        for char in chars.keys():
            if chars[char] < char_num * 0.00002:
                temp.append(char)
                UNK_num += chars[char]
        for char in temp:
            chars.pop(char)
        chars['UNK'] = UNK_num
        sorted_chars = reversed(sorted(chars.items(), key=lambda kv: kv[1]))
        self.train_data = sorted_chars

    def run_pred(self, data):
        preds = []
        for inp in data:
            top_guesses = "" + str(self.train_data[0][0]) + str(self.train_data[1][0]) +\
            str(self.train_data[2][0])
            preds.append(''.join(top_guesses))
        return preds

    def save(self, work_dir):
        with open(os.path.join(work_dir, 'model.checkpoint'), 'wt') as f:
            for char in self.train_data:
                f.write('{}: {}\n'.format(char[0], char[1]))

    @classmethod
    def load(cls, work_dir):
        char_list = []
        with open(os.path.join(work_dir, 'model.checkpoint')) as f:
            char_list = f.readlines()
        # chars = {}
        # for record in char_list:
        #     char, char_num = record.split(': ')
        #     chars[char] = int(char_num[:-1])
        # model = MyModel()
        chars = []
        for record in char_list:
            char, char_num = record.split(': ')
            chars.append((char, int(char_num[:-1])))
        model = MyModel()
        model.train_data = chars
        return model


if __name__ == '__main__':
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('mode', choices=('train', 'test'), help='what to run')
    parser.add_argument('--work_dir', help='where to save', default='work')
    parser.add_argument('--test_data', help='path to test data', default='example/input.txt')
    parser.add_argument('--test_output', help='path to write test predictions', default='pred.txt')
    args = parser.parse_args()

    random.seed(0)

    if args.mode == 'train':
        if not os.path.isdir(args.work_dir):
            print('Making working directory {}'.format(args.work_dir))
            os.makedirs(args.work_dir)
        print('Instatiating model')
        model = MyModel()
        print('Loading training data')
        train_data = MyModel.load_training_data()
        print('Training')
        model.run_train(train_data, args.work_dir)
        print('Saving model')
        model.save(args.work_dir)
    elif args.mode == 'test':
        print('Loading model')
        model = MyModel.load(args.work_dir)
        print('Loading test data from {}'.format(args.test_data))
        test_data = MyModel.load_test_data(args.test_data)
        print('Making predictions')
        pred = model.run_pred(test_data)
        print('Writing predictions to {}'.format(args.test_output))
        assert len(pred) == len(test_data), 'Expected {} predictions but got {}'.format(len(test_data), len(pred))
        model.write_pred(pred, args.test_output)
    else:
        raise NotImplementedError('Unknown mode {}'.format(args.mode))