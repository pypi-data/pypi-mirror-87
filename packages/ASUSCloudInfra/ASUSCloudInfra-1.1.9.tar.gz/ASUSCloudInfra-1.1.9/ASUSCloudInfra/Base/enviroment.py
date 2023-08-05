class Enviroment():
    def __init__(self, rawData = None):
        self._env = {}
        self.setRawData(rawData)

    def setRawData(self, rawData):
        env = {}
        if rawData:
            for data in rawData:
                env[data['name']] = data['value']
        self._env =env
    
    def getKeyList(self):
        return self._env.keys()

    def get(self, key:str):
        return self._env.get(key)
    
    def set(self, key:str, value):
        self._env[key] = value

    def getRawData(self):
        datas = []
        for key in self._env.keys():
            data = {
                'name': key,
                'value': self._env[key]
            }
            datas.append(data)
        return datas

    