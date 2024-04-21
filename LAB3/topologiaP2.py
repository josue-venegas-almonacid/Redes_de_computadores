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


        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')
        s5 = self.addSwitch('s5')

        # Add links
        #Entre hosts
        self.addLink(h1, s1, 1, 2)
        self.addLink(h2, s1, 3, 4)

        self.addLink(h3, s2, 5, 6)
        self.addLink(h4, s2, 7, 8)

        self.addLink(h5, s5, 9, 10)
        self.addLink(h6, s5, 11, 12)

        #Entre switches
        self.addLink(s4, s2, 13, 14)
        self.addLink(s2, s1, 15, 16)
        self.addLink(s1, s5, 17, 18)
        self.addLink(s5, s3, 19, 20)
        self.addLink(s3, s1, 21, 22)
        self.addLink(s3, s4, 23, 24)

topos = { 'topo1': ( lambda: Net() ) }