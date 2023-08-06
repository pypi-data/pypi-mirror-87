# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Functions to write the model at the end of training."""

import os
import pickle
import shutil
import torch
import json

from ...common.constants import ArtifactLiterals
from ....common.exceptions import AutoMLVisionValidationException
from ...inference import InferenceModelWrapper


def write_model(model_wrapper, labels=None, output_dir=None,
                device=None, enable_onnx_norm=False):
    """Save a model to Artifacts.

    :param model_wrapper: Wrapper that contains model
    :type model_wrapper: azureml.contrib.automl.dnn.vision
    :param labels: list of classes
    :type labels: list
    :param output_dir: path to output directory
    :type output_dir: str
    :param device: device where model should be run (usually 'cpu' or 'cuda:0' if it is the first gpu)
    :type device: str
    :param enable_onnx_norm: enable normalization when exporting onnx
    :type enable_onnx_norm: bool
    :return: inference model wrapper object
    :rtype: inference.InferenceModelWrapper
    """
    os.makedirs(output_dir, exist_ok=True)

    # Export and save the torch onnx model.
    onnx_file_path = os.path.join(output_dir, ArtifactLiterals.ONNX_MODEL_FILE_NAME)
    model_wrapper.export_onnx_model(file_path=onnx_file_path, device=device, enable_norm=enable_onnx_norm)

    # Explicitly Save the labels to a json file.
    if labels is None:
        raise AutoMLVisionValidationException('No labels is found in dataset wrapper', has_pii=False)
    label_file_path = os.path.join(output_dir, ArtifactLiterals.LABEL_FILE_NAME)
    with open(label_file_path, 'w') as f:
        json.dump(labels, f)

    # Save PyTorch model weights
    model_location = os.path.join(output_dir, ArtifactLiterals.MODEL_FILE_NAME)
    torch.save(model_wrapper.get_state_dict(), model_location)

    if model_wrapper.distributed:
        model_wrapper.model = model_wrapper.model.module
        model_wrapper.distributed = False

    inference_model_wrapper = InferenceModelWrapper(model_wrapper, labels=labels)
    # Remove device info
    inference_model_wrapper._device = None

    # Save pickle file
    model_wrapper_location = os.path.join(output_dir, ArtifactLiterals.MODEL_WRAPPER_PKL)

    with open(model_wrapper_location, 'wb') as pickle_file:
        pickle.dump(inference_model_wrapper, pickle_file)

    # Save score and featurize script
    dirname = os.path.dirname(os.path.abspath(__file__))
    shutil.copy(os.path.join(dirname, ArtifactLiterals.SCORE_SCRIPT),
                os.path.join(output_dir, ArtifactLiterals.SCORE_SCRIPT))
    shutil.copy(os.path.join(dirname, ArtifactLiterals.FEATURIZE_SCRIPT),
                os.path.join(output_dir, ArtifactLiterals.FEATURIZE_SCRIPT))

    return inference_model_wrapper
