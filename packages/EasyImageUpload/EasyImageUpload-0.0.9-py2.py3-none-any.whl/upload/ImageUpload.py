#!/usr/bin/env python
# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod, abstractproperty
import typing
import os
import logging
import time
import rx
import requests
import shutil
from qiniu import Auth, put_file
from PIL import Image, ImageDraw
import sys
import json
from PySide2.QtCore import QMimeData
from PySide2.QtGui import QImage
from monitor import HandlerStatusInfo, StatusFlag
import tinify


def fileNameGenerate(originName) -> str:
    suffix = os.path.splitext(originName)[-1]
    today = time.strftime("%Y%m%d%H%M%S", time.localtime())
    newFileName = "%s_%s" % (today, originName)
    print("new file name: %s" % newFileName)
    return newFileName


def getProjectPath():
    return os.path.dirname(sys.argv[0])


class ResultInfo:
    def __init__(self, code: bool = True, image: str = None, orgImage: str = None, error: str = None):
        self.code = code
        self.image = image
        self.orgImage = orgImage
        self.error = error


class Strategy(metaclass=ABCMeta):
    def __init__(self):
        self.supportSuffixs = None
        self.saveDirPath = "cacheTemp"
        self.defaultSupportSuffixs: typing.List = ['.jpg', '.png', '.jpeg', '.gif', '.svg', '.bmp', '.webp']
        self.textWatermark = None
        self.tinifyAppKey = None
        self.imgResizeEnable: bool = False
        self.imgMaxWidth: int = 0
        self.imgMaxHeight: int = 0

    def notifyMsg(self, process: float = 0, msg: str = ""):
        pass

    def save(self, imageSrc: str = None) -> ResultInfo:
        if not os.path.isfile(imageSrc):
            printError("imageSrc must is image file")
            return ResultInfo(code=False, error="上传链接不是一个可用的图片文件")
        baseFileName = os.path.basename(imageSrc)
        suffix = os.path.splitext(baseFileName)[-1]
        if str(suffix).lower() not in self.supportSuffixs:
            printError("current setting is not support for image's type of suffix :%s " % suffix)
            return ResultInfo(code=False, error="%s 格式的图片类型暂不支持" % suffix)
        newFileName = fileNameGenerate(baseFileName)
        savePath = os.path.join(self.saveDirPath, newFileName)
        shutil.copyfile(imageSrc, savePath)

        # 0、设置图片大小
        if self.imgResizeEnable:
            self.notifyMsg(15, "重置图片大小：%s" % baseFileName)
            savePath = self.processResize(savePath)

        # 1、压缩处理
        if self.tinifyAppKey:
            self.notifyMsg(20, "压缩图片：%s" % baseFileName)
            savePath = self.processCompression(savePath)

        # 2、水印处理
        if self.textWatermark:
            self.notifyMsg(30, "图片水印处理：%s" % baseFileName)
            savePath = self.processWatermark(savePath)
        # 3、开始上传
        self.notifyMsg(50, "开始上传：%s" % baseFileName)
        result, error = self.startSave(savePath)
        self.notifyMsg(80, "上传结束：%s" % baseFileName)
        os.remove(savePath)
        self.notifyMsg(90, "删除临时文件")
        if result:
            return ResultInfo(code=True, image=result)
        else:
            return ResultInfo(code=False, error=error)

    def processResize(self, imgStr: str) -> str:
        image: Image = Image.open(imgStr)
        w, h = image.size

        if w > self.imgMaxWidth:
            h = (self.imgMaxWidth / w) * h
            w = self.imgMaxWidth
        elif h > self.imgMaxHeight:
            w = (self.imgMaxHeight / h) * w
            h = self.imgMaxHeight

        image = image.resize((int(w), int(h)), Image.ANTIALIAS)
        image.save(imgStr)
        return imgStr

    def processCompression(self, imgStr: str) -> str:
        tinify.key = self.tinifyAppKey
        source = tinify.from_file(imgStr)
        source.to_file(imgStr)
        return imgStr

    def processWatermark(self, imgStr: str) -> str:
        return self.addTextToImage(imgStr, self.textWatermark)

    def addTextToImage(self, imgSrc, text) -> str:
        # font = ImageFont.load("simsun.pil")
        # font = ImageFont.truetype("simsun.ttc", 40, encoding="unic")  # 设置字体
        type = ""
        type_value = None
        if str(os.path.splitext(imgSrc)[-1]).lower() in [".jpeg", '.jpg']:
            image = Image.open(imgSrc)
            print(os.path.splitext(imgSrc)[0])
            os.remove(imgSrc)
            imgSrc = imgSrc.replace(os.path.splitext(imgSrc)[-1], ".png")
            image.save(imgSrc)

        image = Image.open(imgSrc)

        type = "RGBA"
        type_value = (255, 255, 255, 0)

        rgba_image = image.convert(type)
        text_overlay = Image.new(type, rgba_image.size, type_value)
        image_draw = ImageDraw.Draw(text_overlay)

        text_size_x, text_size_y = image_draw.textsize(text)
        # 设置文本文字位置
        print(rgba_image)
        text_xy = (rgba_image.size[0] - text_size_x - 8, rgba_image.size[1] - text_size_y - 10)
        # 设置文本颜色和透明度
        image_draw.text(text_xy, text, fill=(76, 234, 124))

        image_with_text = Image.alpha_composite(rgba_image, text_overlay)
        image_with_text.save(imgSrc)
        return imgSrc

    @abstractmethod
    def startSave(self, imageSrc: str = None) -> typing.Any:
        pass

    @abstractmethod
    def initSetting(self, param: dict = None) -> typing.Any:
        if 'tempCache' in param.keys():
            self.saveDirPath = param["tempCache"]
        else:
            self.saveDirPath = os.path.join(getProjectPath(), self.saveDirPath)
        if not os.path.exists(self.saveDirPath):
            os.mkdir(self.saveDirPath)

        if 'supportSuffixs' in param.keys():
            self.supportSuffixs = param["supportSuffixs"]
        else:
            self.supportSuffixs = self.defaultSupportSuffixs

        if 'textWatermark' in param.keys():
            self.textWatermark = param['textWatermark']

        if 'tinifyAppKey' in param.keys():
            self.tinifyAppKey = param['tinifyAppKey']

        if 'imgResizeEnable' in param.keys():
            self.imgResizeEnable = param['imgResizeEnable']
            if 'imgMaxHeight' in param.keys():
                self.imgMaxHeight = int(param['imgMaxHeight'])

            if 'imgMaxWidth' in param.keys():
                self.imgMaxWidth = int(param['imgMaxWidth'])

        self.init = True


def printError(msg: str = ""):
    logging.error("%s | %s " % ("ImageLocalSaveStrategy", msg))


class ImageQiniuSaveStrategy(Strategy):

    def __init__(self):
        Strategy.__init__(self)
        self.access_key = ""
        self.secret_key = ""
        self.bucket_name = ""
        self.host_image = ""

    def startSave(self, imageSrc: str = None) -> typing.Any:
        q = Auth(self.access_key, self.secret_key)
        token = q.upload_token(self.bucket_name, os.path.basename(imageSrc), 3600)

        ret, info = put_file(token, os.path.basename(imageSrc), imageSrc)
        print(info)
        print(ret)
        if info.status_code == 200:
            return ("%s/%s" % (self.host_image, ret['key']), None)
        return (None, "上传失败")

    def initSetting(self, param: dict = None) -> typing.Any:
        Strategy.initSetting(self, param)
        if 'access_key' in param.keys():
            self.access_key = param["access_key"]
        if 'secret_key' in param.keys():
            self.secret_key = param["secret_key"]
        if 'bucket_name' in param.keys():
            self.bucket_name = param["bucket_name"]

        if 'host_image' in param.keys():
            self.host_image = param["host_image"]


class ImageSMMSSaveStrategy(Strategy):

    def __init__(self):
        Strategy.__init__(self)
        self.appk = ""
        self.username = ""
        self.password = ""
        self.getTokenUrl = 'https://sm.ms/api/v2/token'
        self.uploadUrl = 'https://sm.ms/api/v2/upload'

    def startSave(self, imageSrc: str = None) -> typing.Any:
        return self.upload(imageSrc)

    def getToken(self):
        payload = {'username': self.username, 'password': self.password}
        response = requests.post(url=self.getTokenUrl, data=payload)
        rsp = response.text
        result = json.loads(rsp)
        if result['code'] == 'success':
            return result['data']['token']
        return None

    def upload(self, filePath):
        token = self.getToken()
        headers = {}
        if token:
            headers = {"Authorization": "Basic %s" % token}
            print(headers)
        files = {'smfile': open(filePath, 'rb')}
        response = requests.post(url=self.uploadUrl, headers=headers, files=files)
        rsp = response.text
        print(rsp)
        result = json.loads(rsp)
        if result['code'] == 'success':
            return (result['data']['url'], None)
        elif result['code'] == 'image_repeated':
            return (result['images'], None)
        else:
            return (None, result['message'])

    def initSetting(self, param: dict = None) -> typing.Any:
        Strategy.initSetting(self, param)
        if 'appk' in param.keys():
            self.appk = param["appk"]

        if 'username' in param.keys():
            self.username = param["username"]

        if 'password' in param.keys():
            self.password = param["password"]


class ImageUploadHelper:
    _instance = None

    def __init__(self):
        self.strategy: Strategy = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ImageUploadHelper, cls).__new__(cls, *args, **kwargs)

        return cls._instance

    def init(self, strategy: Strategy = None):
        self.strategy = strategy

    def saveImage(self, imageSrcList: list = None) -> rx.Observable:

        _imageSrcList = imageSrcList

        def _createObserver(observable, scheduler):
            def notifyMsg(proccess, msg):
                observable.on_next(HandlerStatusInfo(StatusFlag.Process, msg=msg, value=proccess))

            try:
                if self.strategy:
                    self.strategy.notifyMsg = notifyMsg
                    observable.on_next(HandlerStatusInfo(StatusFlag.Start, "开始上传"))
                    for img in _imageSrcList:

                        observable.on_next(HandlerStatusInfo(StatusFlag.Process, msg="upload image: %s" % img, value=0))
                        result: ResultInfo = self.strategy.save(img)
                        if result.code:
                            observable.on_next(
                                HandlerStatusInfo(StatusFlag.Process, msg="upload image success", value=100))
                            result.orgImage = img
                            observable.on_next(result)
                        else:
                            observable.on_next(
                                HandlerStatusInfo(StatusFlag.Process, msg="upload image: %s error" % img, value=100))
                            result.orgImage = img
                            observable.on_next(result)
                    observable.on_completed()
                else:
                    observable.on_error("未设置图片上传插件")

            except Exception as e:
                observable.on_error(e)

        return rx.create(_createObserver)

    def saveImageForQMineImage(self, imageSrcList: list) -> rx.Observable:
        _imageSrcList = imageSrcList

        def _createObserver(observable, scheduler):
            def notifyMsg(proccess, msg):
                observable.on_next(HandlerStatusInfo(StatusFlag.Process, msg=msg, value=proccess))

            tempFileList = list()
            try:
                if self.strategy:
                    self.strategy.notifyMsg = notifyMsg
                    observable.on_next(HandlerStatusInfo(StatusFlag.Start, "开始上传"))
                    for img in _imageSrcList:
                        if type(img) != QMimeData:
                            continue
                        image = QImage(img.imageData())
                        tempFileName = os.path.join(getProjectPath(), fileNameGenerate('%s.png' % time.time()))
                        image.save(tempFileName)
                        tempFileList.append(tempFileName)
                        observable.on_next(
                            HandlerStatusInfo(StatusFlag.Process, msg="upload image: %s" % tempFileName, value=0))

                        result = self.strategy.save(tempFileName)
                        if result.code:
                            observable.on_next(
                                HandlerStatusInfo(StatusFlag.Process, msg="upload image success",
                                                  value=100))
                            result.orgImage = tempFileName
                            observable.on_next(result)
                        else:
                            observable.on_next(
                                HandlerStatusInfo(StatusFlag.Process, msg="upload image: %s error" % tempFileName,
                                                  value=100))
                            result.orgImage = tempFileName
                            observable.on_next(result)
                    observable.on_completed()
                else:
                    observable.on_next(
                        HandlerStatusInfo(StatusFlag.Process, msg="未设置图片上传插件", value=100))
                    observable.on_error("未设置图片上传插件")
            except Exception as e:
                observable.on_error(e)
            finally:
                if len(tempFileList) > 0:
                    for file in tempFileList:
                        os.remove(file)

        return rx.create(_createObserver)


imageUploadManager = ImageUploadHelper()
