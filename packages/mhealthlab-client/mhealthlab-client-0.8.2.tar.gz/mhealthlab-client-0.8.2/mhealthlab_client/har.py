from .constants import *
from glob import glob
from loguru import logger
import arus_muss as muss
import arus
import os


class Har:
    def __init__(self, root):
        self._root = root

    def check_exists(self):
        self._sg_folder = os.path.join(self._root, SIGNALIGNER_FOLDER_NAME)
        if len(glob(os.path.join(self._sg_folder, '**', '*.sensor.csv'), recursive=True)) > 0:
            return True
        else:
            return False

    def run_har(self, task):
        if not self.check_exists():
            logger.error(
                "Please convert watch files to signaligner format at first using this script before running har.")
            exit(1)
        if task in ['intensity', 'activity', 'posture']:
            test_files = glob(os.path.join(
                self._sg_folder, '*', '*.sensor.csv'))
            for test_file in test_files:
                logger.info(f'Running {task} model on file: {test_file}')
                model_path = self._get_model_path(task)
                predict_df = muss.cli.predict_on_files(
                    model_path, [test_file], ['NDW'], srs=None, file_format='SIGNALIGNER')
                output_path = test_file.replace(
                    'sensors', task).replace('sensor', task)
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                arus.plugins.signaligner.save_as_signaligner(
                    predict_df, output_path, arus.plugins.signaligner.FileType.ANNOTATION, labelset=task, mode='w', index=False, header=True)
                logger.info(f'Saved predictions to {output_path}')
        else:
            logger.error(f"The given task {task} is not supported.")
            exit(1)

    def _get_model_path(self, task):
        if task == 'intensity':
            task = task.upper()
        else:
            task = task + '_validated'
            task = task.upper()
        name = muss.MUSSHARModel.build_model_filename(
            muss.MUSSHARModel.name, placements=['NDW'], pids=None, target=task, dataset_name='SPADES_LAB')
        return os.path.join(muss.cli.BUILTIN_DIR, name)
