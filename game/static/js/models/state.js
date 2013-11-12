define(['lodash','backbone'],function(_,Backbone){

	var State = Backbone.Model.extend({
		defaults:{
			name: "",
			coordx:0,
			coordy:0,
			population:0,
			income:0,
			research_level:0,
			growth_rate:0,
			income_growth_rate:0,
			id:0,
		},
		findProductIndustries:function(){
			var id = this.id;
			if (this.products != null) //Lazy loading
				return this.products;
			this.products = App.ProductIndustries.filter(function(model){
				return (model.get('states').indexOf(id) > -1);
			});
			return this.products;
		},
		findEnergyIndustries:function(){
			var id = this.id;
			if (this.energies != null) //Lazy loading
				return this.energies;
			this.energies = App.EnergyIndustries.filter(function(model){
				return (model.get('states').indexOf(id) > -1);
			});
			return this.energies;
		},
	});
	
	var States = Backbone.Collection.extend({
		model:State,
		getStates:function(ids){
			return this.filter(function(model){
				return (ids.indexOf(model.get('id')) > -1);
			});
		},
	});
	
	return States;

});