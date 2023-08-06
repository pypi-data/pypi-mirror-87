import argparse
import os
from unittest import mock
from unittest.mock import MagicMock, patch

import pytest
import torch.utils.data as data
from azureml.core import Run, Experiment

import azureml
from azureml.contrib.automl.dnn.vision.common.dataloaders import RobustDataLoader
from azureml.contrib.automl.dnn.vision.common.utils import _merge_settings_args_defaults, _exception_handler, \
    _read_image, _pad
from azureml.contrib.automl.dnn.vision.common.exceptions import AutoMLVisionDataException


class MissingFilesDataset(data.Dataset):
    def __init__(self):
        self._labels = ['label_1', 'label_2', 'label_3']
        self._images = [1, None, 2]

    def __getitem__(self, index):
        return self._images[index], self._labels[index]

    def __len__(self):
        return len(self._labels)


class TestRobustDataLoader:
    def _test_data_loader(self, loader):
        all_data_len = 0
        for images, label in loader:
            all_data_len += images.shape[0]
        assert all_data_len == 2

    def test_robust_dataloader(self):
        dataset = MissingFilesDataset()
        dataloader = RobustDataLoader(dataset, batch_size=10, num_workers=0)
        self._test_data_loader(dataloader)


def test_config_merge():
    settings = {"a": "a_s", "b": 1, "c": "c_s"}

    parser = argparse.ArgumentParser()
    parser.add_argument('--b')
    parser.add_argument('--d')
    parser.add_argument('--f')
    args = parser.parse_args(args=["--b", "b_a", "--d", "d_a", "--f", "f_a"])

    defaults = {"b": "b_d", "d": "d_d", "g": 10}

    merged_settings = _merge_settings_args_defaults(settings, args, defaults)

    assert merged_settings["a"] == "a_s"
    assert merged_settings["b"] == 1
    assert merged_settings["c"] == "c_s"
    assert merged_settings["d"] == "d_a"
    assert merged_settings["f"] == "f_a"
    assert merged_settings["g"] == 10


@mock.patch.object(azureml._restclient.JasmineClient, '__init__', lambda x, y, z, t, **kwargs: None)
@mock.patch.object(azureml._restclient.experiment_client.ExperimentClient, '__init__', lambda x, y, z, **kwargs: None)
@mock.patch('azureml._restclient.experiment_client.ExperimentClient', autospec=True)
@mock.patch('azureml._restclient.metrics_client.MetricsClient', autospec=True)
def test_exception_handler(mock_experiment_client, mock_metrics_client):
    mock_run = MagicMock(spec=Run)
    mock_workspace = MagicMock()
    mock_run.experiment = MagicMock(return_value=Experiment(mock_workspace, "test", _create_in_cloud=False))

    @_exception_handler
    def system_error_method():
        raise RuntimeError()

    @_exception_handler
    def user_error_method():
        raise AutoMLVisionDataException()

    with patch.object(Run, 'get_context', return_value=mock_run):
        system_error_method()
        mock_run.fail.assert_called_once()
        assert mock_run.fail.call_args[1]['error_details'].error_type == 'SystemError'
        user_error_method()
        assert mock_run.fail.call_args[1]['error_details'].error_type == 'UserError'


@pytest.mark.parametrize('use_cv2', [False, True])
@pytest.mark.parametrize('image_url', ["../data/object_detection_data/images/invalid_image_file.jpg",
                                       "../data/object_detection_data/images/corrupt_image_file.png",
                                       "nonexistent_image_file.png",
                                       "../data/object_detection_data/images/000001679.png"])
def test_read_non_existing_image(use_cv2, image_url):
    image_full_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), image_url)
    img = _read_image(ignore_data_errors=True,
                      image_url=image_full_path,
                      use_cv2=use_cv2)
    if any(prefix in image_url for prefix in ['invalid', 'corrupt', 'nonexistent']):
        # PIL manages to load corrupt images
        if 'corrupt' in image_url and not use_cv2:
            return
        assert img is None, image_url
    else:
        assert img is not None, image_url


def test_pad():
    assert _pad([], 0) == []
    assert _pad([], 4) == []
    assert _pad([1], 0) == [1]
    assert _pad([1], 1) == [1]
    assert _pad([1], 4) == [1, 1, 1, 1]
    assert _pad([1, 1, 1, 1], 4) == [1, 1, 1, 1]
    assert _pad([1, 2, 3], 5) == [1, 2, 3, 1, 2]
    assert _pad([1, 2, 3, 4], 3) == [1, 2, 3, 4, 1, 2]
