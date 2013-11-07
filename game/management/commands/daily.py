from django.core.management.base import BaseCommand
from game.models import GlobalConstants
from time import time
from govt.models import State
from django.db import connection
from industry.models import Factory, LoansCreated
from decimal import Decimal
from django.db.models import F
from player.models import LogBook, Player
from energy.models import PowerPlant
from calamity.models import CalamityOccurence, Calamity
from transport.models import TransportCreated
import random

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        connection.query = []
        start = time()
        self.daily()
        self.stdout.write("Total time: %f"%(time()-start))
        self.stdout.write("Total queries: %d"%(len(connection.query)))
    
    def daily(self):
        glo = GlobalConstants.objects.get()
        states = State.objects.all()
        messages = [] #Messages to be logged
        for state in states:
            
            severity = 0
            calamities = CalamityOccurence.objects.select_related('type').filter(state = state)
            for calamity in calamities:
                severity = severity+(1-severity)*(calamity.type.severity/100)
            
            factoriesIn = Factory.objects.select_related('player','type').filter(state = state).exclude(shut_down = True).exclude(player__suspended = True)
            factoriesOut = Factory.objects.select_related('player','type').exclude(state = state).exclude(shut_down = True).filter(transport__states__in = [state.id]).exclude(player__suspended = True)
            factories = factoriesIn | factoriesOut
            sums = {}
            totalMoney = Decimal(state.income*state.population*Decimal(1000))
            
            
            for factory in factories:
                if sums.get(factory.type_id) == None:
                    sums[factory.type_id] = 0
                brand_cost = (factory.player.brand + Decimal(20))/Decimal(20)
                sums[factory.type_id] += Decimal(1)/(brand_cost*factory.selling_price*Decimal(1000))
            
            
            money_per_factory = Decimal(totalMoney/len(sums)) #Money per factory type
            constantSums = {} #Constants for each industry type
            
            for sumInd in sums:
                constantSums[sumInd] = money_per_factory/sums[sumInd]
            
            
            for factory in factories:
                brand_cost = (factory.player.brand + Decimal(20))/Decimal(20)
                tax_remaining = (Decimal(100)-brand_cost*glo.tax_rate)/Decimal(100)
                amount = Decimal(1-severity)*constantSums[factory.type_id]/(brand_cost*factory.selling_price*Decimal(1000))
                no_of_products = Decimal(amount/(factory.selling_price*Decimal(1000)))
                carbon = no_of_products*factory.type.carbon_per_unit
                energy = no_of_products*factory.type.energy_per_unit + factory.type.maintenance_energy
                amount = amount*tax_remaining
                production_costs = no_of_products*factory.type.cost_price*Decimal(1000) + factory.type.maintenance_cost
                factory.player.capital = F('capital') + amount - production_costs
                factory.player.netWorth = F('netWorth') + amount - production_costs - energy*glo.energy_buying_price
                factory.player.extra_energy = F('extra_energy') - energy
                factory.player.monthly_carbon_total = F('monthly_carbon_total') + carbon
                factory.player.save()
                factory.products_last_day = no_of_products
                factory.save()
                messages.append(LogBook(player=factory.player,message='Earned a revenue of %.2f minus tax for %s'%(amount,factory.type.name)))
                messages.append(LogBook(player=factory.player,message='Paid maintenance and production costs of %.2f for %s'%(production_costs,factory.type.name)))            

            
            powerplants = PowerPlant.objects.select_related('player','type').exclude(player__suspended = True).exclude(shut_down = True).filter(state = state)
            for powerplant in powerplants:
                powerplant.person.capital = F('capital') - powerplant.type.maintenance_cost
                powerplant.person.monthly_carbon_total = F('monthly_carbon_total') + powerplant.carbon_per_unit*powerplant.type.output
                powerplant.person.extra_energy = F('extra_energy') + (1-severity)*Decimal(powerplant.type.output)
                powerplant.person.netWorth = F('netWorth') + glo.energy_buying_price*powerplant.type.output - powerplant.type.maintenance_cost
                powerplant.person.save()
                messages.append(LogBook(player=powerplant.player,message='Generated energy units amounting to %.2f for %s'%(powerplant.carbon_per_unit*powerplant.type.output,powerplant.type.name)))
                messages.append(LogBook(player=powerplant.player,message='Paid maintenance and production costs of %.2f for %s'%(production_costs,powerplant.type.name)))
        
        transports = TransportCreated.objects.select_related('player','transport').exclude(player__suspended = True)
        for transport in transports:
            costs = Decimal(transport.states.count())*transport.transport.stopping_cost + transport.transport.travel_rate*transport.distance
            energy = transport.transport.travel_rate*transport.distance
            carbon = transport.transport.travel_rate*transport.distance
            transport.person.capital = F('capital') - costs
            transport.person.extra_energy = F('extra_energy') - energy
            transport.person.monthly_carbon_total = F('monthly_carbon_total') - carbon  
            transport.person.save()
            messages.append(LogBook(player=transport.player,message='Paid maintenance and production costs of %.2f for %s'%(costs,transport.transport.name)))
        
        players = Player.objects.all()
        for player in players:
            if player.suspended:
                if player.capital >= 30:
                    player.suspended = False
                    messages.append(LogBook(player=player,message='Your suspension has been removed since you have accumulated wealth more than 30 million.'))
            elif player.capital < 30:
                player.suspended = True
                messages.append(LogBook(player=player,message='You have been suspended since your capital has gone below 30 million.'))
            if player.extra_energy < 0:
                energy = player.extra_energy
                player.capital = F('capital') + energy * glo.energy_selling_price #Player extra energy is negative
                player.extra_energy = 0
                messages.append(LogBook(player=player,message='You had to buy energy from the government as your energy had expired.'))
            elif player.extra_energy > player.energy_capacity:
                energy = player.extra_energy - player.energy_capacity
                player.capital = F('capital') + energy * glo.energy_buying_price #Player extra energy is negative
                player.extra_energy = F('energy_capacity')
                messages.append(LogBook(player=player,message='Extra energy was sold off to the government.'))
            player.save()
        
        LogBook.objects.bulk_create(messages)
        
        if glo.current_day == 1:
            self.monthly()
        if glo.current_month == 1:
            self.yearly()
        
        glo.nextDay()
    
    def monthly(self):
        Loans = LoansCreated.objects.exclude(player__suspended = True)
        for Loan in Loans:
            Loan.monthlyUpdate()
        
        #Calamities
        counter = random.randint(1,100)
        calamityTime = random.randint(3,10)
        calamity = Calamity.objects.filter(probability_number = counter).order_by('?')[0]
        if calamity is not None:
            state = calamity.states.all().order_by('?')[0]
            occurence = CalamityOccurence(type = calamity, state = state, time_remaining = calamityTime)
            occurence.save()
        
        #Brand, carbon_last_month
        players = Player.objects.all().exclude(player__suspended = True).order_by('-netWorth','-capital')
        carbons = []
        for player in players:
            carbons.append(player.monthly_carbon_total)
        
        #Mapping carbons array to brand array
        maximum = max(carbons)
        divisor = maximum/10.0
        brands = reduce(lambda x: x/divisor - 5, carbons)
        
        
        for index,player in enumerate(players):
            player.monthly_carbon_total = 0
            player.last_month_total = carbons[index]
            player.brand = brands[index]
            player.rank = index+1
            player.save()
    
    def yearly(self):
        states = State.objects.all()
        for state in states:
            state.annualUpdate()
        
        
        factories = Factory.objects.all()
        for factory in factories:
            factory.annualUpdate()
        
        
        powerplants = Factory.objects.all()
        for powerplant in powerplants:
            powerplant.annualUpdate()
            