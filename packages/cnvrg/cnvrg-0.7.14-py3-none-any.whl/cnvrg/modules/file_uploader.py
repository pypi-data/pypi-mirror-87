from cnvrg.modules.cnvrg_files import CnvrgFiles
import cnvrg.helpers.param_build_helper as param_build_helper
import cnvrg.helpers.config_helper as config_helper
from cnvrg.modules.errors import CnvrgError
from cnvrg.modules.storage import storage_factory
from cnvrg.helpers.error_catcher import suppress_exception
import cnvrg.helpers.data_working_dir_helper as data_working_dir_helper
import cnvrg.helpers.apis_helper as apis_helper
import os.path
from typing import AnyStr
import cnvrg.helpers.config_helper as config_helper

# from cnvrg.modules.project import Project
import cnvrg.modules.storage as storage
from os import path, walk
import re
import time
import threading
import multiprocessing
from botocore.exceptions import ClientError
from boto3.s3.transfer import TransferConfig
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Queue, Pool, Process, Manager
from multiprocessing.pool import ThreadPool
from functools import partial
import queue
import math
from progress.bar import IncrementalBar
# mylist = [1,2,3,4,5,6,7,8]
# bar = IncrementalBar('Countdown', max = len(mylist))
# for item in mylist:
#     bar.next()
#     time.sleep(1)
# bar.finish()
storage_client = None


class FileUploader:
    def __init__(self, element=None):
        self.element = element
        global storage_client
        storage_client = storage.storage_factory(element=element)

    # def upload_multiple_files(self, files=None, files_path=None, num_processes=10, num_threads=30, commit_sha1=None):
    def upload_multiple_files(self, files=None, commit_sha1=None):
        if files is not None:
            # print(f"Starting upload of {len(files)}")
            # chunks = FileUploader._chunk_file_list(files, int(multiprocessing.cpu_count() / 2))
            chunks = FileUploader._chunk_file_list(files, math.ceil(len(files)/1000))

            # manager = Manager()
            # progress_queue = manager.Queue(3000)

            # upload_file_chunk_partial = partial(FileUploader.upload_file_chunk, progress_queue, self.element)

            progress_queue = queue.Queue(3000)
            worker_partial = partial(FileUploader.worker, progress_queue)

            for chunk in chunks:
                blob_vs = self.element.create_blob_versions(commit_sha1, chunk)
                blobs = []
                blob_ids = []
                for k, v in blob_vs["files"].items():
                    blobs.append({
                        "full_path": k,
                        "target": v["path"],
                    })
                    blob_ids.append(str(v["bv_id"]))

                thread_pool = ThreadPool()
                thread_pool.map(worker_partial, blobs)
                self.element.connect_blob_versions_to_commit(blob_ids, commit_sha1)

            # pool = Pool()
            # pool.map(upload_file_chunk_partial, chunks)


        # if files_path is not None:
        #     file_list, dir_list = FileUploader._get_files_and_dirs_recursive(files_path)
        #     print(f"Starting upload of {len(file_list)} files in {num_processes} processes")
        #     chunks = FileUploader._chunk_file_list(file_list, int(multiprocessing.cpu_count() / 2))
        #
        #     manager = Manager()
        #     progress_queue = manager.Queue(3000)
        #
        #     upload_file_chunk_partial = partial(FileUploader.upload_file_chunk, progress_queue)
        #
        #     pool = Pool()
        #     pool.map(upload_file_chunk_partial, chunks)
        #
        #     print("finished file map")

    @staticmethod
    def worker(progress_queue, file):
        try:
            # start = time.time()
            storage_client.upload_single_file(file["full_path"], file["target"])
            # print(f"time took: {time.time() - start}")
        except Exception as e:
            print("failed to upload {}".format(file["full_path"]))
            print(e)
        # progress_queue.next()
        return file

    # @staticmethod
    # def upload_file_chunk(progress_queue, element, files):
    #     files_chunks = FileUploader._chunk_file_list(files, int(files.length() / 1000))
    #
    #     worker_partial = partial(FileUploader.worker, progress_queue)
    #
    #     for chunk in files_chunks:
    #         blob_vs = element.create_blob_versions(chunk, unique_full_paths)
    #
    #         thread_pool = ThreadPool()
    #         thread_pool.map(worker_partial, blob_vs)
    #
    #     print("Finished chunk")

    @staticmethod
    def _chunk_file_list(file_list, num_chunks):
        chunks = []
        for i in range(0, num_chunks):
            chunks.append(file_list[i::num_chunks])
        return chunks

    @staticmethod
    def _get_files_and_dirs_recursive(root_dir):
        file_list = []
        dir_list = []
        for root, dirs, files in walk(root_dir, topdown=False):
            relative_root = re.sub(root_dir, "", root)
            if relative_root.startswith("/"):
                relative_root = re.sub("/", "", relative_root, count=1)
            for name in files:
                file_list.append(path.join(relative_root, name))
            for name in dirs:
                dir_list.append(path.join(relative_root, name))

        return file_list, dir_list
