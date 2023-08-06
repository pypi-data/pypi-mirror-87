
import logging
from google.cloud import storage
import google.cloud.storage.blob
import io
import tensorflow as tf
from tensorflow.python.lib.io import file_io
import pandas as pd
import os

log = logging.getLogger(__name__)



##
#   -- use --
# model_file = clf.fit()
# mesh.google.gcs.write(model_file, bucket_name, path/blob_name)
#  --- ultimately
#  from mesh.modelstore import Gcs
#  Gcs(config).write(model_file|model)  # we could wrap functionality in class
#  --- pycaret
#  model = MeshModel((XGBClassifier)xgb.fit())
#  model.persist(local_path/name)
#  Gcs(config).write(model)
##


class GCS(object):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if GCS.__instance is None:
            GCS.__instance = object.__new__(cls)
            try:
                log.debug('connecting to gcs')
                cls.client = storage.Client.from_service_account_json(kwargs['service_key_filename'])
            except KeyError as e:
                print('unable to connect to gcs with service key {}'.format(kwargs['service_key_filename']))
                GCS.__instance = None
        return GCS.__instance

    def __init__(self, **kwargs):

        """
        :param service_key_filename - if not provided, the assumption is already provided
        """
        pass


def read_blob(bucket_name: str, path: str) -> google.cloud.storage.blob.Blob:
    """
    Trivial wrapper to read a blob at a path from cloud storage
    This binary is kept in memory and a BytesIO buffer is returned
    :param bucket_name: a gcs bucket name
    :param path: path within the bucket for gcs
    :return: a blob object
    """
    bucket = GCS().client.get_bucket('{}'.format(bucket_name))
    model_buffer = bucket.blob(path)
    buffer = io.BytesIO()
    model_buffer.download_to_file(buffer)
    return buffer


def read_csv_file(filename, delimiter="|"):
    with file_io.FileIO(filename, 'r') as f:
        df = pd.read_csv(f, delimiter=delimiter)
        return df


def read_csv_files(filename_pattern, delimiter):
    """
    Concatenate sharded csv files from a provided filename pattern
    :param filename_pattern: a filename pattern including a gcs location and ending in a '_*'
    :param delimiter: a csv delimiter, eg '|'
    :return: a pandas data frame
    """
    filenames = tf.io.gfile.glob(filename_pattern)
    dataframes = [read_csv_file(filename, delimiter) for filename in filenames]
    return pd.concat(dataframes)


def write_local_file(file: str, bucket_name: str, path: str):
    """
    Uploads a local file to the provided bucket
    :param bucket_name: a gcs bucket
    :param file: the location of the file in the local directory (including name)
    :param path: the desired location of the file in the provided gcs bucket
    """
    bucket = GCS().client.bucket(bucket_name)
    blob = bucket.blob(path)

    blob.upload_from_filename(file)

    print(
        "File {} uploaded to {}.".format(
            file, path
        )
    )


def write_csv(df, bucket_name, path):
    log.info('Writing to gs://{bucket_name}/{blob}'.format(bucket_name=bucket_name, blob=path))
    bucket = GCS().client.get_bucket('{}'.format(bucket_name))
    bucket.blob(path).upload_from_string(df.to_csv(index=False), 'csv')

