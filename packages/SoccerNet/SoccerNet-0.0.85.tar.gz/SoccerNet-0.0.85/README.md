# SOCCERNETV2

```bash
conda create -n SoccerNet python pip
pip install SoccerNet
```

## How to Download Games (Python)

```python
from SoccerNet import SoccerNetDownloader

mySoccerNetDownloader = SoccerNetDownloader(
    LocalDirectory="/path/to/soccernet/folder")

# input password to download video (copyright protected)
password = input("Password for videos? (contact the author):\n")
mySoccerNetDownloader.password = password

# Download SoccerNet v1
mySoccerNetDownloader.downloadGames(files=["Labels.json"], split=["train","valid","test"]) # download labels
mySoccerNetDownloader.downloadGames(files=["1.mkv", "2.mkv"], split=["train","valid","test"]) # download LQ Videos
mySoccerNetDownloader.downloadGames(files=["1_HQ.mkv", "2_HQ.mkv", "video.ini"], split=["train","valid","test"]) # download HQ Videos
mySoccerNetDownloader.downloadGames(files=["1_ResNET_TF2.npy", "2_ResNET_TF2.npy"], split=["train","valid","test"]) # download Features


# Download SoccerNet Test Set
mySoccerNetDownloader.LocalDirectory = "/path/to/soccernet/challenge/folder"
mySoccerNetDownloader.downloadGames(files=["1.mkv", "2.mkv"], split=["challenge"]) # download LQ Videos
mySoccerNetDownloader.downloadGames(files=["1_HQ.mkv", "2_HQ.mkv", "video.ini"], split=["challenge"]) # download HQ Videos
mySoccerNetDownloader.downloadGames(files=["1_ResNET_TF2.npy", "2_ResNET_TF2.npy"], split=["challenge"]) # download Features
```

## How to read the list Games (Python)

```python
from SoccerNet import getListGames
print(getListGames(split="train")) # return list of games recommended for training
print(getListGames(split="valid")) # return list of games recommended for validation
print(getListGames(split="test")) # return list of games recommended for testing
print(getListGames(split=["train", "valid", "test"])) # return list of games for training, validation and testing
print(getListGames(split="v1")) # return list of games from SoccerNetv1 (train/valid/test)
print(getListGames(split="challenge")) # return list of games for the challenge
print(getListGames(split=["v1", "challenge"])) # return complete list of games

```

## [Coming soon...] How to extract features (TensorFlow 2)

### Tensorflow
```bash
conda install cudnn cudatoolkit=10.1
pip install scikit-video tensorflow imutils opencv-python==3.4.11.41
```

### Pytorch
```bash
conda install pytorch torchvision cudatoolkit=10.1 cudnn -c pytorch
pip install av
```
### Python
```python
from SoccerNet import FeatureExtractor

myFeatureExtractor = FeatureExtractor(
    args.soccernet_dirpath, feature="ResNet", video="LQ", back_end="TF2")

myFeatureExtractor.extractGameIndex(0)
```

## [Coming soon...] Tensorflow/Pytorch dataloader

```bash
pip install scikit-video
# pip cudnn cudatoolkit=10.1
pip install tensorflow
pip install pytorch torchvision cudatoolkit=10.1
pip install av

# conda install pytorch torchvision cudatoolkit=10.1 -c pytorch
```
