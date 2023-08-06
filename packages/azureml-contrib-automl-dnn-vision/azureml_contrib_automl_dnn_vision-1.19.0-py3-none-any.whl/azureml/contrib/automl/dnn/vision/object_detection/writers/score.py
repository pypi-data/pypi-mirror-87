# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Functions for inference using a trained model"""
import os
import time
import torch

from azureml.contrib.automl.dnn.vision.common.dataloaders import RobustDataLoader
from azureml.contrib.automl.dnn.vision.common.labeled_dataset_helper import AmlLabeledDatasetHelper
from azureml.contrib.automl.dnn.vision.common.logging_utils import get_logger
from azureml.contrib.automl.dnn.vision.common.prediction_dataset import PredictionDataset
from azureml.contrib.automl.dnn.vision.common.utils import _data_exception_safe_iterator, log_end_scoring_stats
from azureml.contrib.dataset.labeled_dataset import _LabeledDatasetFactory
from azureml.core.run import Run, _OfflineRun

from ..common.constants import ScoringParameters
from ..trainer.train import move_images_to_device
from ...common.average_meter import AverageMeter
from ...common.system_meter import SystemMeter
from ...common.constants import ScoringLiterals

from ..common.object_detection_utils import _fetch_model_from_artifacts, \
    _write_prediction_file_line, _write_dataset_file_line, _validate_score_run

logger = get_logger(__name__)


def _score_with_model(model_wrapper, run, target_path, output_file, root_dir,
                      image_list_file, batch_size=1,
                      ignore_data_errors=True,
                      labeled_dataset_factory=_LabeledDatasetFactory,
                      labeled_dataset_file="labeled_dataset.json",
                      input_dataset_id=None, always_create_dataset=False,
                      num_workers=None, validate_score=False):
    if output_file is None:
        output_file = os.path.join(ScoringLiterals.DEFAULT_OUTPUT_DIR,
                                   ScoringLiterals.PREDICTION_FILE_NAME)

    model = model_wrapper.model
    classes = model_wrapper.classes
    model.eval()

    score_start = time.time()
    ws = None if isinstance(run, _OfflineRun) else run.experiment.workspace
    model_wrapper.disable_model_transform()

    logger.info("Building the prediction dataset")
    dataset = PredictionDataset(root_dir=root_dir, image_list_file=image_list_file,
                                transforms=model_wrapper.get_inference_transform(),
                                ignore_data_errors=ignore_data_errors,
                                input_dataset_id=input_dataset_id, ws=ws)

    dataloader = RobustDataLoader(dataset, batch_size=batch_size,
                                  collate_fn=dataset.collate_function,
                                  num_workers=num_workers)

    batch_time = AverageMeter()
    end = time.time()
    system_meter = SystemMeter()

    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    model.to(device)

    logger.info("Starting the inference")

    with torch.no_grad():
        try:
            with open(output_file, "w") as fw, open(labeled_dataset_file, "w") as ldsf:
                # count number of lines written to prediction
                prediction_num_lines = 0
                for i, (filenames, image_batch) in enumerate(_data_exception_safe_iterator(iter(dataloader))):
                    image_batch = move_images_to_device(image_batch, device)
                    labels = model(image_batch)

                    for filename, label, image in zip(filenames, labels, image_batch):
                        prediction_num_lines += 1
                        # Extract image shape
                        image_shape = (image.shape[1], image.shape[2])
                        _write_prediction_file_line(fw, filename, label, image_shape, classes)
                        _write_dataset_file_line(ldsf, filename,
                                                 label, image_shape, classes)

                    batch_time.update(time.time() - end)
                    end = time.time()
                    if i % 100 == 0 or i == len(dataloader) - 1:
                        mesg = "Epoch: [{0}/{1}]\t" "Time {batch_time.value:.4f}" \
                               " ({batch_time.avg:.4f})\t".format(i, len(dataloader), batch_time=batch_time)
                        mesg += system_meter.get_gpu_stats()
                        logger.info(mesg)
                        system_meter.log_system_stats(True)

                logger.info("Number of lines written to prediction file: {}".format(prediction_num_lines))

            if always_create_dataset or input_dataset_id is not None:
                datastore = ws.get_default_datastore()
                AmlLabeledDatasetHelper.create(run, datastore, labeled_dataset_file, target_path,
                                               'ObjectDetection', labeled_dataset_factory)

        finally:
            os.remove(labeled_dataset_file)

    # measure total scoring time
    score_time = time.time() - score_start
    log_end_scoring_stats(score_time, batch_time, system_meter)

    # Begin validation if flag is passed
    if validate_score:
        _validate_score_run(input_dataset_id=input_dataset_id, workspace=ws,
                            output_file=output_file, score_run=run)


def score(training_run_id, experiment_name=None, output_file=None, root_dir=None,
          image_list_file=None, batch_size=1, ignore_data_errors=True,
          output_dataset_target_path=None, input_dataset_id=None,
          validate_score=False, **model_settings):
    """Load model and infer on new data.

    :param training_run_id: Name of the training run to load model from
    :type training_run_id: String
    :param experiment_name: Name of experiment to load model from
    :type experiment_name: String
    :param output_file: Name of file to write results to
    :type output_file: String
    :param root_dir: prefix to be added to the paths contained in image_list_file
    :type root_dir: str
    :param image_list_file: path to file containing list of images
    :type image_list_file: str
    :batch_size: Inference batch size
    :type batch_size: Int
    :param ignore_data_errors: boolean flag on whether to ignore input data errors
    :type ignore_data_errors: bool
    :param output_dataset_target_path: path on Datastore for the output dataset files.
    :type output_dataset_target_path: str
    :param input_dataset_id: The input dataset id.  If this is specified image_list_file is not required.
    :type input_dataset_id: str
    :param validate_score: boolean flag on whether to validate the score
    :type validate_score: bool
    :param model_settings: Optional keyword arguments to define model specifications
    :type model_settings: Dictionary
    """
    logger.info("[start prediction: batch_size: {}]".format(batch_size))
    system_meter = SystemMeter(log_static_sys_info=True)
    system_meter.log_system_stats()

    model_wrapper = _fetch_model_from_artifacts(training_run_id, experiment_name, **model_settings)
    logger.info("Model restored successfully")

    current_scoring_run = Run.get_context()

    if output_dataset_target_path is None:
        output_dataset_target_path = AmlLabeledDatasetHelper.get_default_target_path()

    num_workers = ScoringParameters.DEFAULT_NUM_WORKERS

    _score_with_model(model_wrapper, current_scoring_run,
                      output_dataset_target_path,
                      output_file=output_file,
                      root_dir=root_dir,
                      image_list_file=image_list_file,
                      batch_size=batch_size,
                      ignore_data_errors=ignore_data_errors,
                      input_dataset_id=input_dataset_id,
                      num_workers=num_workers,
                      validate_score=validate_score)
