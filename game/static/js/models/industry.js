define(['backbone'], function(Backbone){
	
	var ProductIndustry = Backbone.Model.extend({
		defaults:{
			name:"",
			carbon_per_unit:0,
			initial_cost:0,
			cost_price:0,
			energy_per_unit:0,
			states:[],
			research_level:0,
			maintenance_cost:0,
			maintenance_energy:0,
			unit:"",
		},
	});
	
	var ProductIndustries = Backbone.Collection.extend({
		model: ProductIndustry,
		
		comparator:function(model){
			return -1*model.get('initial_cost');
		},
	});
	
	var EnergyIndustry = Backbone.Model.extend({
		defaults:{
			name:"",
			carbon_per_unit:0,
			initial_cost:0,
			states:[],
			research_level:0,
			maintenance_cost:0,
			output:0,
		},
	});
	
	var EnergyIndustries = Backbone.Collection.extend({
		model: EnergyIndustry,
		
		comparator:function(model){
			return -1*model.get('initial_cost');
		},
	});
	
	return {
		ProductIndustries : ProductIndustries,
		EnergyIndustries : EnergyIndustries,
	}
	
});