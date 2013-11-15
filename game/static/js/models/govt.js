define(['backbone'], function(Backbone){
	var Loan = Backbone.Model.extend({
		defaults:{
			amount:0,
			time:0,
			factories:[],
		},
	});
	
	var Loans = Backbone.Collection.extend({
		model:Loan,
		url:'/api/loans',
	});
	
	var Log = Backbone.Model.extend({
		defaults:{
			message:"",
			id:0,
		},
	});
	
	var LogBook = Backbone.Collection.extend({
		model: Log,
		url:'/api/logbook',
	});
	
	var EnergyTrader = Backbone.Model.extend({
		defaults:{
			user__username:"",
			extra_energy:"",
			rank:0,
		},
	});
	
	var EnergyMarket = Backbone.Collection.extend({
		model: EnergyTrader,
		url:'/api/energymarket',
		comparator:function(model){
			return model.get('rank');
		},
	});
	
	return {
		Loans:Loans,
		LogBook:LogBook,
		EnergyMarket:EnergyMarket,
	};
});