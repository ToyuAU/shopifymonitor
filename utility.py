class Data:
    def loadProxies(self,directory):
        proxies = []
        with open(directory,'r') as e:
            e = e.readlines()
            for i in e:
                i = i.strip().split(':')
                proxies.append({
                    'http':'http://{}:{}@{}:{}'.format(i[2],i[3],i[0],i[1]),
                    'https':'http://{}:{}@{}:{}'.format(i[2],i[3],i[0],i[1])
                })

        if proxies == []:
            proxies.append(None)
        return proxies
