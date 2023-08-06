import os
import pytest
import torch

from azureml.contrib.automl.dnn.vision.object_detection.eval.vocmap import _iou, _map_score_voc_11_point_metric, \
    _map_score_voc_auc, VocMap
from azureml.contrib.automl.dnn.vision.object_detection.data.datasets import FileObjectDetectionDatasetWrapper
from azureml.contrib.automl.dnn.vision.common.exceptions import AutoMLVisionSystemException


def setup_vocmap_object():
    data_root = "object_detection_data"
    image_root = os.path.join(data_root, "images")
    annotation_file = os.path.join(data_root, "missing_image_annotations.json")
    dataset = FileObjectDetectionDatasetWrapper(annotations_file=annotation_file,
                                                image_folder=image_root,
                                                ignore_data_errors=True)
    return VocMap(dataset)


class TestVocMap:
    def test_iou(self):
        # Zero areas should not fail
        prediction = torch.tensor([[0, 0, 0, 0]])
        gts = torch.tensor([[0, 0, 0, 0], [0, 0, 399, 299]])
        iou = _iou(prediction, gts)
        assert iou.ndim == 1
        assert iou.shape[0] == 2
        assert iou[0].item() == 0
        assert iou[1].item() == 0

        prediction = torch.tensor([[0, 0, 399, 299]])
        gts = torch.tensor([[0, 0, 399, 299], [400, 300, 399, 299]])
        iou = _iou(prediction, gts)
        assert iou.ndim == 1
        assert iou.shape[0] == 2
        assert iou[0].item() == 1
        assert iou[1].item() == 0

        prediction = torch.rand(1, 4) * 0.5
        gts = torch.rand(4, 4) * 0.5
        width = 800
        height = 600
        prediction[0, (0, 2)] *= width
        gts[:, (0, 2)] *= width
        prediction[0, (1, 3)] *= height
        gts[:, (1, 3)] *= height
        iou = _iou(prediction, gts)
        assert iou.ndim == 1
        assert iou.shape[0] == 4

    def test_map_using_11_point_metric(self):
        # Precision list and recall list should be of equal size.
        precision_list = torch.rand(10, dtype=torch.float)
        recall_list = torch.rand(5, dtype=torch.float)
        with pytest.raises(AutoMLVisionSystemException):
            _map_score_voc_11_point_metric(precision_list, recall_list)

        # Empty lists should succeed.
        precision_list = torch.tensor([], dtype=torch.float)
        recall_list = torch.tensor([], dtype=torch.float)
        _map_score_voc_11_point_metric(precision_list, recall_list)

        precision_list = torch.rand(10, dtype=torch.float)
        recall_list = torch.rand(10, dtype=torch.float)
        map_score = _map_score_voc_11_point_metric(precision_list, recall_list)
        assert map_score.ndim == 0  # Scalar value

        # recall list with duplicate values.
        recall_list = torch.arange(0.0, 1.1, 0.1, dtype=torch.float)
        recall_list, _ = torch.sort(torch.cat((recall_list, recall_list, recall_list)))
        orig_precision_list = torch.rand(11, dtype=torch.float)
        precision_list, _ = torch.sort(torch.cat((orig_precision_list, orig_precision_list, orig_precision_list)),
                                       descending=True)
        map_score = _map_score_voc_11_point_metric(precision_list, recall_list)
        # Since precision list is sorted, max precision at 11 recall points corresponding entry in orig_precision_list.
        # map score would be the average of the orig_precision_list.
        expected_map_score = orig_precision_list.sum() / orig_precision_list.nelement()
        assert round(map_score.item(), 3) == round(expected_map_score.item(), 3)

    def test_map_using_auc_metric(self):
        # Precision list and recall list should be of same shape
        precision_list = torch.rand(10, dtype=torch.float)
        recall_list = torch.rand(5, dtype=torch.float)
        with pytest.raises(AutoMLVisionSystemException):
            _map_score_voc_auc(precision_list, recall_list)

        # Recall list should be sorted in ascending order.
        precision_list = torch.rand(10, dtype=torch.float)
        recall_list = torch.arange(1.0, 0.0, -0.1, dtype=torch.float)
        with pytest.raises(AutoMLVisionSystemException):
            _map_score_voc_auc(precision_list, recall_list)

        # Empty precision and recall list
        _map_score_voc_auc(torch.tensor([]), torch.tensor([]))

        recall_list, _ = torch.sort(torch.rand(10, dtype=torch.float))
        map_score = _map_score_voc_auc(precision_list, recall_list)
        assert map_score.ndim == 0

        # Check with single recall value to verify unique recall list logic.
        recall_list = torch.zeros(10, dtype=torch.float)
        map_score = _map_score_voc_auc(precision_list, recall_list)
        assert map_score.ndim == 0

        # recall_list with duplicate values.
        recall_list = torch.arange(0.1, 1.1, 0.1, dtype=torch.float)
        recall_list, _ = torch.sort(torch.cat((recall_list, recall_list, recall_list)))
        orig_precision_list = torch.rand(10, dtype=torch.float)
        precision_list, _ = torch.sort(torch.cat((orig_precision_list, orig_precision_list, orig_precision_list)),
                                       descending=True)
        map_score = _map_score_voc_auc(precision_list, recall_list)
        assert map_score.ndim == 0
        expected_map_score = torch.sum(orig_precision_list) * 0.1
        assert round(map_score.item(), 3) == round(expected_map_score.item(), 3)

    @pytest.mark.usefixtures("new_clean_dir")
    def test_categorize_prediction(self):
        vocmap = setup_vocmap_object()

        gts = [{"image_id": "1", "bbox": [0, 0, 299, 199], "category_id": "label1", "iscrowd": False},
               {"image_id": "2", "bbox": [0, 0, 299, 199], "category_id": "label1", "iscrowd": False},
               {"image_id": "1", "bbox": [300, 200, 299, 199], "category_id": "label1", "iscrowd": False},
               {"image_id": "1", "bbox": [600, 400, 299, 199], "category_id": "label1", "iscrowd": True}]
        detected_gts = torch.zeros(len(gts), dtype=torch.uint8)

        # No image gts should return false positive.
        prediction = {"image_id": "3", "bbox": [0, 0, 299, 199], "category_id": "label1", "score": 0.5}
        result = vocmap._categorize_prediction(prediction, gts, detected_gts)
        assert result == 0

        # Prediction should match with gts from same image.
        prediction.update({"image_id": "2"})
        result = vocmap._categorize_prediction(prediction, gts, detected_gts)
        assert result == 1
        assert detected_gts[1] == 1
        prediction.update({"image_id": "1"})
        result = vocmap._categorize_prediction(prediction, gts, detected_gts)
        assert result == 1
        assert detected_gts[0] == 1

        # Prediction matching a new gt.
        prediction.update({"bbox": [300, 200, 299, 199]})
        result = vocmap._categorize_prediction(prediction, gts, detected_gts)
        assert result == 1
        assert detected_gts[2] == 1
        # Prediction matching an already detected gt should return false positive.
        result = vocmap._categorize_prediction(prediction, gts, detected_gts)
        assert result == 0

        # Prediction matching "iscrowd" should return neither false positive nor true positive
        prediction.update({"bbox": [600, 400, 299, 199]})
        result = vocmap._categorize_prediction(prediction, gts, detected_gts)
        assert result == 2

        # Prediction whose best iou match < iou threshold should return false positive
        prediction.update({"bbox": [0, 0, 149, 99]})
        result = vocmap._categorize_prediction(prediction, gts, detected_gts)
        assert result == 0

    @pytest.mark.usefixtures("new_clean_dir")
    def test_precision_recall_curve(self):
        vocmap = setup_vocmap_object()

        # Mock vocmap._label_gts and vocmap._labels
        label1 = "label1"
        label2 = "label2"
        vocmap._labels.extend([label1, label2])
        vocmap._label_gts[label1] = [
            {"image_id": "1", "bbox": [0, 0, 299, 199], "category_id": label1, "iscrowd": False},
            {"image_id": "2", "bbox": [0, 0, 299, 199], "category_id": label1, "iscrowd": False},
            {"image_id": "1", "bbox": [600, 400, 299, 199], "category_id": label1, "iscrowd": True}
        ]
        # label 2 with only "iscrowd" gts.
        vocmap._label_gts[label2] = [
            {"image_id": "1", "bbox": [0, 0, 299, 199], "category_id": label2, "iscrowd": True},
            {"image_id": "2", "bbox": [0, 0, 299, 199], "category_id": label2, "iscrowd": True},
        ]

        # Empty list of predictions
        predictions = []
        precision_list, recall_list = vocmap._precision_recall_curve(predictions, label1)
        assert precision_list.nelement() == 0
        assert recall_list.nelement() == 0

        # If there are no non crowd gts, return None
        predictions = [
            {"image_id": "1", "bbox": [0, 0, 299, 199], "category_id": label2, "score": 0.5}
        ]
        precision_list, recall_list = vocmap._precision_recall_curve(predictions, label2)
        assert precision_list is None
        assert recall_list is None

        # Should not fail due to division by 0 when true positive and false positives are zero
        predictions = [
            {"image_id": "1", "bbox": [600, 400, 299, 199], "category_id": label1, "score": 0.5}  # matches "iscrowd"
        ]
        precision_list, recall_list = vocmap._precision_recall_curve(predictions, label1)
        assert torch.all(torch.eq(precision_list, torch.tensor([0], dtype=torch.float)))
        assert torch.all(torch.eq(recall_list, torch.tensor([0], dtype=torch.float)))

        # List of predictions unsorted by score
        predictions = [
            {"image_id": "1", "bbox": [0, 0, 299, 199], "category_id": label1, "score": 0.8},  # tp
            {"image_id": "2", "bbox": [0, 0, 299, 199], "category_id": label1, "score": 0.5},  # tp
            {"image_id": "3", "bbox": [0, 0, 299, 199], "category_id": label1, "score": 0.7},  # fp due to no gts
            {"image_id": "1", "bbox": [0, 0, 149, 99], "category_id": label1, "score": 0.4},  # fp due to low iou
            # fp because prediction with higher score matched the same gt.
            {"image_id": "1", "bbox": [0, 0, 299, 199], "category_id": label1, "score": 0.6},
            {"image_id": "1", "bbox": [600, 400, 299, 199], "category_id": label1, "score": 0.9}  # matches "iscrowd"
        ]
        # Expected results corresponding to prediction categories sorted by score
        expected_recall_list = torch.tensor([0, 0.5, 0.5, 0.5, 1, 1], dtype=torch.float)
        expected_precision_list = torch.tensor([0, 1, 0.5, 1 / 3, 0.5, 0.4], dtype=torch.float)
        precision_list, recall_list = vocmap._precision_recall_curve(predictions, label1)
        assert torch.all(torch.eq(precision_list, expected_precision_list))
        assert torch.all(torch.eq(recall_list, expected_recall_list))

    @pytest.mark.usefixtures("new_clean_dir")
    def test_map_precision_recall(self):
        vocmap = setup_vocmap_object()

        # Mock vocmap._label_gts and vocmap._labels
        label1 = "label1"
        label2 = "label2"
        label3 = "label3"
        vocmap._labels.extend([label1, label2, label3])
        vocmap._label_gts[label1] = [
            {"image_id": "1", "bbox": [0, 0, 299, 199], "category_id": label1, "iscrowd": False},
            {"image_id": "2", "bbox": [0, 0, 299, 199], "category_id": label1, "iscrowd": False},
            {"image_id": "1", "bbox": [600, 400, 299, 199], "category_id": label1, "iscrowd": True}
        ]
        # label 2 with only "iscrowd" gts.
        vocmap._label_gts[label2] = [
            {"image_id": "1", "bbox": [0, 0, 299, 199], "category_id": label2, "iscrowd": True},
            {"image_id": "2", "bbox": [0, 0, 299, 199], "category_id": label2, "iscrowd": True},
        ]
        # label 3 with no gts.
        vocmap._label_gts[label3] = []

        # No gts, no predictions
        label_score = vocmap._map_precision_recall([], label3)
        assert label_score[VocMap.PRECISION] == -1.0
        assert label_score[VocMap.RECALL] == -1.0
        assert label_score[VocMap.AVERAGE_PRECISION] == -1.0
        # No non crowd gts, no predictions
        label_score = vocmap._map_precision_recall([], label2)
        assert label_score[VocMap.PRECISION] == -1.0
        assert label_score[VocMap.RECALL] == -1.0
        assert label_score[VocMap.AVERAGE_PRECISION] == -1.0

        # No gts, some predictions
        predictions = [
            {"image_id": "1", "bbox": [0, 0, 299, 199], "category_id": label3, "score": 0.5}
        ]
        label_score = vocmap._map_precision_recall(predictions, label3)
        assert label_score[VocMap.PRECISION] == 0.0
        assert label_score[VocMap.RECALL] == -1.0
        assert label_score[VocMap.AVERAGE_PRECISION] == -1.0
        # No non crowd gts, some predictions
        predictions = [
            {"image_id": "1", "bbox": [0, 0, 299, 199], "category_id": label2, "score": 0.5}
        ]
        label_score = vocmap._map_precision_recall(predictions, label2)
        assert label_score[VocMap.PRECISION] == 0.0
        assert label_score[VocMap.RECALL] == -1.0
        assert label_score[VocMap.AVERAGE_PRECISION] == -1.0

        # Has Non crowd gts, no predictions
        label_score = vocmap._map_precision_recall([], label1)
        assert label_score[VocMap.PRECISION] == -1.0
        assert label_score[VocMap.RECALL] == 0.0
        assert label_score[VocMap.AVERAGE_PRECISION] == 0.0

        # Has non crowd gts, some predictions
        predictions = [
            {"image_id": "1", "bbox": [0, 0, 299, 199], "category_id": label1, "score": 0.8},  # tp
            {"image_id": "2", "bbox": [0, 0, 299, 199], "category_id": label1, "score": 0.5},  # tp
            {"image_id": "3", "bbox": [0, 0, 299, 199], "category_id": label1, "score": 0.7},  # fp due to no gts
        ]
        label_score = vocmap._map_precision_recall(predictions, label1)
        assert label_score[VocMap.PRECISION].ndim == 0  # Scalar
        assert label_score[VocMap.PRECISION] != -1
        assert label_score[VocMap.RECALL].ndim == 0  # Scalar
        assert label_score[VocMap.RECALL] != -1
        assert label_score[VocMap.AVERAGE_PRECISION].ndim == 0  # Scalar
        assert label_score[VocMap.AVERAGE_PRECISION] != -1
