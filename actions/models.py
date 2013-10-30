from player.models import Player, LogBook, ResearchProject
from transport.forms import TransportCreatedForm
from energy.models import EnergyIndustry, PowerPlant
from govt.models import State, AquireRecord, EnergyDeal
from industry.models import ProductIndustry, Factory
from django.core.exceptions import ValidationError
from game.models import GlobalConstants
from industry.forms import LoansCreatedForm
from django.db.models import F

#Main game profile class. Proxy for Player class
class Profile(Player):
    class Meta:
        proxy = True
    
    def buy_transport(self, transport, states):
        created_transport = TransportCreatedForm({'player':self.id, 'transport':transport, 'states':states})
        ct = created_transport.save()
        self.capital = F('capital') - ct.type.initial_cost
        self.save()
        LogBook.objects.create(player = self, message = "Bought Transport for Rs. %.2f Million."%ct.type.initial_cost)
    
    def sell_transport(self, transportcreated):
        ct = self.transportcreated_set.get(pk = transportcreated)
        amount = ct.type.initial_cost*0.8
        self.capital = F('capital') + amount
        ct.delete()
        self.save()
        LogBook.objects.create(player = self, message = "Sold Transport for Rs. %.2f Million."%amount)

    def buy_powerPlant(self,industry,state):
        currentIndustry = EnergyIndustry.objects.get(pk = industry)
        currentState = State.objects.get(pk = state)
        currentPowerPlant = PowerPlant(type = currentIndustry, 
                                state = currentState,
                                player = self,
                                actual_value = currentIndustry.initial_cost*0.9)
        currentPowerPlant.full_clean()
        currentPowerPlant.save()
        self.capital = F('capital') - currentIndustry.initial_cost
        self.save()
        LogBook.objects.create(player = self, message = "Bought Power plant for Rs. %.2f Million."%currentIndustry.initial_cost)
    
    def sell_powerPlant(self, powerPlant):
        currentPowerPlant = self.factory_set.get(pk = powerPlant)
        amount = currentPowerPlant.actual_value
        currentPowerPlant.delete()
        self.capital = F('capital') + amount
        self.save()
        LogBook.objects.create(player = self, message = "Sold Power plant for Rs. %.2f Million."%amount)
    
    def buy_factory(self,industry,state):
        currentIndustry = ProductIndustry.objects.get(pk = industry)
        currentState = State.objects.get(pk = state)
        factory = Factory(type = currentIndustry, 
                          state = currentState, 
                          player = self,
                          selling_price = 1.2*float(currentIndustry.cost_price),
                          actual_value = float(currentIndustry.initial_cost)*0.9)
        factory.full_clean()
        factory.save()
        self.capital = F('capital') - currentIndustry.initial_cost
        self.save()
        LogBook.objects.create(player = self, message = "Bought Factory for Rs. %.2f Million."%currentIndustry.initial_cost)
    
    def sell_factory(self, factory):
        currentFactory = self.factory_set.get(pk = factory)
        amount = currentFactory.actual_value
        currentFactory.delete()
        self.capital = F('capital') + amount
        self.save()
        LogBook.objects.create(player = self, message = "Sold Factory for Rs. %.2f Million."%amount)
    
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
    
    def proposeEnergyOffer(self,player,amount_energy,amount_money):
        engDeal = EnergyDeal(from_player = Player.objects.get(pk = player),
                            to_player = self,
                            amount_energy = float(amount_energy),
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
        LogBook.objects.create(player = self.player, message = "Research Project started.")
    
    def endResearch(self):
        if not hasattr(self, 'Research'):
            raise ValidationError("No such Research")
        self.Research.delete()
        LogBook.objects.create(player = self.player, message = "Research Project Cancelled.")
    
    def takeLoan(self,amount,time, industries):
        loan_amount = amount*(100.0+float(GlobalConstants.objects.get().loan_interest_rate))/100.0
        currentLoanCreated = LoansCreatedForm({'player':self.id, 'amount':float(loan_amount)/time, 'time_remaining':time, 'mortaged_industries':industries})
        currentLoanCreated.save()
        self.capital = F('capital') + amount
        self.save()
    
    def payLoan(self,amount):
        if hasattr(self,'Loan'):
            self.Loan.payBack(amount)
    
    def setSellingEnergy(self,val):
        self.selling_energy = val
        self.save()