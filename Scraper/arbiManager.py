from Scraper.worldNode import Rankings, NodeManager


class ArbiManager:

    def __init__(self):
        self.alert = None
        self.oldArbi = None
        self.currArbi = None
        self.r = Rankings()
        self.fillRankA()
        self.fillRankB()
        self.fillRankC()

    def tick(self, driver):
        arbiData = driver.getArbi()
        if arbiData is not None:
            results = self.r.findNode(arbiData['node'].lower(), arbiData['type'].lower(), arbiData['enemy'].lower)

            if results is not None:
                results[1].alert()
                self.currArbi = arbiData['node'].lower()

    def highAlert(self):
        self.alert = "high"

    def basicAlert(self):
        self.alert = "basic"

    def lowAlert(self):
        self.alert = 'low'

    def clearAlert(self):
        self.alert = None

    def getAlert(self):
        if self.oldArbi != self.currArbi:
            self.oldArbi = self.currArbi
            return self.alert
        else:
            self.clearAlert()
            return None

    def fillRankA(self):
        a = NodeManager(self.highAlert)
        names = ['olympus', 'laomedeia', 'ganymede', 'ur', 'tamu', 'apollo', 'kelpie']
        for n in names:
            a.addNode(n, "any", "disruption")

        names = ['io', 'sinai', 'helene', 'hydron']
        for n in names:
            a.addNode(n, "any", "defense")

        names = ['paimon', 'larzac lares', 'sangeru', 'hyf', 'stöfler']
        for n in names:
            a.addNode(n, "infested", "defense")

        self.r.addManager(a, "a")

    def fillRankB(self):
        b = NodeManager(self.basicAlert)
        names = ['paimon', 'larzac', 'lares', 'sangeru', 'hyf', 'stöfler']
        for n in names:
            b.addNode(n, "grineer", "defense")
            b.addNode(n, "corpus",  "defense")

        self.r.addManager(b, "b")

    def fillRankC(self):
        c = NodeManager(self.lowAlert)
        names = ['callisto', 'ose', 'odin', 'gaia']
        for n in names:
            c.addNode(n, "any", "interception")

        names = ['stickney', 'wahiba', 'malva', 'v prime', 'palus']
        for n in names:
            c.addNode(n, "any", "survival")

        self.r.addManager(c, "c")




