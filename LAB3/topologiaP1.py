from mininet.topo import Topo

class Net( Topo ):
    def __init__( self ):
        Topo.__init__(self)

        # Add hosts and switches
        h1 = self.addHost('h1', mac="00:00:00:00:00:01")
        h2 = self.addHost('h2', mac="00:00:00:00:00:02")
        h3 = self.addHost('h3', mac="00:00:00:00:00:03")
        h4 = self.addHost('h4', mac="00:00:00:00:00:04")
        h5 = self.addHost('h5', mac="00:00:00:00:00:05")
        h6 = self.addHost('h6', mac="00:00:00:00:00:06")
        h7 = self.addHost('h7', mac="00:00:00:00:00:07")
        h8 = self.addHost('h8', mac="00:00:00:00:00:08")


        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')

        # Add links
        #Entre hosts
        self.addLink(h1, s1, 1, 2)
        self.addLink(h2, s1, 3, 4)

        self.addLink(h3, s2, 5, 6)
        self.addLink(h4, s2, 7, 8)

        self.addLink(h5, s3, 9, 10)
        self.addLink(h6, s3, 11, 12)

        self.addLink(h7, s4, 13, 14)
        self.addLink(h8, s4, 15, 16)

        #Entre switches
        self.addLink(s1, s2, 17, 18)
        self.addLink(s2, s3, 19, 20)
        self.addLink(s3, s4, 21, 22)
        self.addLink(s4, s1, 23, 24)

topos = { 'topo1': ( lambda: Net() ) }