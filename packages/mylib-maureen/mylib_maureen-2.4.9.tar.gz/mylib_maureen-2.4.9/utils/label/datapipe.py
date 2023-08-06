# -*- coding:utf-8 _*-  
"""
@author: Maureen Hsu
@file: datapipe.py 
@time: 2020/05/28
"""
from __future__ import annotations
# python packages
from enum import Enum
from typing import Union, List, Optional, Tuple

# 3rd-party packages
import numpy as np
from loguru import logger

# self-defined packages
from utils.label.VOCLabel import VOCAnnotationSet
from utils.my_class import type_myclass


class Dataset(Enum):
    TRAIN = "train"
    VALIDATION = "validation"
    TEST = "test"


def get_indexes(nb_samples: int, test_split: float, val_split: float,
                is_shuffle: bool) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    indexes = np.arange(nb_samples)

    if is_shuffle:
        np.random.seed(0)
        np.random.shuffle(indexes)

    test_count = int(nb_samples * test_split)
    test_indexes = indexes[:test_count]
    indexes = indexes[test_count:]

    if is_shuffle:
        np.random.seed()
        np.random.shuffle(indexes)

    val_split = int(len(indexes) * val_split)
    val_indexes = indexes[:val_split]
    train_indexes = indexes[val_split:]

    return train_indexes, val_indexes, test_indexes


def VOCAnnotationSets(datasets: List[str], voc_dataset_class: Optional[Union[List[type_myclass], type_myclass]],
                      image_dirs: List[str]) -> VOCAnnotationSet:
    combined_voc_set = None
    for dir_, image_dir in zip(datasets, image_dirs):
        voc_set = VOCAnnotationSet(dir_,
                                   defined_classes=voc_dataset_class,
                                   image_dir=image_dir)
        if combined_voc_set is None:
            combined_voc_set = voc_set
        else:
            combined_voc_set.add_annotation(voc_set.annotations)
    return combined_voc_set


class VOCDataSubset(VOCAnnotationSet):
    @property
    def training(self) -> VOCDataSubset:
        return self._get_subset(Dataset.TRAIN)

    @property
    def testing(self) -> VOCDataSubset:
        return self._get_subset(Dataset.TEST)

    @property
    def validation(self) -> VOCDataSubset:
        return self._get_subset(Dataset.VALIDATION)

    @property
    def nb_samples(self) -> int:
        return len(self)

    def __init__(self, voc_set: VOCAnnotationSet, val_split: float = 0.1, test_split: float = 0.1,
                 is_shuffle: bool = True, balanced: bool = False):
        super().__init__()
        self.__dict__.update(voc_set.__dict__)
        self._set_indexes = {Dataset.TRAIN: np.array([]), Dataset.VALIDATION: np.array([]), Dataset.TEST: np.array([])}
        self._split_data(val_split, test_split, is_shuffle, balanced)

    def _split_data(self, val_split: float, test_split: float, is_shuffle: bool, balanced: bool) -> None:
        if val_split == 0 and test_split == 0:
            self._set_indexes[Dataset.TRAIN] = np.arange(self.nb_samples)
        else:
            if balanced:  # only valid for classification
                for klass in self.class_count:
                    class_count = self.class_count[klass]
                    train_indexes, val_indexes, test_indexes = get_indexes(class_count, test_split, val_split,
                                                                           is_shuffle)
                    arr = np.array(self.class_dict[klass])
                    self._set_indexes[Dataset.TEST] = np.append(self._set_indexes[Dataset.TEST], arr[test_indexes])
                    self._set_indexes[Dataset.VALIDATION] = np.append(self._set_indexes[Dataset.VALIDATION],
                                                                      arr[val_indexes])
                    self._set_indexes[Dataset.TRAIN] = np.append(self._set_indexes[Dataset.TRAIN], arr[train_indexes])
                    logger.info(
                        "Label {} has train: {} val: {} test: {}".format(klass, len(train_indexes), len(val_indexes),
                                                                         len(test_indexes)))

            else:
                train_indexes, val_indexes, test_indexes = get_indexes(self.nb_samples, test_split, val_split,
                                                                       is_shuffle)
                self._set_indexes[Dataset.TEST] = test_indexes
                self._set_indexes[Dataset.VALIDATION] = val_indexes
                self._set_indexes[Dataset.TRAIN] = train_indexes

            logger.info(
                f"Total nb_samples {self.nb_samples}, train: {len(self._set_indexes[Dataset.TRAIN])}, "
                f"val: {len(self._set_indexes[Dataset.VALIDATION])}, test: {len(self._set_indexes[Dataset.TEST])}")

    def _get_subset(self, subset: Dataset) -> VOCDataSubset:
        voc_set = VOCAnnotationSet(defined_classes=self.defined_classes, debug=self.debug,
                                   for_classification=self.for_classification)
        for i in self._set_indexes[Dataset(subset)]:
            voc_set.add_annotation(self.annotations[i])

        voc_split = VOCDataSubset(voc_set, 0.0, 0.0, is_shuffle=False, balanced=False)
        return voc_split
