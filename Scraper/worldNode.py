class basics:
    modes = ['defense', 'survival', 'disruption', 'interception', 'excavation']
    factions = ["grineer", "infested", "corpus", "corrupted"]


class WarframeNode:
    def __init__(self, name, faction, mode):
        self.name = name
        self.faction = faction
        self.mode = mode
        return


class NodeManager:
    b = basics()

    def __init__(self, itemFoundMethod):
        self.nodes = []
        self.alert = itemFoundMethod

    def __addNode(self, node):
        self.nodes.append(node)

    def addNode(self, name, faction, mode):
        if faction == "any":
            for f in self.b.factions:
                self.removeNode(name, faction)
                self.nodes.append(WarframeNode(name, f, mode))
        else:
            self.removeNode(name, faction)
            self.nodes.append(WarframeNode(name, faction, mode))

    def removeNode(self, name, faction):
        for n in self.nodes:
            if n.name.find(name):
                if faction == "any":
                    self.nodes.remove(n)
                elif n.faction == faction:
                    self.nodes.remove(n)
                    break
        return None

    def findNode(self, name):
        for n in self.nodes:
            if n.name.find(name):
                return n
        return None


class Rankings:

    def __init__(self):
        self.nodeManagers = {}

    def addManager(self, manager, ranking):
        self.nodeManagers[ranking] = manager

    def findNode(self, name):
        for key, m in self.nodeManagers.items():
            node = m.findNode(name)
            if node is not None:
                return node, m
        return None
