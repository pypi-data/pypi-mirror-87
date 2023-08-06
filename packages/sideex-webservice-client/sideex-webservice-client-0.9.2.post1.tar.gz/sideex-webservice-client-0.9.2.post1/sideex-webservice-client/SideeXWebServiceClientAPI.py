import json
import asyncio
import aiohttp
import os
import ssl
from enum import Enum

class ProtocolType(Enum):
    HTTP = 0
    HTTPS_DISABLE = 1
    HTTPS_ENABLE = 2

class SideeXWebServiceClientAPI():
    def __init__(self, baseURL, protocolType=ProtocolType.HTTP, caFilePath=None):
        self.baseURL = baseURL
        self.protocolType = protocolType
        self.caFilePath = caFilePath
        self.sslContext = None

        if self.baseURL[-1] != '/':
            self.baseURL = self.baseURL + "/"

        if self.protocolType == ProtocolType.HTTPS_DISABLE:
            self.sslContext = False
        elif self.protocolType == ProtocolType.HTTPS_ENABLE:
            self.sslContext = ssl.create_default_context(cafile=self.caFilePath)

    async def echo(self):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=self.sslContext)) as session:
            # data = aiohttp.FormData()
            # data.add_field('token', token, content_type='application/x-www-form-urlencoded')

            async with session.get(self.baseURL+"sideex-webservice/echo") as resp:
                return await resp.text()

    async def runTestSuite(self, file):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=self.sslContext)) as session:
            data = aiohttp.FormData()
            data.add_field('file', file, filename=os.path.basename(file.name), content_type='application/x-www-form-urlencoded')
            async with session.post(self.baseURL+"sideex-webservice/runTestSuites", data = data) as resp:
                return await resp.text()
    
    async def getState(self, token):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=self.sslContext)) as session:
            data = aiohttp.FormData()
            data.add_field('token', token, content_type='application/x-www-form-urlencoded')

            async with session.get(self.baseURL+"sideex-webservice/getState", data = data) as resp:
                return await resp.text()

    async def download(self, formData, filePath, option):
        tempURL = self.baseURL
        if option == 0:
            tempURL = tempURL + "sideex-webservice/downloadReports"
        else:
            tempURL = tempURL + "sideex-webservice/downloadLogs"

        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=self.sslContext)) as session:
            async with session.get(tempURL, data = formData) as resp:
                test = await resp.read()
                with open(filePath, "wb") as f:
                    f.write(test)
    
    async def deleteJob(self, token):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=self.sslContext)) as session:
            data = aiohttp.FormData()
            data.add_field('token', token, content_type='application/x-www-form-urlencoded')

            async with session.post(self.baseURL+"sideex-webservice/deleteJob", data = data) as resp:
                return await resp.text()