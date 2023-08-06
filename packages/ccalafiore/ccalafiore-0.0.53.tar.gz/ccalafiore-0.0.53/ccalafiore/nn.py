# websites:
# https://pytorch.org/docs/stable/torchvision/transforms.html
# https://pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html#sphx-glr-beginner-blitz-cifar10-tutorial-py
# https://pytorch.org/hub/pytorch_vision_resnet/
# https://discuss.pytorch.org/t/normalize-each-input-image-in-a-batch-independently-and-inverse-normalize-the-output/23739
# https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html

import torch
import torchvision
import PIL
import math
import numpy as np
import os
import copy
from . import array as cc_array
from . import txt as cc_txt
from . import clock as cc_clock
from . import maths as cc_maths
from . import combinations as cc_combinations
from .strings import format_float_to_str as cc_strings_format_float_to_str


class Time:
    def __init__(self, range_time, level, range_shifts=None, n_shifts=None):

        if not isinstance(range_time, cc_array.IntRange):
            self.range_time = cc_array.IntRange(range_time)
        else:
            self.range_time = range_time

        self.level = level

        if range_shifts is None:
            self.range_shifts = range_shifts
            self.random_shifts = False
        else:
            self.range_shifts = cc_array.IntRange(range_shifts)
            if self.range_shifts.len < 1:
                self.random_shifts = False
                self.range_shifts = None
            else:
                self.random_shifts = True

        self.possible_shifts = None
        self.n_possible_shifts = None
        self.n_shifts = None
        self.shifts = None

        self.use_tmp_shifts = False
        self.n_tmp_shifts = None
        self.tmp_shifts = None

        if self.random_shifts:
            self.possible_shifts = self.range_shifts.to_list()
            self.n_possible_shifts = self.possible_shifts.__len__()
            if n_shifts is not None:
                self.n_shifts = n_shifts
                self.n_tmp_shifts = self.n_possible_shifts * math.ceil(self.n_shifts / self.n_possible_shifts)
                if self.n_tmp_shifts > self.n_shifts:
                    self.use_tmp_shifts = True
                    self.tmp_shifts = self.possible_shifts * math.ceil(self.n_shifts / self.n_possible_shifts)
                else:
                    self.shifts = self.possible_shifts * math.ceil(self.n_shifts / self.n_possible_shifts)

    def set_n_shifts(self, n_shifts):

        if self.random_shifts and (n_shifts is not None):
            self.n_shifts = n_shifts
            self.n_tmp_shifts = self.n_possible_shifts * math.ceil(self.n_shifts / self.n_possible_shifts)
            if self.n_tmp_shifts > self.n_shifts:
                self.use_tmp_shifts = True
                self.tmp_shifts = self.possible_shifts * math.ceil(self.n_shifts / self.n_possible_shifts)
                self.shifts = None
            else:
                self.shifts = self.possible_shifts * math.ceil(self.n_shifts / self.n_possible_shifts)

    def next_shifts(self):

        if self.random_shifts and (self.n_shifts is not None):
            if self.use_tmp_shifts:
                self.shifts = np.random.permutation(self.tmp_shifts)[:self.n_shifts]
            else:
                self.shifts = np.random.permutation(self.shifts)


class LoaderOfImageDatasetWithBalancedClassesAndClassDirectories:

    def __init__(
            self, directory_root, level_classes, n_levels_directories=None,
            conditions_directories=None, batch_size=None, n_batches=None,
            shuffle=False, time=None, transforms=None, device=None,
            return_combinations_eb=False):

        self.directory_root = directory_root
        self.level_classes = level_classes

        self.time = time

        if n_levels_directories is None:
            self.n_levels_directories = len(conditions_directories)
        elif conditions_directories is None:
            conditions_directories = [None] * self.n_levels_directories  # type: list

        self.L = self.n_levels_directories

        self.shuffle = shuffle

        if transforms is None:
            self.transforms = torchvision.transforms.Compose([torchvision.transforms.ToTensor()])
        else:
            self.transforms = transforms

        self.device = device

        self.return_combinations_eb = return_combinations_eb

        self.conditions_directories_names = [None] * self.L  # type: list
        self.n_conditions_directories = [None] * self.L  # type: list
        self.conditions_directories = [None] * self.L  # type: list

        directory_root_l = self.directory_root
        for l in range(self.L):
            self.conditions_directories_names[l] = os.listdir(directory_root_l)

            if conditions_directories[l] is None:
                self.n_conditions_directories[l] = len(self.conditions_directories_names[l])
                self.conditions_directories[l] = np.arange(self.n_conditions_directories[l])
            else:
                self.conditions_directories[l] = conditions_directories[l]
                self.n_conditions_directories[l] = len(self.conditions_directories[l])

            directory_root_l = os.path.join(directory_root_l, self.conditions_directories_names[l][0])

        if self.time is not None:
            if self.time.range_time.stop is None:
                self.time.range_time.stop = self.n_conditions_directories[self.time.level]
            self.conditions_directories[self.time.level] = (
                self.conditions_directories[self.time.level][self.time.range_time.to_slice()])
            self.n_conditions_directories[self.time.level] = len(self.conditions_directories[self.time.level])

        self.K = self.n_classes = self.n_conditions_directories[self.level_classes]
        self.V = self.n_variables = len(self.n_conditions_directories)
        self.n_samples = cc_maths.prod(self.n_conditions_directories)
        # self.n_samples = math.prod(self.n_conditions_directories)

        if batch_size is None:
            if n_batches is None:
                self.batch_size = self.n_samples
                self.n_batches = 1
            else:
                self.n_batches = n_batches
                self.batch_size = cc_maths.rint(self.n_samples / self.n_batches)
        else:
            self.batch_size = batch_size
            self.n_batches = cc_maths.rint(self.n_samples / self.batch_size)

        print('self.batch_size =', self.batch_size)
        print('self.n_samples =', self.n_samples)
        print('self.n_batches =', self.n_batches)
        print('self.time =', self.time)
        print('self.n_conditions_directories =', self.n_conditions_directories)
        # print('self.conditions_directories =', self.conditions_directories)

        if self.shuffle:
            self.batches_indexes = None
        else:
            self.batches_indexes = np.split(np.arange(self.n_samples), self.n_batches, axis=0)

        if (self.time is not None) and self.time.random_shifts:
            self.combinations_directories_no_shift = (
                cc_combinations.conditions_to_combinations(self.conditions_directories))
            self.combinations_directories = None
            # self.combinations_directories = np.copy(self.combinations_directories_no_shift)

            if self.time.n_shifts is None:
                self.time.set_n_shifts(self.n_samples)

            # self.time.next_shifts()
            # self.combinations_directories[:, self.time.level] += self.time.shifts
            self.labels = torch.tensor(
                self.combinations_directories_no_shift[slice(0, self.n_samples, 1), self.level_classes],
                dtype=torch.int64, device=self.device)

        else:
            self.combinations_directories_no_shift = None
            self.combinations_directories = (
                cc_combinations.conditions_to_combinations(self.conditions_directories))

            self.labels = torch.tensor(
                self.combinations_directories[slice(0, self.n_samples, 1), self.level_classes],
                dtype=torch.int64, device=self.device)

        # if self.return_combinations_eb:
        #     self.combinations_eb = np.empty([self.batch_size, self.L], dtype='i')
        self.labels_eb = None

        self.combinations_eb = None

        combination_directory_str_0 = [self.conditions_directories_names[l][0] for l in range(self.L)]
        directory_0 = os.path.join(self.directory_root, *combination_directory_str_0)
        image_0 = PIL.Image.open(directory_0)
        tensor_0 = self.transforms(image_0)
        # shape_sample_0 = np.asarray(tensor_0.shape)
        # self.shape_sample = shape_sample_0
        # self.shape_batch = np.empty(self.shape_sample.size + 1, self.shape_sample.dtype)
        # self.shape_batch[0] = self.batch_size
        # self.shape_batch[1:] = self.shape_sample
        # self.tensor_batch = torch.empty(tuple(self.shape_batch), dtype=tensor_0.dtype)
        shape_sample_0 = list(tensor_0.shape)
        self.shape_sample = shape_sample_0
        self.shape_batch = torch.Size(tuple([self.batch_size] + shape_sample_0))
        self.tensor_batch = torch.empty(self.shape_batch, dtype=tensor_0.dtype, device=self.device)

        self.n_dims_samples = self.shape_sample.__len__()
        self.n_dims_batch = self.n_dims_samples + 1
        self.indexes_batch = np.empty(self.n_dims_batch, dtype=object)
        self.indexes_batch[1:] = slice(0, None, 1)

        print('self.tensor_batch.shape =', self.tensor_batch.shape)
        print()

    def load_batches_e(self):

        if (self.time is not None) and self.time.random_shifts:
            self.time.next_shifts()
            self.combinations_directories = np.copy(self.combinations_directories_no_shift)
            self.combinations_directories[:, self.time.level] += self.time.shifts

        if self.shuffle:
            self.batches_indexes = np.split(np.random.permutation(self.n_samples), self.n_batches, axis=0)

        # self.n_batches = 3
        if self.return_combinations_eb:

            for b in range(self.n_batches):
                self.labels_eb = self.labels[self.batches_indexes[b]]

                self.combinations_eb = self.combinations_directories[self.batches_indexes[b], :]
                # batch_size_eb = batches_indexes_e.shape[0]
                for i in range(self.batch_size):
                    combination_directory_ebi = self.combinations_eb[i, :]
                    combination_directory_str_ebi = [
                        self.conditions_directories_names[l][combination_directory_ebi[l]]
                        for l in range(self.L)]

                    directory_ebi = os.path.join(self.directory_root, *combination_directory_str_ebi)

                    self.indexes_batch[0] = i

                    image_ebi = PIL.Image.open(directory_ebi)
                    self.tensor_batch[tuple(self.indexes_batch)] = self.transforms(image_ebi)

                yield [self.tensor_batch, self.labels_eb, self.combinations_eb]

        else:

            for b in range(self.n_batches):
                self.labels_eb = self.labels[self.batches_indexes[b]]
                # batch_size_eb = batches_indexes_e.shape[0]
                for i in range(self.batch_size):
                    combination_directory_ebi = self.combinations_directories[self.batches_indexes[b][i], :]
                    combination_directory_str_ebi = [
                        self.conditions_directories_names[l][combination_directory_ebi[l]]
                        for l in range(self.L)]
                    directory_ebi = os.path.join(self.directory_root, *combination_directory_str_ebi)
                    self.indexes_batch[0] = i

                    image_ebi = PIL.Image.open(directory_ebi)
                    self.tensor_batch[tuple(self.indexes_batch)] = self.transforms(image_ebi)

                yield [self.tensor_batch, self.labels_eb]


def train_classifier_with_early_stop(
        model, loader, criterion, optimizer, scheduler, I=20, directory_outputs=''):

    # timer = cc_clock.Timer()
    cc_timer = cc_clock.Timer()

    for key_loader_k in loader.keys():
        if key_loader_k == 'training' or key_loader_k == 'validation':
            pass
        else:
            raise ValueError('Unknown keys in loader')

    headers = [
        'Epoch', 'Unsuccessful Epochs', 'Training Loss', 'Training Accuracy',
        'Valuation Loss', 'Lowest Valuation Loss', 'Is Lower Loss',
        'Valuation Accuracy', 'Highest Valuation Accuracy', 'Is Higher Accuracy']

    n_columns = len(headers)
    new_line_stats = [None] * n_columns  # type: list

    stats = {
        'headers': {headers[k]: k for k in range(n_columns)},
        'n_columns': n_columns,
        'lines': []}

    directory_model = os.path.join(directory_outputs, 'model.pth')
    directory_model_state = os.path.join(directory_outputs, 'model_state.pth')
    directory_stats = os.path.join(directory_outputs, 'stats.csv')

    n_decimals_for_printing = 6

    best_model_wts = copy.deepcopy(model.state_dict())

    lowest_loss = math.inf
    lowest_loss_str = str(lowest_loss)
    highest_accuracy = -math.inf
    highest_accuracy_str = str(highest_accuracy)

    i = 0
    e = 0

    n_dashes = 110
    dashes = '-' * n_dashes
    print(dashes)

    while i < I:

        print('Epoch {e} ...'.format(e=e))

        stats['lines'].append(new_line_stats.copy())
        stats['lines'][e][stats['headers']['Epoch']] = e


        # Each epoch has a training and a validation phase
        # training phase
        model.train()  # Set model to training mode

        running_loss_e = 0.0
        running_corrects_e = 0

        b = 0
        # Iterate over data.
        for batch_eb, labels_eb in loader['training'].load_batches_e():

            # zero the parameter gradients
            optimizer.zero_grad()

            # forward
            # track history
            torch.set_grad_enabled(True)
            outputs = model(batch_eb)
            _, preds = torch.max(outputs, 1)
            loss_eb = criterion(outputs, labels_eb)

            # backward + optimize
            loss_eb.backward()
            optimizer.step()

            torch.set_grad_enabled(False)

            # # statistics
            # loss_float_eb = loss_eb.item()
            # # noinspection PyTypeChecker
            # corrects_eb = torch.sum(preds == labels_eb).item()
            # accuracy_eb = corrects_eb / batch_eb.shape[0]
            # loss_str_eb = cc_strings_format_float_to_str(loss_float_eb, n_decimals=n_decimals_for_printing)
            # accuracy_str_eb = cc_strings_format_float_to_str(accuracy_eb, n_decimals=n_decimals_for_printing)
            # print('Training. Epoch: {:d}. Batch {:d}. Loss: {:s}. Accuracy: {:s}.'.format(e, b, loss_str_eb, accuracy_str_eb))

            running_loss_e += loss_eb.item() * batch_eb.shape[0]
            # noinspection PyTypeChecker
            running_corrects_e += torch.sum(preds == labels_eb).item()

            b += 1

        # scheduler.step()

        loss_e = running_loss_e / loader['training'].n_samples
        accuracy_e = running_corrects_e / loader['training'].n_samples
        # loss_e = float(running_loss_e / loader['training'].n_samples)
        # accuracy_e = float(running_corrects_e / loader['training'].n_samples)

        loss_str_e = cc_strings_format_float_to_str(loss_e, n_decimals=n_decimals_for_printing)
        accuracy_str_e = cc_strings_format_float_to_str(accuracy_e, n_decimals=n_decimals_for_printing)

        print('Epoch: {:d}. Training.   Loss: {:s}. Accuracy: {:s}.'.format(e, loss_str_e, accuracy_str_e))

        stats['lines'][e][stats['headers']['Training Loss']] = loss_e
        stats['lines'][e][stats['headers']['Training Accuracy']] = accuracy_e
        # stats['Training Loss'].append(float(loss_e))
        # stats['Training Accuracy'].append(float(accuracy_e))


        # validation phase
        model.eval()  # Set model to evaluate mode

        # zero the parameter gradients
        optimizer.zero_grad()

        torch.set_grad_enabled(False)

        running_loss_e = 0.0
        running_corrects_e = 0

        b = 0
        # Iterate over data.
        for batch_eb, labels_eb in loader['validation'].load_batches_e():

            # forward
            outputs = model(batch_eb)
            _, preds = torch.max(outputs, 1)
            loss_eb = criterion(outputs, labels_eb)

            # # statistics
            # loss_float_eb = loss_eb.item()
            # # noinspection PyTypeChecker
            # corrects_eb = torch.sum(preds == labels_eb).item()
            # accuracy_eb = corrects_eb / batch_eb.shape[0]
            # loss_str_eb = cc_strings_format_float_to_str(loss_float_eb, n_decimals=n_decimals_for_printing)
            # accuracy_str_eb = cc_strings_format_float_to_str(accuracy_eb, n_decimals=n_decimals_for_printing)
            # print('Validation. Epoch: {:d}. Batch {:d}. Loss: {:s}. Accuracy: {:s}.'.format(e, b, loss_str_eb, accuracy_str_eb))

            running_loss_e += loss_eb.item() * batch_eb.shape[0]
            # noinspection PyTypeChecker
            running_corrects_e += torch.sum(preds == labels_eb).item()

            b += 1

        loss_e = running_loss_e / loader['validation'].n_samples
        accuracy_e = running_corrects_e / loader['validation'].n_samples
        # loss_e = float(running_loss_e / loader['training'].n_samples)
        # accuracy_e = float(running_corrects_e / loader['training'].n_samples)

        loss_str_e = cc_strings_format_float_to_str(loss_e, n_decimals=n_decimals_for_printing)
        accuracy_str_e = cc_strings_format_float_to_str(accuracy_e, n_decimals=n_decimals_for_printing)

        stats['lines'][e][stats['headers']['Valuation Loss']] = loss_e
        stats['lines'][e][stats['headers']['Valuation Accuracy']] = accuracy_e

        if accuracy_e > highest_accuracy:
            highest_accuracy = accuracy_e
            highest_accuracy_str = cc_strings_format_float_to_str(highest_accuracy, n_decimals=n_decimals_for_printing)

            stats['lines'][e][stats['headers']['Is Higher Accuracy']] = 1
            stats['lines'][e][stats['headers']['Highest Valuation Accuracy']] = highest_accuracy
        else:
            stats['lines'][e][stats['headers']['Is Higher Accuracy']] = 0
            stats['lines'][e][stats['headers']['Highest Valuation Accuracy']] = highest_accuracy

        if loss_e < lowest_loss:

            lowest_loss = loss_e
            lowest_loss_str = cc_strings_format_float_to_str(lowest_loss, n_decimals=n_decimals_for_printing)
            i = 0
            stats['lines'][e][stats['headers']['Is Lower Loss']] = 1
            stats['lines'][e][stats['headers']['Unsuccessful Epochs']] = i
            stats['lines'][e][stats['headers']['Lowest Valuation Loss']] = lowest_loss

            best_model_wts = copy.deepcopy(model.state_dict())  # deep copy the model
            for directory_i in [directory_model, directory_model_state, directory_stats]:
                if os.path.isfile(directory_i):
                    os.remove(directory_i)

            torch.save(model, directory_model)
            torch.save(best_model_wts, directory_model_state)

            cc_txt.lines_to_csv_file(directory_stats, stats['lines'], stats['headers'])
        else:
            i += 1
            stats['lines'][e][stats['headers']['Is Lower Loss']] = 0
            stats['lines'][e][stats['headers']['Unsuccessful Epochs']] = i
            stats['lines'][e][stats['headers']['Lowest Valuation Loss']] = lowest_loss

            if os.path.isfile(directory_stats):
                os.remove(directory_stats)
            cc_txt.lines_to_csv_file(directory_stats, stats['lines'], stats['headers'])

        print('Epoch: {:d}. Validation. Loss: {:s}. Lowest Loss: {:s}. Accuracy: {:s}. Highest Accuracy: {:s}.'.format(
            e, loss_str_e, lowest_loss_str, accuracy_str_e, highest_accuracy_str))

        print('Epoch {e} - Unsuccessful Epochs {i}.'.format(e=e, i=i))

        e += 1
        print(dashes)

    print()
    E = e

    time_training = cc_timer.get_delta_time()

    print('Training completed in {d} days {h} hours {m} minutes {s} seconds'.format(
        d=time_training.days, h=time_training.hours,
        m=time_training.minutes, s=time_training.seconds))
    print('Number of Epochs: {E:d}'.format(E=E))
    print('Lowest Validation Loss: {:s}'.format(lowest_loss_str))
    print('Highest Validation Accuracy: {:s}'.format(highest_accuracy_str))

    # load best model weights
    model.load_state_dict(best_model_wts)
    return model, stats


def test_classifier(model, criterion, loader):

    # timer = cc_clock.Timer()
    cc_timer = cc_clock.Timer()

    headers_stats = ['N_samples', *['C_' + str(v) for v in range(loader.V)], 'Loss', 'Accuracy']

    n_columns_stats = len(headers_stats)
    line_stats = [loader.n_samples, *loader.n_conditions_directories, None, None]  # type: list

    stats = {
        'headers': {headers_stats[i]: i for i in range(n_columns_stats)},
        'line': line_stats}

    headers_trials = [
        'Trial',
        'Label',
        *['Condition_' + str(v) for v in range(loader.V)],
        *['Probability_' + str(k) for k in range(loader.K)],
        'Classification',
        'Correct_Classification'
    ]

    n_columns_trials = len(headers_trials)

    trials = {
        'headers': {headers_trials[i]: i for i in range(n_columns_trials)},
        'lines': np.empty([loader.n_samples, n_columns_trials], dtype=object)}

    n_decimals_for_printing = 6

    if model.training:
        model.eval()  # Set model to evaluate mode

    torch.set_grad_enabled(False)

    running_loss_e = 0.0
    running_corrects_e = 0

    b = 0
    # Iterate over data.
    for data_eb in loader.load_batches_e():

        samples_eb, labels_eb, combinations_eb, directories_eb = data_eb

        # forward
        outputs = model(samples_eb)
        _, preds = torch.max(outputs, 1)
        loss_eb = criterion(outputs, labels_eb)
        # todo: get probabilities
        # todo: fill trials['lines']

        running_loss_e += loss_eb.item() * samples_eb.shape[0]
        # noinspection PyTypeChecker
        running_corrects_e += torch.sum(preds == labels_eb).item()

        b += 1

    loss_e = running_loss_e / loader['validation'].n_samples
    accuracy_e = running_corrects_e / loader['validation'].n_samples
    # loss_e = float(running_loss_e / loader['training'].n_samples)
    # accuracy_e = float(running_corrects_e / loader['training'].n_samples)

    loss_str_e = cc_strings_format_float_to_str(loss_e, n_decimals=n_decimals_for_printing)
    accuracy_str_e = cc_strings_format_float_to_str(accuracy_e, n_decimals=n_decimals_for_printing)

    stats['line'][stats['headers']['Loss']] = loss_e
    stats['line'][stats['headers']['Accuracy']] = accuracy_e

    print('Test. Loss: {:s}. Accuracy: {:s}.'.format(loss_str_e, accuracy_str_e))

    print()

    time_training = cc_timer.get_delta_time()

    print('Test completed in {d} days {h} hours {m} minutes {s} seconds'.format(
        d=time_training.days, h=time_training.hours,
        m=time_training.minutes, s=time_training.seconds))

    return stats, trials


def load_resnet(name_model, K=None, softmax=False, pretrained=False, device=None):

    model = load_model(name_model, pretrained=pretrained, device=None)
    if (K is None) or (K == model.fc.out_features):
        if softmax:
            model.fc = torch.nn.Sequential(model.fc, torch.nn.Softmax())
    else:
        num_ftrs = model.fc.in_features
        if softmax:
            model.fc = torch.nn.Sequential(torch.nn.Linear(num_ftrs, K), torch.nn.Softmax())
        else:
            # Here the size of each output sample is set to K.
            model.fc = torch.nn.Linear(num_ftrs, K)

    model = set_device(model, device)

    return model


def load_model(name_model, pretrained=False, device=None):
    # model = torch.hub.load('pytorch/vision:v0.6.0', 'resnet152', pretrained=True)

    # model = torchvision.models.resnet18()
    if isinstance(name_model, str):
        template_load_string = f"model = torchvision.models.{name_model:s}(pretrained=pretrained)"
    else:
        template_load_string = f"model = torchvision.models.{str(name_model):s}(pretrained=pretrained)"

    dict_globals = {'__builtins__': None}
    dict_locals = {'torchvision': torchvision, 'pretrained': pretrained}  # type: dict
    exec(template_load_string, dict_globals, dict_locals)
    model = dict_locals['model']

    model = set_device(model, device)

    return model


def set_device(tensor, device):

    if device is None:
        return tensor
    elif isinstance(device, str):
        if device != 'cpu':
            tensor = tensor.to(torch.device(device))
        return tensor
    elif isinstance(device, torch.device):
        if device.type != 'cpu':
            tensor = tensor.to(device)
        return tensor

