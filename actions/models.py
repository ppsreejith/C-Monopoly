from player.models import Player, LogBook, ResearchProject
from transport.forms import TransportCreatedForm
from energy.models import EnergyIndustry, PowerPlant
from govt.models import State, AquireRecord, EnergyDeal
from industry.models import ProductIndustry, Factory
from django.core.exceptions import ValidationError
from game.models import GlobalConstants
from industry.forms import LoansCreatedForm
from decimal import Decimal
from django.db.models import F

#Main game profile class. Proxy for Player class
class Profile(Player):
    class Meta:
        proxy = True
    
    def buy_transport(self, transport, states):
        ct = TransportCreatedForm({'player':self.id, 'transport':transport, 'states':states, 'distance':0}).save()
        self.capital = F('capital') - ct.transport.initial_cost
        self.netWorth = F('netWorth') - ct.transport.initial_cost*Decimal(0.2)
        self.save()
        ct.setDistance()
        LogBook.objects.create(player = self, message = "Bought Transport for Rs. %.2f Million."%ct.transport.initial_cost)
    
    def sell_transport(self, transportcreated):
        ct = self.transportcreated_set.get(pk = transportcreated)
        amount = ct.transport.initial_cost*Decimal(0.8)
        ct.delete()
        self.capital = F('capital') + amount
        self.save()
        LogBook.objects.create(player = self, message = "Sold Transport for Rs. %.2f Million."%amount)
    
    def setTransport(self, factory, transport):
        currentFactory = self.factory_set.get(pk = factory)
        currentTransport = self.transportcreated_set.get(pk = transport)
        currentFactory.setTransport(currentTransport)
    
    def clearTransport(self, factory):
        currentFactory = self.factory_set.get(pk = factory)
        currentFactory.setTransport(None)
    
    def buy_powerPlant(self,industry,state):
        currentIndustry = EnergyIndustry.objects.get(pk = industry)
        currentState = State.objects.get(pk = state)
        currentPowerPlant = PowerPlant(type = currentIndustry, 
                                state = currentState,
                                player = self,
                                actual_value = currentIndustry.initial_cost*Decimal(0.9))
        currentPowerPlant.full_clean()
        currentPowerPlant.save()
        self.capital = F('capital') - currentIndustry.initial_cost
        self.netWorth = F('netWorth') - currentIndustry.initial_cost*Decimal(0.1)
        self.save()
        LogBook.objects.create(player = self, message = "Bought Power plant for Rs. %.2f Million."%float(currentIndustry.initial_cost))
    
    def sell_powerPlant(self, powerPlant):
        currentPowerPlant = self.powerplant_set.get(pk = powerPlant)
        amount = currentPowerPlant.actual_value
        currentPowerPlant.delete()
        self.capital = F('capital') + amount
        self.save()
        LogBook.objects.create(player = self, message = "Sold Power plant for Rs. %.2f Million."%float(amount))
    
    def buy_factory(self,industry,state):
        currentIndustry = ProductIndustry.objects.get(pk = industry)
        currentState = State.objects.get(pk = state)
        factory = Factory(type = currentIndustry, 
                          state = currentState, 
                          player = self,
                          selling_price = currentIndustry.cost_price*Decimal(1.1),
                          actual_value = currentIndustry.initial_cost*Decimal(0.9))
        factory.full_clean()
        factory.save()
        self.capital = F('capital') - currentIndustry.initial_cost
        self.netWorth = F('netWorth') - currentIndustry.initial_cost*Decimal(0.1)
        self.save()
        LogBook.objects.create(player = self, message = "Bought Factory for Rs. %.2f Million."%float(currentIndustry.initial_cost))
    
    def setSellingPrice(self, factory, new_sp):
        currentFactory = self.factory_set.get(pk = factory)
        currentFactory.setSellingPrice(new_sp)
    
    def sell_factory(self, factory):
        currentFactory = self.factory_set.get(pk = factory)
        if hasattr(self, 'Loan'):
            if currentFactory in self.Loan.mortaged_industries.all():
                raise ValidationError("Can't sell off a mortaged Factory")
        amount = currentFactory.actual_value
        currentFactory.delete()
        self.capital = F('capital') + amount
        self.save()
        LogBook.objects.create(player = self, message = "Sold Factory for Rs. %.2f Million."%float(amount))
    
    def shutdownFactory(self,factory):
        currentFactory = self.factory_set.get(pk = factory)
        currentFactory.shutdown()
        LogBook.objects.create(player = self, message = "Shutdown factory in %s"%currentFactory.state.name)
    
    def restartFactory(self,factory):
        currentFactory = self.factory_set.get(pk = factory)
        currentFactory.restart()
        LogBook.objects.create(player = self, message = "Restarted factory in %s"%currentFactory.state.name)
    
    def shutdownPowerPlant(self,powerplant):
        currentPowerPlant = self.powerplant_set.get(pk = powerplant)
        currentPowerPlant.shutdown()
        LogBook.objects.create(player = self, message = "Shutdown Power plant in %s"%currentPowerPlant.state.name)
    
    def restartPowerPlant(self,powerplant):
        currentPowerPlant = self.powerplant_set.get(pk = powerplant)
        currentPowerPlant.restart()
        LogBook.objects.create(player = self, message = "Restarted Power plant in %s"%currentPowerPlant.state.name)
    
    def acceptOffer(self):
        if not hasattr(self, 'Offer'):
            raise ValidationError("No such acquisition")
        self.Offer.full_clean()
    
    def proposeOffer(self,player,amount):
        acqRec = AquireRecord(from_player = self,
                              to_player = Player.objects.get(pk = player),
                              amount = amount)
        acqRec.full_clean()
        acqRec.save()
    
    def cancelProposal(self):
        self.Acquisition.delete()
    
    def rejectOffer(self):
        if not hasattr(self, 'Offer'):
            raise ValidationError("No such acquisition")
        self.Offer.failed()
    
    def acceptEnergyOffer(self,energyOffer):
        offer = self.EnergyOffer.get(pk = energyOffer)
        offer.accept()
    
    def buyEnergy(self,amount_energy):
        glo = GlobalConstants.objects.get()
        if self.capital < amount_energy*glo.energy_selling_price + Decimal(30):
            raise ValidationError("You can't afford it")
        self.capital = F('capital') - amount_energy*glo.energy_selling_price
        self.extra_energy = F('extra_energy') + amount_energy
        self.save()
    
    def proposeEnergyOffer(self,player,amount_energy,amount_money):
        engDeal = EnergyDeal(from_player = Player.objects.get(pk = player),
                            to_player = self,
                            amount_energy = Decimal(amount_energy),
                            cost = amount_money)
        engDeal.full_clean()
        engDeal.save()
    
    def cancelEnergyProposal(self):
        self.EnergyContract.delete()
    
    def rejectEnergyOffer(self,energyOffer):
        offer = self.EnergyOffer.get(pk = energyOffer)
        offer.reject()
    
    def startResearch(self):
        resPro = ResearchProject(player = self,
                                 time_remaining = GlobalConstants.objects.get().initial_research_time*self.research_level)
        resPro.full_clean()
        resPro.save()
        LogBook.objects.create(player = self, message = "Research Project started.")
    
    def endResearch(self):
        if not hasattr(self, 'Research'):
            raise ValidationError("No such Research")
        self.Research.delete()
        LogBook.objects.create(player = self, message = "Research Project Cancelled.")
    
    def takeLoan(self,amount,time, industries):
        time = Decimal(time)
        amount = Decimal(amount)
        loan_amount = amount*(Decimal(100.0)+GlobalConstants.objects.get().loan_interest_rate)/Decimal(100.0)
        currentLoanCreated = LoansCreatedForm({'player':self.id, 'amount':loan_amount/time, 'time_remaining':time, 'mortaged_industries':industries})
        currentLoanCreated.save()
        self.capital = F('capital') + amount
        self.netWorth = F('netWorth') - (loan_amount - amount)
        self.save()
        LogBook.objects.create(player = self, message = "Loan worth %.2f taken"%float(amount))
    
    def payLoan(self,amount):
        if hasattr(self,'Loan'):
            self.Loan.payBack(amount)
    
    def setSellingEnergy(self,val):
        self.selling_energy = val
        self.save()