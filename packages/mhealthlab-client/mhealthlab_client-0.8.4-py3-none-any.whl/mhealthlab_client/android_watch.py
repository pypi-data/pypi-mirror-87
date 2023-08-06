import glob
import os
import datetime
import pandas as pd
import numpy as np
from loguru import logger
import arus
from .constants import *


class AndroidWatch:
    def __init__(self, root_folder, pid):
        self._root = root_folder
        self._pid = pid

    def _parse_session(self):
        folders = glob.glob(os.path.join(
            self._root, "*", "*"), recursive=True)
        folders = list(filter(lambda path: os.path.isdir(
            path) and SIGNALIGNER_FOLDER_NAME not in path, folders))
        folders_as_ts = list(map(AndroidWatch.folder_name_to_date, folders))
        folders_as_ts = sorted(folders_as_ts)
        self._session_st = folders_as_ts[0]
        self._session_et = folders_as_ts[-1] + datetime.timedelta(hours=1)
        return self._session_st, self._session_et

    def convert_to_actigraph(self, date_range=None, sr=50):
        self._parse_session()
        session_span = arus.plugins.signaligner.shrink_session_span(
            (self._session_st, self._session_et), date_range=date_range)
        logger.info('Session span: {}'.format(session_span))
        assert sr is not None
        filepaths = glob.glob(os.path.join(
            self._root, '*', '*', '*.sensor.csv'), recursive=True)
        filepaths = list(
            filter(lambda f: SIGNALIGNER_FOLDER_NAME not in f, filepaths))
        sensor_type = arus.mh.parse_sensor_type_from_filepath(
            filepaths[0])
        data_id = sensor_type + '-' + 'AccelerometerCalibrated'
        sub_session_markers = arus.plugins.signaligner.auto_split_session_span(
            session_span, 'W-SUN')
        logger.debug(sub_session_markers)
        for i in range(len(sub_session_markers) - 1):
            sub_session_span = sub_session_markers[i:i + 2]
            st_display = sub_session_span[0].strftime('%Y%m%d%H')
            et_display = sub_session_span[1].strftime('%Y%m%d%H')
            logger.info(
                f'Process sub session: {st_display} - {et_display} based on W-SUN')

            # set output file paths
            output_path = os.path.join(
                self._root, SIGNALIGNER_FOLDER_NAME, f'{st_display}_{et_display}_sensors', f'{self._pid}_Android_{data_id}_{st_display}_{et_display}.sensor.csv')
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            output_annotation_path = os.path.join(os.path.dirname(
                output_path.replace('sensors', 'labelsets')), f'{self._pid}_missing_{data_id}_{st_display}_{et_display}.annotation.csv')
            os.makedirs(os.path.dirname(
                output_annotation_path), exist_ok=True)
            arus.plugins.signaligner.signify_sensor_files(
                filepaths, data_id, output_path, output_annotation_path, sub_session_span, sr)

    @staticmethod
    def folder_name_to_date(folder_name):
        hour = os.path.basename(folder_name).split('-')[0]
        date = os.path.basename(os.path.dirname(folder_name))
        date_parts = date.split('-')
        ts = datetime.datetime(int(date_parts[0]), int(date_parts[1]),
                               int(date_parts[2]), int(hour), 0, 0, 0)
        return ts


if __name__ == "__main__":
    watch = AndroidWatch('D:/datasets/sample_watch_data/P1', 'P1')
    watch.convert_to_actigraph(sr=50, date_range=['', '2010-06-11'])
