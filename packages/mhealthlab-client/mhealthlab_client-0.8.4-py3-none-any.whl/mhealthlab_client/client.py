
import enum
import os
from tqdm import tqdm
from loguru import logger
import pyzipper
import glob
import pysftp
import pkg_resources
import shutil
import arus
import functools
import datetime
import re


class Client:
    class Status(enum.Enum):
        DISCONNECTED = enum.auto()
        CONNECTED = enum.auto()

    def __init__(self):
        self._hostname = 'wockets.ccs.neu.edu'
        self._username = 'sftpuser'
        self._password = 'mHealth@NEU'
        self._status = Client.Status.DISCONNECTED
        self._data_folder = '.'
        self._studies = ['MICROT', 'LML']
        self._client = None

    def connect(self, pwd):
        try:
            extra_known_hosts = pkg_resources.resource_filename(
                'mhealthlab_client', 'known_hosts')
            cnopts = pysftp.CnOpts(knownhosts=extra_known_hosts)
            self._client = pysftp.Connection(host=self._hostname,
                                             username=self._username,
                                             password=pwd,
                                             cnopts=cnopts)
        except Exception as e:
            logger.error("Failed to connect to the server via SFTP.")
            logger.error(e)
            exit(1)
        self._status = Client.Status.CONNECTED
        logger.info('Connected to the server')

    def validate_study_name(self, study_name):
        if study_name not in self._studies:
            logger.error('Study name is not supported: {}', study_name)
            return False
        return True

    def validate_participant_name(self, project, pid):
        found = len(self.find_participants(project, pid)) > 0
        if found:
            return True
        else:
            logger.error(f"Participant {pid} is not found for study {project}")
            return False

    def get_participants(self, project):
        assert self._status == Client.Status.CONNECTED
        with self._client.cd(f'./{project}'):
            participants = self._client.listdir()
        return participants

    def find_participants(self, project, keyword):
        participants = self.get_participants(project)
        pids = list(filter(lambda pid: keyword in pid, participants))
        return pids

    def download_all(self, project, to, pwd=None, date_range=None):
        folder = os.path.join(self._data_folder, project)
        self._download(folder, to, date_range)
        if pwd is None:
            return
        else:
            failed_files = self._decrypt(to, pwd)

            if failed_files is not None:
                logger.error("Failed to decrypt these files: ")
                for f, e in failed_files:
                    logger.error('{}, {}', f, e)
            else:
                logger.info("All files are decrypted successfully")

    def decrypt_all(self, to, pwd):
        failed_files = self._decrypt(to, pwd)
        if failed_files is not None:
            logger.error("Failed to decrypt these files: ")
            for f, e in failed_files:
                logger.error('{}, {}', f, e)
        else:
            logger.info("All files are decrypted successfully")

    def download_by_participant(self, project, pid, to, pwd=None, date_range=None):
        # Must use '/' because this is the path for the remote server
        folder = self._data_folder + '/' + project + '/' + pid
        root = to
        to = os.path.join(to, pid)
        n_files = self._download(folder, to, date_range)
        if pwd is None:
            return
        else:
            failed_files = self._decrypt(to, pwd)

            if failed_files is not None:
                logger.error("Failed to decrypt these files: ")
                n_failed = len(failed_files)
                badzip_log_file = os.path.join(
                    root, f'{pid}_badzip_{n_failed}-{n_files}.log')
                if os.path.exists(badzip_log_file):
                    os.remove(badzip_log_file)
                handle_id = logger.add(badzip_log_file)
                for f, e in failed_files:
                    logger.error('{}, {}', f, e)
                logger.remove(handle_id)
            else:
                logger.info("All files are decrypted successfully")

            # merge residuals
            self._merge_residuals(to)

    def decrypt_by_participant(self, pid, to, pwd):
        root = to
        to = os.path.join(to, pid)
        failed_files = self._decrypt(to, pwd)

        if failed_files is not None:
            logger.error("Failed to decrypt these files: ")
            n_failed = len(failed_files)
            badzip_log_file = os.path.join(
                root, f'{pid}_badzip_{n_failed}.log')
            if os.path.exists(badzip_log_file):
                os.remove(badzip_log_file)
            handle_id = logger.add(badzip_log_file)
            for f, e in failed_files:
                logger.error('{}, {}', f, e)
            logger.remove(handle_id)
        else:
            logger.info("All files are decrypted successfully")

        # merge residuals
        self._merge_residuals(to)

    def _merge_residuals(self, to, progress_bar=True):
        local_files = glob.glob(os.path.join(
            to, '**', '*.zip.done'), recursive=True)
        residual_files = list(filter(lambda f: "_" in os.path.basename(
            f.replace('.zip.done', '')), local_files))
        n = len(residual_files)
        if progress_bar:
            bar = tqdm(total=n)
        for f in residual_files:
            folder_path = f.replace('.zip.done', '')
            if progress_bar:
                bar.update()
                bar.set_description(f'Merging residual: {folder_path}')
            ts = os.path.basename(folder_path).split('_')[1]
            dest_path = os.path.join(os.path.dirname(
                folder_path), os.path.basename(folder_path).split('_')[0])
            self._recursive_merge(folder_path, dest_path, ts=ts)
            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)
        if progress_bar:
            bar.close()

    def _recursive_merge(self, src, dest, ts):
        def rreplace(s, old, new, occurrence):
            li = s.rsplit(old, occurrence)
            return new.join(li)

        if os.path.isdir(src):
            os.makedirs(dest, exist_ok=True)
            files = os.listdir(src)
            for f in files:
                self._recursive_merge(os.path.join(src, f),
                                      os.path.join(dest, f), ts)
        else:
            if os.path.isfile(dest):
                # already exist, create a new file
                dest = rreplace(dest, ".", f".{ts}.", 1)
            if os.path.exists(src):
                shutil.copyfile(src, dest)

    def _decrypt_file(self, f, to, pwd):
        ref = None
        try:
            ref = pyzipper.AESZipFile(
                f, mode='r', compression=pyzipper.ZIP_DEFLATED)
            os.makedirs(to, exist_ok=True)
            try:
                ref.extractall(to)
            except RuntimeError as e:
                ref.extractall(to, pwd=pwd)
            except Exception as e:
                ref.extractall(to, pwd=pwd)
            ref.close()
            if os.path.dirname(f) != to:
                failed_files = self._decrypt(to, pwd, progress_bar=False)
                if failed_files is not None:
                    return failed_files
                else:
                    return None
            else:
                return None
        except Exception as e:
            if ref is not None:
                ref.close()
            if e is not None:
                return f, e
            else:
                return f, ""

    def _decrypt(self, folder, pwd, progress_bar=True):
        local_files = glob.glob(os.path.join(
            folder, '**', '*.zip'), recursive=True)
        n = len(local_files)
        if progress_bar:
            bar = tqdm(total=n)
        failed_files = []
        for f in local_files:
            if os.path.basename(f).count('.') > 1:
                to = os.path.dirname(f)
            else:
                to = os.path.join(os.path.dirname(
                    f), os.path.basename(f).split('.')[0])
            result = self._decrypt_file(f, to, pwd)
            if result is not None:
                if type(result) is list:
                    failed_files += result
                else:
                    failed_files.append(result)
            else:
                os.remove(f)
                # create an empty file as a marker indicating that this zip file has been decrypted.
                with open(f + '.done', 'w'):
                    pass
            if progress_bar:
                bar.update()
                bar.set_description(f'Decrypting {f}')
        if progress_bar:
            bar.close()
        if len(failed_files) == 0:
            return None
        return failed_files

    def _get_files(self, folder, date_range=None):
        files = []
        logger.info(
            'Analyzing the total amount of files to be downloaded for this participant...')
        local_index = './index.txt'
        self._client.get(folder + '/index.txt', local_index)
        with open(local_index, 'r') as index:
            files = index.readlines()
        files = [f.strip().replace('/srv', '.') for f in files]
        filtered_files = self._filter_files_by_dates(
            files, date_range=date_range)
        if date_range is None:
            logger.info(
                f'Found {len(filtered_files)} files.')
        elif len(date_range) == 1:
            logger.info(
                f'Found {len(filtered_files)} files with start date: {date_range[0]}.'
            )
        elif len(date_range) == 2:
            logger.info(
                f'Found {len(filtered_files)} files with start date: {date_range[0]} and stop date: {date_range[1]}.'
            )
        os.remove(local_index)
        return filtered_files

    def _download(self, folder, to, date_range=None):
        assert self._status == Client.Status.CONNECTED
        files = self._get_files(folder, date_range)
        n = len(files)
        bar = tqdm(total=n)
        for f in files:
            local = f.replace(folder, to)
            local_name = os.path.basename(local).replace(':', '')
            local = os.path.join(os.path.dirname(local), local_name)
            if os.path.exists(local) or os.path.exists(local + '.done'):
                bar.update()
                bar.set_description(f"File {local} was already downloaded.")
                continue
            os.makedirs(os.path.dirname(local), exist_ok=True)
            self._client.get(f, local)
            bar.update()
            bar.set_description(f'Downloaded file: {local}')
        bar.close()
        return n

    def _filter_files_by_dates(self, files, date_range=None):
        if date_range is None:
            return files
        else:
            start_date, stop_date = Client.parse_date_range(date_range)
            filter_fn = functools.partial(Client.filter_by_date,
                                          start_date=start_date, stop_date=stop_date)
            filtered = list(filter(filter_fn, files))
            return filtered

    @staticmethod
    def extract_participant_list(filepath):
        with open(filepath, mode='r') as f:
            pids = f.readlines()
        pids = list(map(lambda pid: pid.strip('\n'), pids))
        return pids

    @staticmethod
    def parse_date_range(date_range):
        if date_range is None:
            start_date = datetime.datetime.strptime("1970-01-01", '%Y-%m-%d')
            stop_date = datetime.datetime.strptime("2100-12-31", '%Y-%m-%d')
        elif len(date_range) == 1:
            start_date = datetime.datetime.strptime(date_range[0], '%Y-%m-%d')
            stop_date = datetime.datetime.strptime("2100-12-31", '%Y-%m-%d')
        elif len(date_range) == 2:
            if date_range[0] == '':
                stop_date = datetime.datetime.strptime(
                    date_range[1], '%Y-%m-%d')
                start_date = datetime.datetime.strptime(
                    "1970-01-01", '%Y-%m-%d')
            else:
                start_date = datetime.datetime.strptime(
                    date_range[0], '%Y-%m-%d')
                stop_date = datetime.datetime.strptime(
                    date_range[1], '%Y-%m-%d')
        return start_date, stop_date

    @staticmethod
    def filter_by_date(filepath, start_date, stop_date):
        if 'index.txt' in filepath:
            return False
        pattern = re.compile('[0-9]{4}-[0-9]{2}-[0-9]{2}')
        date_str = pattern.findall(filepath)
        if len(date_str) >= 1:
            file_date = datetime.datetime.strptime(date_str[0], '%Y-%m-%d')
            if file_date >= start_date and file_date <= stop_date:
                return True
            else:
                return False
        else:
            return True
