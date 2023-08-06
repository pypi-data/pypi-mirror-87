import os
import tempfile
import pytest
import sys

import azureml.contrib.automl.dnn.vision.classification.runner as runner
from azureml.contrib.automl.dnn.vision.classification.models import ModelFactory
from azureml.contrib.automl.dnn.vision.classification.inference.inference_model_wrapper import InferenceModelWrapper
from azureml.contrib.automl.dnn.vision.classification.common.constants import ArtifactLiterals

from azureml.train.automl import constants
from .run_mock import RunMock, ExperimentMock, WorkspaceMock, DatastoreMock


data_folder = 'classification_data/images'
labels_root = 'classification_data/'


def _get_settings(csv_file):
    return {
        'images_folder': '.',
        'labels_file': csv_file,
        'validation_labels_file': 'valid_labels.csv',
        'seed': 47,
        'deterministic': True,
        'num_workers': 0,
        'output_scoring': True,
        'labels_file_root': labels_root,
        'data_folder': data_folder
    }


@pytest.mark.usefixtures('new_clean_dir')
def test_score_validation_data(monkeypatch):
    def mock_score(inference_model_wrapper, run, target_path,
                   output_file, root_dir, image_list_file,
                   batch_size, ignore_data_errors, input_dataset_id,
                   num_workers):
        assert target_path.startswith('automl/datasets/')
        assert batch_size == 20
        assert input_dataset_id == val_dataset_id
        assert num_workers == 8

        data_folder = os.path.join(tmp_output_dir, 'cracks')
        expected_root_dir = os.path.join(data_folder, '.')
        assert root_dir == expected_root_dir

        with open(image_list_file, 'w') as f:
            f.write('testcontent')

    with tempfile.TemporaryDirectory() as tmp_output_dir:
        ds_mock = DatastoreMock('datastore_mock')
        ws_mock = WorkspaceMock(ds_mock)
        experiment_mock = ExperimentMock(ws_mock)
        run_mock = RunMock(experiment_mock)

        model_wrapper = ModelFactory().get_model_wrapper('seresnext', 10)
        classes = ['A'] * 10
        test_inference_model_wrapper = InferenceModelWrapper(model_wrapper, labels=classes, device='cpu')
        val_dataset_id = '123'
        image_folder = '.'
        settings = {
            'validation_batch_size': 20,
            'batch_size': 40,
            'validation_labels_file': 'test.csv',
            'labels_file_root': tmp_output_dir,
            'data_folder': os.path.join(tmp_output_dir, 'cracks'),
            'num_workers': 8
        }

        with monkeypatch.context() as m:
            m.setattr(runner, '_score_with_model', mock_score)
            runner.score_validation_data(inference_model_wrapper=test_inference_model_wrapper,
                                         azureml_run=run_mock, ignore_data_errors=True,
                                         val_dataset_id=val_dataset_id,
                                         image_folder=image_folder,
                                         settings=settings)
            expected_val_labels_file = os.path.join(tmp_output_dir, 'test.csv')
            assert os.path.exists(expected_val_labels_file)


@pytest.mark.usefixtures('new_clean_dir')
def test_binary_classification_local_run(monkeypatch):
    _test_classification_local_run(monkeypatch, 'binary_classification.csv')


@pytest.mark.usefixtures('new_clean_dir')
def test_multiclassification_local_run(monkeypatch):
    _test_classification_local_run(monkeypatch, 'multiclass.csv')


@pytest.mark.usefixtures('new_clean_dir')
def test_multilabel_local_run(monkeypatch):
    _test_classification_local_run(monkeypatch, 'multilabel.csv')


def _test_classification_local_run(monkeypatch, csv_file):
    settings = _get_settings(csv_file)

    def mock_score_validation_data(inference_model_wrapper, azureml_run, ignore_data_errors,
                                   val_dataset_id, image_folder, settings):
        # Ensures score_validation_data is called
        test_output_dir = settings['output_dir']
        predictions_file = os.path.join(test_output_dir, 'predictions.txt')
        with open(predictions_file, 'w') as f:
            f.write('test content')

    with monkeypatch.context() as m:
        with tempfile.TemporaryDirectory() as tmp_output_dir:
            m.setattr(sys, 'argv', ['runner.py', '--data-folder', data_folder, '--labels-file-root', labels_root])
            m.setattr(runner, 'score_validation_data', mock_score_validation_data)
            settings['output_dir'] = tmp_output_dir
            settings['task_type'] = constants.Tasks.IMAGE_MULTI_LABEL_CLASSIFICATION
            settings['validation_output_file'] = os.path.join(tmp_output_dir, 'predictions.txt')
            runner.run(settings, multilabel=True)
            expected_output = os.path.join(tmp_output_dir, ArtifactLiterals.MODEL_WRAPPER_PKL)
            expected_validation_output = os.path.join(tmp_output_dir, 'predictions.txt')
            assert os.path.exists(expected_output)
            assert os.path.exists(expected_validation_output)
