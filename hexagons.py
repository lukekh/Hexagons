import math
import matplotlib.pyplot as plt
import random
import time

class hexloc:
    def __init__(self, x, y, z):
        self._loc = (x, y, z)
    
    @property
    def loc(self):
        self.minimise()
        return self._loc
    
    @loc.setter
    def loc(self, val):
        h = hexloc(*val)
        self._loc = h.loc
    
    def __repr__(self):
        self.minimise()
        return f"hexloc{self.loc}"
    
    def __str__(self):
        return repr(self)
    
    def minimise(self):
        self._loc = tuple([i - sorted(self._loc)[1] for i in self._loc])
    
    def __iter__(self):
        return iter(self.loc)
    
    def __add__(self, other):
        return hexloc(*[hi+ki for hi,ki in zip(self, other)])
    
    def __sub__(self, other):
        return hexloc(*[hi-ki for hi,ki in zip(self, other)])
    
    def __neg__(self):
        return hexloc(*[-hi for hi in self])
    
    def __mul__(self, i):
        return hexloc(*[i*hi for hi in self])
    
    def __rmul__(self, i):
        return hexloc(*[i*hi for hi in self])
    
    def __eq__(self, other):
        try:
            c = tuple([hi-ki for hi, ki in zip(self.loc, other.loc)])
        except AttributeError:
            return False
        return c[0] == c[1] == c[2]
    
    def cartesian(self):
        return (
            self.loc[0] + self.loc[1]*math.cos(2*math.pi/3) + self.loc[2]*math.cos(4*math.pi/3),
            self.loc[1]*math.sin(2*math.pi/3) + self.loc[2]*math.sin(4*math.pi/3),
        )
    
    def __abs__(self):
        return tuple([abs(i) for i in self])
    
    def __hash__(self):
        return hash( (type(self), self.loc) )
    
    def hexdist(self):
        return sum(abs(self))
    

class hextile:
    def __init__(self, *loc):
        self.loc = hexloc(*loc) # Location is a hexloc
    
    def __repr__(self):
        return f"hextile{self.loc.loc}"
    
    def __iter__(self):
        return iter(self.loc)
    
    def __eq__(self, other):
        try:
            return self.loc == other.loc
        except AttributeError:
            False
    
    def adjacent(self, other):
        delta = abs(self.loc - other.loc)
        dist = sum([i for i in delta])
        if dist == 1:
            return True
        else:
            return False
    
    def __hash__(self):
        return hash( (type(self), self.loc) )


class Player:
    def __init__(self):
        self.loc = hexloc(0,0,0)
    
    def __repr__(self):
        return f"player{self.loc.loc}"
    
    def move(self, x=0, y=0, z=0):
        self.loc += hexloc(x,y,z)
        return self
    
    def on(self, tile):
        if self.loc == tile.loc:
            return True
        else:
            return False
    
    def at(self, loc):
        if self.loc == loc:
            return True
        else:
            return False
    
    def __hash__(self):
        return hash( (type(self), self.loc) )


    
class hexboard:
    def __init__(self, hexset=set()):
        self.hexset = hexset | {hextile(0,0,0)}
        self.player = Player()
    
    def move(self, x, y, z):
        self.player.move(x,y,z)
        t = hextile(*self.player.loc)
        if t not in self:
            self.hexset |= {t}
        return self
    
    def __contains__(self, item):
        return item in self.hexset
    
    def __repr__(self):
        return str( (self.player, self.hexset) )
    
    def __getitem__(self, item:hexloc):
        h = hextile(*item) 
        if h in self:
            return list(self.hexset & {h})[0]
        else:
            raise KeyError("this hex is not in the hexset")
    
    def plot(self, s=None):
        player_x, player_y = self.player.loc.cartesian()
        board_x,  board_y  = zip(*[h.loc.cartesian() for h in self.hexset])
        
        plt.scatter(board_x, board_y, c='steelblue', s=s)
        plt.scatter([0], [0], c='forestgreen', s=s)
        plt.scatter(player_x, player_y, c='firebrick', s=s)
        plt.gca().set_aspect('equal', adjustable='datalim')
        plt.axis('off')
        
        plt.show()
    
    def game(self):
        from IPython.display import clear_output

        def keymap(char):
            try:
                c=char.lower()
                d = {
                    'd': ( 1, 0, 0),
                    'w': ( 0, 1, 0),
                    'z': ( 0, 0, 1),
                    'a': (-1, 0, 0),
                    'x': ( 0,-1, 0),
                    'e': ( 0, 0,-1)
                }
                return d[c]
            except KeyError:
                return (0,0,0)

        # Init
        usr_input = "init"    
        
        while usr_input.lower() not in ("exit", "quit"):
            self.plot()
            usr_input = input("Move with the hexagon around the 's' key:\n")
            self.move(*keymap(usr_input))
            clear_output()
        
        self.plot()
        print("Successfully exited game")
    
    def sierpinski_walk(self, n):
        from IPython.display import clear_output

        def keymap(char):
            try:
                c=char.lower()
                d = {
                    'd': ( 1, 0, 0),
                    'w': ( 0, 1, 0),
                    'z': ( 0, 0, 1),
                    'a': (-1, 0, 0),
                    'x': ( 0,-1, 0),
                    'e': ( 0, 0,-1)
                }
                return d[c]
            except KeyError:
                return (0,0,0)
        
        seq = sierpinski(n)
        
        for i, letter in enumerate(seq):
            self.plot(s=64/math.sqrt(i+1))
            self.move(*keymap(letter))
            time.sleep(0.25)
            clear_output()
        
        self.plot(s=64/math.sqrt(len(seq)))
    
    def sierpinski(self, n):
        from IPython.display import clear_output

        def keymap(char):
            try:
                c=char.lower()
                d = {
                    'd': ( 1, 0, 0),
                    'w': ( 0, 1, 0),
                    'z': ( 0, 0, 1),
                    'a': (-1, 0, 0),
                    'x': ( 0,-1, 0),
                    'e': ( 0, 0,-1)
                }
                return d[c]
            except KeyError:
                return (0,0,0)
        
        seq = sierpinski(n)
        
        for letter in seq:
            self.move(*keymap(letter))
        
        self.plot(s=(64)/math.sqrt(3**(n-1)))

    def random_walk(self, n):
        from IPython.display import clear_output

        def keymap(char):
            try:
                c=char.lower()
                d = {
                    'd': ( 1, 0, 0),
                    'w': ( 0, 1, 0),
                    'z': ( 0, 0, 1),
                    'a': (-1, 0, 0),
                    'x': ( 0,-1, 0),
                    'e': ( 0, 0,-1)
                }
                return d[c]
            except KeyError:
                return (0,0,0)
        
        for i in range(n):
            self.plot()
            self.move(*keymap(random.choice(['d', 'e', 'w', 'a', 'z', 'x'])))
            time.sleep(0.25)
            clear_output()
        
        print(f"Agent has moved {self.player.loc.hexdist()} hexes away from origin.")
        self.plot()
        
def rot_c(string):
    seq = reversed(list(string))
    rot = []
    
    d = {
        'd': 'e',
        'e': 'w',
        'w': 'a',
        'a': 'z',
        'z': 'x',
        'x': 'd'
    }
    
    for letter in seq:
        rot.append(d[letter])
    
    return "".join(rot)

def rot_a(string):
    seq = reversed(list(string))
    rot = []
    
    d = {
        'd': 'x',
        'e': 'd',
        'w': 'e',
        'a': 'w',
        'z': 'a',
        'x': 'z'
    }
    
    for letter in seq:
        rot.append(d[letter])
    
    return "".join(rot)

def sierpinski(n):
        def recurse(n, s="d"):
            if n < 1:
                return s
            else:
                return recurse( n-1, rot_c(s)+s+rot_a(s) )
        return recurse(n-1)