# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Helper Utils for logging."""

import logging

from . import distributed_utils


class ProcessRankLoggingFilter(logging.Filter):
    """Filter to add process rank information to log records."""

    def filter(self, record):
        """ Add process rank information to the log record if running in distributed mode.
        No op otherwise.
        The information is added to the properties attribute as this attribute is merged into
        custom dimensions by log_server and is reported to AppInsights.
        (See LogRecordStreamHandler.handle_log_record in azureml.automl.core.shared.log_server)

        :param record: log record
        :type record: logging.LogRecord
        :return: Flag to indicate if this specific record has to be logged.
        :rtype: bool
        """
        if distributed_utils.dist_available_and_initialized():
            process_rank_property = {"rank": distributed_utils.get_rank()}
            if hasattr(record, "properties"):
                record.properties.update(process_rank_property)
            else:
                record.properties = process_rank_property
        return True


def get_logger(name):
    """ Get a logger object with the specified name. This function adds a ProcessRankLoggingFilter to the returned
    logger so that logs output will have rank information.

    :param name: Name of the logger.
    :type name: str
    :return: logger object.
    :rtype: logging.Logger
    """
    name_logger = logging.getLogger(name)
    name_logger.addFilter(ProcessRankLoggingFilter())
    return name_logger
