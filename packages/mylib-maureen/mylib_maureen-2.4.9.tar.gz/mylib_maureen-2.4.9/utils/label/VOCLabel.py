# -*- coding:utf-8 _*-  
"""
@author: Maureen Hsu
@file: label.py 
@time: 2020/02/24
"""

# python packages
# Python 3.7 introduces PEP 563: postponed evaluation of annotations.
# A module that uses the future statement from __future__ import annotations
# will store annotations as strings automatically:
from __future__ import annotations

import abc
import json
from typing import Optional, List, Union, Tuple, Dict
from collections import defaultdict

# 3rd-party packages
import cv2
import imgaug as ia
from loguru import logger

# self-defined packages
from utils import os_path
from utils.my_class import type_myclass

ANNOTATION_FOLDER_DEFAULT_NAME = "Annotations"


class VOCJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'to_dic'):
            return obj.to_dic()

        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


class VOCLabel(metaclass=abc.ABCMeta):
    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.to_dic() == other.to_dic()
        return False

    @abc.abstractmethod
    def to_dic(self):
        return NotImplemented


class VOCBbox(VOCLabel):
    @property
    def width(self) -> float:
        return self._width

    @property
    def height(self) -> float:
        return self._height

    @property
    def xmin(self) -> float:
        return self._xmin

    @xmin.setter
    def xmin(self, value: float) -> None:
        if hasattr(self, "xmax"):
            assert value < self.xmax, f"Cannot set property xmax, {value} > {self.xmax}"
        self._xmin = value
        if hasattr(self, "xmax"):
            self._width = self.xmax - self.xmin
            assert self.width > 0, f"width: {self._width} < 0"

    @property
    def x1(self) -> float:
        return self._xmin

    @property
    def x2(self) -> float:
        return self._xmax

    @property
    def y1(self) -> float:
        return self._ymin

    @property
    def y2(self) -> float:
        return self._ymax

    @property
    def xmax(self) -> float:
        return self._xmax

    @xmax.setter
    def xmax(self, value: float) -> None:
        if hasattr(self, "xmin"):
            assert value > self.xmin, f"Cannot set property xmin, {value} < {self.xmin}"
        self._xmax = value
        if hasattr(self, "xmin"):
            self._width = self.xmax - self.xmin
            assert self.width > 0, f"width: {self._width} < 0"

    @property
    def ymin(self) -> float:
        return self._ymin

    @ymin.setter
    def ymin(self, value: float) -> None:
        if hasattr(self, "ymax"):
            assert value < self.ymax, f"Cannot set property ymin, {value} > {self.ymax}"
        self._ymin = value
        if hasattr(self, "ymax"):
            self._height = self.ymax - self.ymin

    @property
    def ymax(self) -> float:
        return self._ymax

    @ymax.setter
    def ymax(self, value: float) -> None:
        self._ymax = value
        if hasattr(self, "ymin"):
            assert value > self.ymin, f"Cannot set property ymax, {value} < {self.ymin}"
            self._height = self.ymax - self.ymin

    def get_coords(self, format_: str = None) -> Union[Tuple[float, float, float, float],
                                                       Dict[str, float],
                                                       Tuple[Tuple[float, float], Tuple[float, float]]]:
        if format_ is None:
            return self.x1, self.y1, self.x2, self.y2
        elif format_ == "dict":
            return {"x1": self.x1, "y1": self.y1, "x2": self.x2, "y2": self.y2}
        else:
            return (self.x1, self.y1), (self.x2, self.y2)

    def __init__(self, *args, **kargs):
        if args is None and kargs is None:
            xmin, ymin, xmax, ymax = 0, 0, 1, 1
        elif len(kargs) == 4:
            xmin, ymin, xmax, ymax = kargs["xmin"], kargs["ymin"], kargs["xmax"], kargs["ymax"]
        elif len(args) == 4:
            xmin, ymin, xmax, ymax = args
        else:
            raise Exception("Not enough args, kargs")

        self.xmin = int(xmin)
        self.xmax = int(xmax)
        self.ymin = int(ymin)
        self.ymax = int(ymax)

    def to_dic(self, recursively: bool = True) -> Union[VOCBbox, Dict[str, float]]:
        if not recursively:
            return self
        return {"xmin": self.xmin, "ymin": self.ymin,
                "xmax": self.xmax, "ymax": self.ymax}

    def to_json_file(self, filepath: str) -> None:
        with open(filepath, "w+") as f:
            f.write(json.dumps(self.to_dic()))
        logger.debug(f"Json {filepath} exported.")

    def to_imgaug_bbox(self, label: Optional[str] = None) -> ia.BoundingBox:
        imgaug_bbox = ia.BoundingBox(x1=self.xmin, y1=self.ymin, x2=self.xmax, y2=self.ymax, label=label)
        return imgaug_bbox

    @staticmethod
    def from_imgaug_bbox(imgaug_bbox: ia.BoundingBox) -> VOCBbox:
        assert isinstance(imgaug_bbox, ia.BoundingBox)
        voc_bbox = VOCBbox(imgaug_bbox.x1, imgaug_bbox.y1, imgaug_bbox.x2, imgaug_bbox.y2)
        return voc_bbox


class VOCObject(VOCLabel):
    @property
    def truncated(self) -> bool:
        return self._truncated

    @truncated.setter
    def truncated(self, value: bool) -> None:
        assert isinstance(value, bool)
        self._truncated = value

    @property
    def difficult(self) -> bool:
        return self._difficult

    @difficult.setter
    def difficult(self, value: bool) -> None:
        assert isinstance(value, bool)
        self._difficult = value

    @property
    def defined_classes(self) -> Union[type_myclass, List[type_myclass]]:
        return self._defined_classes

    @defined_classes.setter
    def defined_classes(self, value: Union[type_myclass, List[type_myclass]]) -> None:
        self._defined_classes = value
        if value is None:
            return

        if isinstance(self.name, str):
            for defined_class in self.defined_classes:
                try:
                    self.name = defined_class.get_pair(self.name)
                    break
                except KeyError:
                    pass
        elif isinstance(self.name, list):
            for i, n in enumerate(self.name):
                try:
                    self.name[i] = self.defined_classes[i].get_pair(n)
                except KeyError:
                    pass

    @property
    def name(self) -> Union[str, List[str], type_myclass, List[type_myclass]]:
        return self._name

    @name.setter
    def name(self, value: Union[str, List[str], type_myclass, List[type_myclass]]):
        self._name = value

    @property
    def bbox(self) -> VOCBbox:
        return self._bbox

    @bbox.setter
    def bbox(self, value: Union[VOCBbox, list]) -> None:
        if isinstance(value, VOCBbox):
            self._bbox = value
        else:
            self._bbox = VOCBbox(*value)

    @property
    def x1(self) -> float:
        return self._bbox.x1

    @property
    def x2(self) -> float:
        return self._bbox.x2

    @property
    def y1(self) -> float:
        return self._bbox.y1

    @property
    def y2(self) -> float:
        return self._bbox.y2

    @property
    def score(self) -> Union[List[float], float]:
        return self._score

    @score.setter
    def score(self, value: Union[List[float], float]):
        self._score = value

    @property
    def from_annotation(self) -> VOCAnnotation:  # parent
        return self._voc_annotation

    @from_annotation.setter
    def from_annotation(self, value: VOCAnnotation):
        assert isinstance(value, VOCAnnotation) or value is None
        self._voc_annotation = value

    def __init__(self, name: Union[str, List[str], type_myclass, List[type_myclass]],
                 bbox: Union[VOCBbox, list],
                 truncated: bool = False, difficult: bool = False,
                 defined_classes: bool = None, from_annotation: bool = None,
                 score: float = 1.0):
        self.name = name
        self.bbox = bbox
        self.defined_classes = defined_classes
        self.truncated = truncated
        self.difficult = difficult
        self.from_annotation = from_annotation
        self.score = score

    def to_dic(self, recursively: bool = True) -> dict:
        if isinstance(self.name, list):
            name = [str(k) for k in self.name]
        else:
            name = str(self.name)
        return {"name": name,
                "bndbox": self.bbox.to_dic(recursively),
                "truncated": self.truncated,
                "difficult": self.difficult}

    def to_json_file(self, filepath: str) -> None:
        with open(filepath, "w+") as f:
            f.write(json.dumps(self.to_dic(recursively=True), cls=VOCJSONEncoder))
        logger.debug(f"Json {filepath} exported.")

    @staticmethod
    def load_json(j, defined_classes: Union[type_myclass, List[type_myclass]] = None,
                  from_annotation: Optional[VOCAnnotation] = None, debug: bool = True) -> VOCObject:
        bbox = VOCBbox(**j["bndbox"])
        obj = VOCObject(name=j["name"], bbox=bbox, truncated=j["truncated"], difficult=j["difficult"],
                        defined_classes=defined_classes, from_annotation=from_annotation)
        if debug:
            logger.debug(f"VOCObject loaded from {j}")
        return obj

    def to_imgaug_bbox(self) -> ia.BoundingBox:
        imgaug_bbox = ia.BoundingBox(x1=self.bbox.xmin, y1=self.bbox.ymin, x2=self.bbox.xmax, y2=self.bbox.ymax,
                                     label=self.name)
        return imgaug_bbox

    @staticmethod
    def from_imgaug_bbox(imgaug_bbox) -> VOCObject:
        assert isinstance(imgaug_bbox, ia.BoundingBox)
        bbox = VOCBbox(imgaug_bbox.x1, imgaug_bbox.y1, imgaug_bbox.x2, imgaug_bbox.y2)
        voc_obj = VOCObject(imgaug_bbox.label, bbox)
        return voc_obj


class VOCAnnotation(VOCLabel):
    @property
    def image_path(self) -> str:  # image_path
        return self._image_path

    @image_path.setter
    def image_path(self, value: str) -> None:
        self._org_image_path = value
        self._image_path = value
        if self._image_path is not None:
            self._image_path = os_path.abspath(self._image_path)
            self._org_image_path = os_path.abspath(self._org_image_path)

    @property
    def annotation_path(self) -> Union[None, str]:
        if self._annotation_path:
            return self._annotation_path
        elif self.filename and self.folder:  # default value
            return os_path.join(os_path.dirname(self.folder, full_path=True), ANNOTATION_FOLDER_DEFAULT_NAME,
                                self.filename + ".json")
        return None

    @annotation_path.setter
    def annotation_path(self, value: str) -> None:
        self._org_annotation_path = value
        self._annotation_path = value

    @property
    def filename(self) -> Union[None, str]:
        if self._annotation_path:
            return os_path.get_filename(self._annotation_path)
        if self.image_path:
            return os_path.get_filename(self.image_path)
        return None

    @property
    def folder(self) -> Union[None, str]:
        if self._folder:
            return self._folder
        if self.image_path:
            return os_path.dirname(self.image_path)
        if self.annotation_path:
            return os_path.dirname(self.annotation_path, depth=2)
        return None

    @folder.setter
    def folder(self, value) -> None:
        self._folder = value

    @property
    def objects(self) -> List[VOCObject]:
        return self._objects

    @property
    def bboxes(self) -> List[VOCBbox]:
        bboxes = [obj.bbox for obj in self.objects]
        return bboxes

    @property
    def size(self) -> tuple:
        return self._size

    @size.setter
    def size(self, value: Union[list, tuple]):
        if value:
            value_int = tuple([int(v) for v in value])
            self._size = value_int

    @property
    def segmented(self) -> bool:
        return self._segmented

    @segmented.setter
    def segmented(self, value: bool) -> None:
        self._segmented = value

    @property
    def defined_classes(self) -> Union[type_myclass, List[type_myclass]]:
        return self._defined_classes

    @property
    def from_annotation_set(self) -> VOCAnnotationSet:  # parent
        return self._from_annotation_set

    @from_annotation_set.setter
    def from_annotation_set(self, value: VOCAnnotationSet) -> None:
        self._from_annotation_set = value

    @property
    def for_classification(self) -> bool:  # parent
        return self._for_classification

    @for_classification.setter
    def for_classification(self, value: bool) -> None:
        self._for_classification = value

    @property
    def unpacked(self) -> bool:
        return self._unpacked

    def unpack(self) -> None:
        image = cv2.imread(self.image_path)
        self.size = image.shape
        self._unpacked = True

    def __init__(self, image_path=None, objects=None, annotation_path=None, from_annotation_set=None,
                 defined_classes=None, folder=None, filename=None, for_classification=False, size=None):
        # assert (image_path or (folder and filename))

        self._folder = None
        if not image_path and (folder and filename):
            image_path = os_path.join(folder, filename)

        self._objects = []
        if size:
            self._unpacked = True
        else:
            self._unpacked = False
        self.image_path = image_path
        self.size = size
        if objects:
            self.add_objects(objects)
        self.segmented = False
        self._defined_classes = defined_classes
        self.from_annotation_set = from_annotation_set
        self.annotation_path = annotation_path
        self.for_classification = for_classification

    def __len__(self) -> int:
        return len(self.objects)

    def add_objects(self, objs) -> None:
        if not isinstance(objs, list):
            objs = [objs]
        for obj in objs:
            assert isinstance(obj, VOCObject)
            self._objects.append(obj)

    def to_dic(self, recursively: bool = True) -> dict:
        if not self.size:
            size = (0, 0, 0)
        else:
            size = self.size
        if len(size) == 3:
            depth = size[2]
        else:
            depth = 1

        return {"folder": self.folder,
                "filename": os_path.basename(self.image_path),  # image filename
                "size": {"width": size[1],
                         "height": size[0],
                         "depth": depth},
                "objects": [obj.to_dic(recursively) for obj in self._objects],
                "segmented": self.segmented
                }

    def to_json_file(self, dir_: Optional[str] = None, filepath: Optional[str] = None) -> None:
        if dir_ is not None and filepath is None:
            filepath = os_path.join(dir_, self.filename)
        elif dir_ is None and filepath is None:
            filepath = self.annotation_path

        os_path.make_dir(os_path.dirname(filepath))

        with open(filepath, "w+") as f:
            f.write(json.dumps(self.to_dic(recursively=True), cls=VOCJSONEncoder))
        logger.debug(f"Json {filepath} exported.")

    @staticmethod
    def load_json(j, annotation_path: str = None,
                  defined_classes: Optional[Union[type_myclass, List[type_myclass]]] = None,
                  from_annotation_set: Optional[VOCAnnotationSet] = None,
                  debug: bool = True,
                  image_dir: Optional[str] = None) -> VOCAnnotation:
        if image_dir is not None:
            image_path = os_path.join(image_dir, j["filename"])
        else:
            image_path = os_path.join(j["folder"], j["filename"])

        # check image path exists
        if not os_path.exists(image_path):
            if annotation_path:
                exception = f"Image path {image_path} does not exist. Loading {annotation_path} failed."
            else:
                exception = f"Image path {image_path} does not exist. Loading {j} failed."
            logger.warning(exception)
            raise FileExistsError(exception)

        ann = VOCAnnotation(image_path=image_path, from_annotation_set=from_annotation_set,
                            annotation_path=annotation_path, defined_classes=defined_classes,
                            size=(j["size"]["height"], j["size"]["width"], j["size"]["depth"]))

        object_js = j["objects"]
        for object_j in object_js:
            obj = VOCObject.load_json(object_j, defined_classes=defined_classes, from_annotation=ann, debug=debug)
            ann.add_objects([obj])

        if "segmented" in j:
            ann.segmented = j["segmented"]

        if debug:
            logger.debug(f"VOC Annotation loaded from {j}")
        return ann

    @staticmethod
    def load_json_wrapper(j, queue, **kwargs):
        ann = VOCAnnotation.load_json(j, **kwargs)
        queue.put(ann)

    def to_imgaug_bbox_in_image(self) -> ia.BoundingBoxesOnImage:
        bbs = ia.BoundingBoxesOnImage([
            obj.to_imgaug_bbox() for obj in self.objects
        ], shape=self.size)
        return bbs

    def flatten(self, for_classification: bool = True) -> List[VOCAnnotation]:
        annotations = []
        for obj in self.objects:
            ann = VOCAnnotation(image_path=self.image_path, annotation_path=self.annotation_path,
                                from_annotation_set=self.from_annotation_set, defined_classes=self.defined_classes,
                                objects=[obj], for_classification=for_classification, size=self.size)
            annotations.append(ann)
        return annotations

    def read_image(self):
        if os_path.exists(self.image_path):
            image = cv2.imread(self.image_path)
        else:
            image = cv2.imread(self._org_image_path)
        if self.for_classification:
            bbox = self.objects[0].bbox
            x1, y1, x2, y2 = bbox.x1, bbox.y1, bbox.x2, bbox.y2
            if len(image.shape) == 3:
                image = image[y1:y2 + 1, x1:x2 + 1, :]
            else:
                image = image[y1:y2 + 1, x1:x2 + 1]
        return image

    def load_from_json_file(self, json_file: str) -> None:
        with open(json_file, "r") as f:
            j = json.load(f)
        self.__dict__.update(self.load_json(j, annotation_path=json_file).__dict__)


class VOCAnnotationSet(VOCLabel):
    @property
    def folder(self) -> str:
        self._folder = self.annotations[0].folder
        for annotation in self.annotations:
            if annotation.folder != self._folder:
                raise Exception("Not all annotation have same dir.")
        return self._folder

    @folder.setter
    def folder(self, value: str) -> None:
        logger.warning(f"Changing all annotations folder to {value}")
        for i, annotation in enumerate(self.annotations):
            self.annotations[i].folder = value

    @property
    def image_paths(self) -> List[str]:  # image_paths
        return self._image_paths

    @property
    def annotations(self) -> List[VOCAnnotation]:
        return self._annotations

    @property
    def defined_classes(self) -> Union[type_myclass, List[type_myclass]]:
        return self._defined_classes

    @defined_classes.setter
    def defined_classes(self, value) -> None:
        self._defined_classes = value
        if value is not None:
            for defined_class in self._defined_classes:
                for klass in list(defined_class):
                    self._class_count[defined_class][klass] = 0
                    self._class_dict[defined_class][klass] = []

    @property
    def class_count(self) -> dict:
        if not self.defined_classes:
            return self._class_count[str]
        return self._class_count

    @property
    def class_dict(self) -> dict:
        if not self.defined_classes:
            return self._class_dict[str]
        return self._class_dict

    def __len__(self):
        return len(self.annotations)

    @property
    def unpacked(self) -> bool:
        return self._unpacked

    @property
    def for_classification(self) -> bool:
        return self._for_classification

    @for_classification.setter
    def for_classification(self, value: bool) -> None:
        self._for_classification = value

    def __init__(self, dir_or_file: Optional[Union[str, List[str]]] = None,
                 defined_classes: Optional[Union[type_myclass, List[type_myclass]]] = None,
                 debug: bool = False,
                 for_classification: bool = False, image_dir: Optional[str] = None):

        self._folder = ""
        self._image_paths = []
        self._annotations = []
        self._class_count = defaultdict(lambda: defaultdict(int))
        self._class_dict = defaultdict(lambda: defaultdict(list))  # index of annotations
        self._unpacked = True
        self.for_classification = for_classification
        self.debug = debug
        self.defined_classes = defined_classes

        # load from dir or jsons or json
        if dir_or_file:
            if not os_path.exists(dir_or_file):
                raise FileNotFoundError
            if isinstance(dir_or_file, list) and all(os_path.isfile(x) for x in dir_or_file):
                self.load_from_jsons(sorted(dir_or_file), debug=debug,
                                     for_classification=for_classification, image_dir=image_dir)
            elif os_path.isdir(dir_or_file) or \
                    (isinstance(dir_or_file, list) and all(os_path.isdir(x) for x in dir_or_file)):
                if os_path.isdir(dir_or_file):
                    label_files = os_path.list_dir(dir_or_file, extension=".json", exclude_pattern="._")
                else:
                    label_files = []
                    for lf in dir_or_file:
                        label_files += os_path.list_dir(lf, extension=".json", exclude_pattern="._")
                if not label_files:
                    label_files = os_path.list_dir(os_path.join(dir_or_file, ANNOTATION_FOLDER_DEFAULT_NAME),
                                                   extension=".json", exclude_pattern="._")
                self.load_from_jsons(sorted(label_files), debug=debug, for_classification=for_classification,
                                     image_dir=image_dir)
            else:  # is file
                raise NotImplementedError
                # self.load_from_json(dir_or_file)

    def add_annotation(self, annotation: Union[List[VOCAnnotation], VOCAnnotation]) -> None:
        if not annotation:
            return
        if isinstance(annotation, list):
            for ann in annotation:
                self.add_annotation(ann)
            return

        assert isinstance(annotation, VOCAnnotation)
        self._image_paths.append(annotation.image_path)
        self._annotations.append(annotation)
        self._unpacked = self._unpacked and annotation.unpacked

        # class_count
        if not self._defined_classes:
            for obj in annotation.objects:
                if isinstance(obj.name, list):
                    for n in obj.name:
                        self._class_count[str][n] += 1
                        self._class_dict[str][n].append(len(self))

                else:
                    self._class_count[str][obj.name] += 1
                    self._class_dict[str][obj.name].append(len(self))
        else:
            for obj in annotation.objects:
                if isinstance(obj.name, list):
                    for n in obj.name:
                        self._class_count[type(n)][n] += 1
                        self._class_dict[type(n)][n].append(len(self))
                else:
                    self._class_count[type(obj.name)][obj.name] += 1
                    self._class_dict[type(obj.name)][obj.name].append(len(self))

    def to_dic(self, recursively: bool = True) -> List[dict]:
        return [annotation.to_dic(recursively) for annotation in self.annotations]

    def to_json_files(self, dir_: Optional[str] = None, filenames: Optional[List[str]] = None,
                      filepaths: Optional[List[str]] = None) -> None:
        if filenames:
            assert len(filenames) == len(self._annotations)
        assert bool(dir_) is not bool(filepaths)
        if dir_:
            os_path.make_dir(dir_)
        for i, annotation in enumerate(self._annotations):
            if dir_ and filenames:
                annotation.to_json_file(filepath=os_path.join(dir_, filenames[i]))
            elif dir_:
                annotation.to_json_file(dir_=dir_)
            else:
                annotation.to_json_file()

    def to_json_file(self, filename: str) -> None:
        with open(filename, "w+") as f:
            f.write(json.dumps(self.to_dic(recursively=True), cls=VOCJSONEncoder))
        logger.debug(f"Json {filename} exported.")

    def load_from_jsons(self, label_files: List[str], debug: bool = False, for_classification: bool = False,
                        image_dir: Optional[str] = None) -> VOCAnnotationSet:

        for label_file in label_files:
            with open(label_file, "r") as f:
                j = json.load(f)
            annotation = VOCAnnotation.load_json(j, annotation_path=label_file, from_annotation_set=self,
                                                 defined_classes=self.defined_classes, debug=debug,
                                                 image_dir=image_dir)
            if for_classification:
                if annotation:
                    annotation = annotation.flatten()
            self.add_annotation(annotation)

        logger.debug(f"Loaded {len(self)} annotations from jsons {label_files[-5:-1]}")
        return self

    def load_from_json(self, json_file: str) -> VOCAnnotationSet:
        with open(json_file, "r") as f:
            annotation_js = json.load(f)

        for annotation_j in annotation_js:
            annotation = VOCAnnotation.load_json(annotation_j, self.defined_classes, from_annotation_set=self)
            self.add_annotation(annotation)
        logger.debug(f"Loaded {len(self)} annotations from {json_file}.")
        return self

    def unpack(self) -> None:
        for ann in self.annotations:
            ann.unpack()
        self._unpacked = True
