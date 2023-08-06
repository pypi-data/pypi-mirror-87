
import urllib.request
import os
from tqdm import tqdm
import json
import random
from TrackingNet.utils import getListSequence, getDimensionSplit


class MyProgressBar():
    def __init__(self, filename):
        self.pbar = None
        self.filename = filename

    def __call__(self, block_num, block_size, total_size):
        if not self.pbar:
            self.pbar = tqdm(total=total_size, unit='iB', unit_scale=True)
            self.pbar.set_description(f"Downloading {self.filename}...")
            self.pbar.refresh()  # to show immediately the update

        self.pbar.update(block_size)


class OwnCloudDownloader():
    def __init__(self, LocalDirectory, OwnCloudServer):
        self.LocalDirectory = LocalDirectory
        self.OwnCloudServer = OwnCloudServer

    def downloadFile(self, path_local, path_owncloud, user=None, password=None, verbose=True):
        # return 0: successfully downloaded
        # return 1: HTTPError
        # return 2: unsupported error
        # return 3: file already exist locally

        if user is not None or password is not None:
            # update Password

            password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
            password_mgr.add_password(
                None, self.OwnCloudServer, user, password)
            handler = urllib.request.HTTPBasicAuthHandler(
                password_mgr)
            opener = urllib.request.build_opener(handler)
            urllib.request.install_opener(opener)

        if os.path.exists(path_local):  # check existence
            if verbose:
                print(f"{path_local} already exists")
            return 2

        try:
            try:
                if verbose:
                    urllib.request.urlretrieve(
                        path_owncloud, path_local, MyProgressBar(path_local))
                else:
                    urllib.request.urlretrieve(
                        path_owncloud, path_local)

            except urllib.error.HTTPError as identifier:
                print(identifier)
                return 1
        except:
            os.remove(path_local)
            raise
            return 2
        return 0


class TrackingNetDownloader(OwnCloudDownloader):
    def __init__(self, LocalDirectory,
                 OwnCloudServer="https://exrcsdrive.kaust.edu.sa/exrcsdrive/public.php/webdav/"):
        super(TrackingNetDownloader, self).__init__(
            LocalDirectory, OwnCloudServer)

    def downloadZippedSPLIT(self, split):

        FileLocal = os.path.join(self.LocalDirectory, split+".zip")
        FileURL = os.path.join(self.OwnCloudServer,
                               split+".zip").replace(' ', '%20')
        res = self.downloadFile(path_local=FileLocal,
                                path_owncloud=FileURL,
                                user="MAaiTPdOwiPDNlp",  # user for video HQ
                                password="TrackingNet")

    def downloadSequence(self, split, sequence, verbose=True):

        os.makedirs(os.path.join(self.LocalDirectory,
                                 split, "anno"), exist_ok=True)
        os.makedirs(os.path.join(self.LocalDirectory,
                                 split, "zips"), exist_ok=True)
        for file in [os.path.join(split, "anno", sequence+".txt"), os.path.join(split, "zips", sequence+".zip")]:
            FileLocal = os.path.join(self.LocalDirectory, file)
            FileURL = os.path.join(self.OwnCloudServer,
                                   file).replace(' ', '%20')
            # print(FileLocal)
            # print(FileURL)
            res = self.downloadFile(path_local=FileLocal,
                                    path_owncloud=FileURL,
                                    user="MAaiTPdOwiPDNlp",  # user for video HQ
                                    password="TrackingNet",
                                    verbose=verbose)

    def downloadSplit(self, split):
        listSeqence = getListSequence(split)
        t = tqdm(listSeqence, total=getDimensionSplit(split), unit='iB', unit_scale=True)
        t.set_description(f"Downloading {split}...")
        t.refresh()  # to show immediately the update
        tot_size = 0
        def downloadSequenceProc(sequence):
            split, sequence = sequence.split("/")

            s = self.downloadSequence(split, sequence, verbose=False)
            t.update(os.path.getsize(os.path.join(
                self.LocalDirectory, split, "zips", sequence+".zip")))
            # return os.path.getsize(os.path.join(
            #     self.LocalDirectory, split, "zips", sequence+".zip"))

        from multiprocessing.pool import ThreadPool as Pool
        pool_size = 5
        pool = Pool(pool_size)

        for sequence in getListSequence(split):
            pool.apply_async(downloadSequenceProc, (sequence,))

        pool.close()
        pool.join()
