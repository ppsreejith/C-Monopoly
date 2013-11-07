from django.db import models
from django.core.exceptions import ValidationError
from player.models import Player
from govt.models import State
import math, itertools

# Create your models here.
class Transport(models.Model):
    name = models.CharField(max_length = 50, unique = True)
    research_level = models.PositiveIntegerField(help_text="Typically a small number (Integer)")
    states = models.ManyToManyField(State, help_text = "Available states")
    initial_cost = models.DecimalField(max_digits = 9, decimal_places = 2, help_text="In Millions")
    stopping_cost = models.DecimalField(max_digits = 9, decimal_places = 5, help_text="In Millions")
    travel_rate = models.DecimalField(max_digits = 9, decimal_places = 5, help_text="In Millions. Cost per unit distance.")
    max_stops = models.PositiveIntegerField(help_text="Typically a small number (Integer)")
    carbon_cost_rate = models.DecimalField(max_digits = 9, decimal_places = 2, help_text = "Carbon cost per unit distance.")
    energy_rate = models.DecimalField(max_digits = 9, decimal_places = 2, help_text = "Energy units per unit distance.")
    def __unicode__(self):
        return self.name

class TransportCreated(models.Model):
    transport = models.ForeignKey(Transport)
    states = models.ManyToManyField(State,help_text = "Available Stops")
    distance = models.DecimalField(max_digits=12, decimal_places=5,default = 0, help_text="Will be calculated automatically")
    player = models.ForeignKey(Player)
    def __unicode__(self):
        return str(self.transport) + " by " + str(self.player)
    class Meta:
        verbose_name = "Created Transport"
    def setDistance(self):
        coords = self.states.values('coordx','coordy')
        self.distance = solve_tsp_dynamic(coords)
        self.save()

def check_stops(states, transport):
    check_no_states(states)
    if states.count() > transport.max_stops:
        raise ValidationError("Maximum number of stops exceeded")
    elif set(states.all()) - set(transport.states.all()):
        raise ValidationError("Invalid stops")

def check_no_states(states):
    if states.count() < 3:
        raise ValidationError("Need more states")

def check_player(transport,player,states):
    if player.research_level < transport.research_level:
        raise ValidationError("You are not qualified enough to build this transport.")
    if player.transportcreated_set.count() > 3:
        raise ValidationError("You have reached the maximum number of transports possible.")
    if any(state.research_level > player.research_level for state in states):
        raise ValidationError("You are not qualified enough to reach some states.")
    check_commodity(transport,player)

def check_commodity(commodity, player):
    if commodity.initial_cost > player.capital - 30:
        raise ValidationError("This %s is too expensive for you."%str(commodity))

def solve_tsp_dynamic(points):
        def find_lengths(order):
            l = len(order)
            newpath = []
            for i in range(0,l):
                newpath.append(points[order[i]])
            newpath.append(points[0])
            summ = 0
            earl = newpath[0]
            for i in range(1,l+1):
                summ += length(earl,newpath[i])
                earl = newpath[i]
            return summ
    
        def length(x,y):
            return math.sqrt((y['coordx']-x['coordx'])**2 + (y['coordy']-x['coordy'])**2)
        
        #calc all lengths
        all_distances = [[length(x,y) for y in points] for x in points]
        #initial value - just distance from 0 to every other point + keep the track of edges
        A = {(frozenset([0, idx+1]), idx+1): (dist, [0,idx+1]) for idx,dist in enumerate(all_distances[0][1:])}
        cnt = len(points)
        for m in range(2, cnt):
            B = {}
            for S in [frozenset(C) | {0} for C in itertools.combinations(range(1, cnt), m)]:
                for j in S - {0}:
                    B[(S, j)] = min( [(A[(S-{j},k)][0] + all_distances[k][j], A[(S-{j},k)][1] + [j]) for k in S if k != 0 and k!=j])
            A = B
        res = min([(A[d][0] + all_distances[0][d[1]], A[d][1]) for d in iter(A)])
        ans = find_lengths(res[1])
        return ans