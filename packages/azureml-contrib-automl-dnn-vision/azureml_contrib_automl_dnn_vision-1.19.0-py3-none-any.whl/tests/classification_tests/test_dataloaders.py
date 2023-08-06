import os
import pytest
import shutil
from torchvision import transforms
from azureml.contrib.automl.dnn.vision.classification.io.read.dataloader import _get_data_loader
from azureml.contrib.automl.dnn.vision.classification.io.read.dataset_wrappers import BaseDatasetWrapper, \
    ImageFolderLabelFileDatasetWrapper
from azureml.contrib.automl.dnn.vision.common.exceptions import AutoMLVisionDataException
from azureml.contrib.automl.dnn.vision.common.utils import _pad


class DummyDataset(BaseDatasetWrapper):
    def __init__(self):
        self._priv_labels = ['label_1', 'label_2', 'label_3']
        self._data_list = [7, 7, 7, 7]
        super().__init__(labels=self._priv_labels)

    def __len__(self):
        return len(self._data_list)

    def pad(self, padding_factor):
        self._data_list = _pad(self._data_list, padding_factor)

    def item_at_index(self, idx):
        return self._data_list[idx]

    def label_at_index(self, idx):
        return self._priv_labels[idx % 3]


@pytest.mark.usefixtures('new_clean_dir')
class TestDataLoader:
    def _test_data_loader(self, loader):
        all_data_len = 0
        for images, label in loader:
            all_data_len += images.shape[0]
        assert all_data_len == 3

    def test_get_data_loader(self):
        dataset = DummyDataset()
        assert len(dataset) == 4
        dataset.pad(3)
        assert len(dataset) == 6
        dataloader = _get_data_loader(dataset, transform_fn=None, batch_size=2, num_workers=0)

        for image, label in dataloader:
            assert image.shape[0] == len(label)

    def test_robust_get_data_loader(self):
        new_path = 'classification_data/images/missingfile.jpg'
        shutil.copy('classification_data/images/crack_1.jpg', new_path)
        dataset_not_ignore = ImageFolderLabelFileDatasetWrapper(
            'classification_data/images',
            input_file='classification_data/multiclass_missing_image.csv',
            ignore_data_errors=False
        )
        dataset_ignore = ImageFolderLabelFileDatasetWrapper(
            'classification_data/images',
            input_file='classification_data/multiclass_missing_image.csv',
            ignore_data_errors=True
        )
        os.remove(new_path)
        transform_fn = transforms.ToTensor()
        with pytest.raises(AutoMLVisionDataException):
            dataloader = _get_data_loader(dataset_not_ignore, transform_fn=transform_fn,
                                          batch_size=10, num_workers=0)
            self._test_data_loader(dataloader)

        dataloader = _get_data_loader(dataset_ignore, transform_fn=transform_fn, batch_size=10, num_workers=0)
        self._test_data_loader(dataloader)
