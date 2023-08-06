
import urllib.request
import os
from tqdm import tqdm
import json
import random
from SoccerNet.utils import getListGames

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

        if os.path.exists(path_local): # check existence
            if verbose:
                print(f"{path_local} already exists")
            return 2

        try:
            try:
                urllib.request.urlretrieve(
                    path_owncloud, path_local, MyProgressBar(path_local))

            except urllib.error.HTTPError as identifier:
                print(identifier)
                return 1
        except:
            os.remove(path_local)
            raise
            return 2
        return 0


class SoccerNetDownloader(OwnCloudDownloader):
    def __init__(self, LocalDirectory,
                 OwnCloudServer="https://exrcsdrive.kaust.edu.sa/exrcsdrive/public.php/webdav/"):
        super(SoccerNetDownloader, self).__init__(
            LocalDirectory, OwnCloudServer)

    def downloadVideoHD(self, game, file):
        # if file in ["1_HQ.mkv", "2_HQ.mkv", "video.ini"]:

        FileLocal = os.path.join(self.LocalDirectory, game, file)
        FileURL = os.path.join(self.OwnCloudServer, game, file).replace(' ', '%20')
        res = self.downloadFile(path_local=FileLocal,
                                path_owncloud=FileURL,
                                user="B72R7dTu1tZtIst",  # user for video HQ
                                password=self.password)


    def downloadVideo(self, game, file):
        # if file in ["1_HQ.mkv", "2_HQ.mkv", "video.ini"]:

        FileLocal = os.path.join(self.LocalDirectory, game, file)
        FileURL = os.path.join(self.OwnCloudServer, game, file).replace(' ', '%20')
        res = self.downloadFile(path_local=FileLocal,
                                path_owncloud=FileURL,
                                user="6XYClm33IyBkTgl",  # user for video
                                password=self.password)
                                    

    def downloadGames(self, files=["1.mkv", "2.mkv", "Labels.json"], split=["v1"], task="spotting", verbose=True, randomized=False):

        for spl in split:

            gamelist = getListGames(spl, task)
            if randomized:
                gamelist = random.sample(gamelist,len(gamelist))

            for game in gamelist:


                for file in files:

                    GameDirectory = os.path.join(self.LocalDirectory, game)
                    FileURL = os.path.join(
                        self.OwnCloudServer, game, file).replace(' ', '%20')
                    os.makedirs(GameDirectory, exist_ok=True)

                    if spl == "challenge": # specific buckets for the challenge set

                        # LQ Videos
                        if file in ["1.mkv", "2.mkv"]:
                            res = self.downloadFile(path_local=os.path.join(GameDirectory, file),
                                                    path_owncloud=FileURL,
                                                    user="trXNXsW9W04onBh",  # user for video LQ
                                                    password=self.password,
                                                    verbose=verbose)

                        # HQ Videos
                        elif file in ["1_HQ.mkv", "2_HQ.mkv", "video.ini"]:
                            res = self.downloadFile(path_local=os.path.join(GameDirectory, file),
                                                    path_owncloud=FileURL,
                                                    user="gJ8gja7V8SLxYBh",  # user for video HQ
                                                    password=self.password,
                                                    verbose=verbose)

                        # Labels
                        elif "Labels" in file:
                        # file in ["Labels.json", "Labels_v2.json"]:
                        # elif any(feat in file for feat in ["ResNET", "C3D", "I3D", "R25D"]):
                            res = self.downloadFile(path_local=os.path.join(GameDirectory, file),
                                                    path_owncloud=FileURL,
                                                    user="WUOSnPSYRC1RY13",  # user for Labels
                                                    password=self.password,
                                                    verbose=verbose)

                        # Features
                        elif any(feat in file for feat in ["ResNET", "C3D", "I3D", "R25D"]):
                            res = self.downloadFile(path_local=os.path.join(GameDirectory, file),
                                                    path_owncloud=FileURL,
                                                    user="d4nu5rJ6IilF9B0",  # user for Features
                                                    password="SoccerNet",
                                                    verbose=verbose)

                    else: # bucket for "v1"
                        # LQ Videos
                        if file in ["1.mkv", "2.mkv"]:
                            res = self.downloadFile(path_local=os.path.join(GameDirectory, file),
                                                    path_owncloud=FileURL,
                                                    user="6XYClm33IyBkTgl",  # user for video LQ
                                                    password=self.password,
                                                    verbose=verbose)

                        # HQ Videos
                        elif file in ["1_HQ.mkv", "2_HQ.mkv", "video.ini"]:
                            res = self.downloadFile(path_local=os.path.join(GameDirectory, file),
                                                    path_owncloud=FileURL,
                                                    user="B72R7dTu1tZtIst",  # user for video HQ
                                                    password=self.password,
                                                    verbose=verbose)

                        # Labels
                        elif "Labels" in file:
                        # elif file in ["Labels.json"]:
                            res = self.downloadFile(path_local=os.path.join(GameDirectory, file),
                                                    path_owncloud=FileURL,
                                                    user="ZDeEfBzCzseRCLA",  # user for Labels
                                                    password="SoccerNet",
                                                    verbose=verbose)
                        
                        # features
                        elif any(feat in file for feat in ["ResNET", "C3D", "I3D", "R25D"]):
                            res = self.downloadFile(path_local=os.path.join(GameDirectory, file),
                                                    path_owncloud=FileURL,
                                                    user="9eRjic29XTk0gS9",  # user for Features
                                                    password="SoccerNet",
                                                    verbose=verbose)

    #     for file in files:

    #         GameDirectory = os.path.join(self.LocalDirectory, game)
    #         FileURL = os.path.join(
    #             self.OwnCloudServer, game, file).replace(' ', '%20')
    #         os.makedirs(GameDirectory, exist_ok=True)

    #         # LQ Videos
    #         if file in ["1.mkv", "2.mkv"]:
    #             res = self.downloadFile(path_local=os.path.join(GameDirectory, file),
    #                                     path_owncloud=FileURL,
    #                                     user="trXNXsW9W04onBh",  # user for video LQ
    #                                     password=self.password)

    #         # HQ Videos
    #         elif file in ["1_HQ.mkv", "2_HQ.mkv", "video.ini"]:
    #             res = self.downloadFile(path_local=os.path.join(GameDirectory, file),
    #                                     path_owncloud=FileURL,
    #                                     user="gJ8gja7V8SLxYBh",  # user for video HQ
    #                                     password=self.password)

    #         # Labels
    #         elif file in ["Labels.json"]:
    #             res = self.downloadFile(path_local=os.path.join(GameDirectory, file),
    #                                     path_owncloud=FileURL,
    #                                     user="WUOSnPSYRC1RY13",  # user for Labels
    #                                     password=self.password)

    #         # Labels
    #         elif any(feat in file for feat in ["ResNET", "C3D", "I3D"]):
    #             res = self.downloadFile(path_local=os.path.join(GameDirectory, file),
    #                                     path_owncloud=FileURL,
    #                                     user="d4nu5rJ6IilF9B0",  # user for Features
    #                                     password="SoccerNet")



    # def downloadTestGames(self, files=["1.mkv", "2.mkv", "Labels.json"]):

    #     for game in getListTestGames():

    #         # game = os.path.join(championship, season, game)


    #         for file in files:

    #             GameDirectory = os.path.join(self.LocalDirectory, game)
    #             FileURL = os.path.join(
    #                 self.OwnCloudServer, game, file).replace(' ', '%20')
    #             os.makedirs(GameDirectory, exist_ok=True)

    #             # LQ Videos
    #             if file in ["1.mkv", "2.mkv"]:
    #                 res = self.downloadFile(path_local=os.path.join(GameDirectory, file),
    #                                         path_owncloud=FileURL,
    #                                         user="trXNXsW9W04onBh",  # user for video LQ
    #                                         password=self.password)

    #             # HQ Videos
    #             elif file in ["1_HQ.mkv", "2_HQ.mkv", "video.ini"]:
    #                 res = self.downloadFile(path_local=os.path.join(GameDirectory, file),
    #                                         path_owncloud=FileURL,
    #                                         user="gJ8gja7V8SLxYBh",  # user for video HQ
    #                                         password=self.password)

    #             # Labels
    #             elif file in ["Labels.json"]:
    #                 res = self.downloadFile(path_local=os.path.join(GameDirectory, file),
    #                                         path_owncloud=FileURL,
    #                                         user="WUOSnPSYRC1RY13",  # user for Labels
    #                                         password=self.password)

    #             # Labels
    #             elif any(feat in file for feat in ["ResNET", "C3D", "I3D"]):
    #                 res = self.downloadFile(path_local=os.path.join(GameDirectory, file),
    #                                         path_owncloud=FileURL,
    #                                         user="d4nu5rJ6IilF9B0",  # user for Features
    #                                         password="SoccerNet")


                    
