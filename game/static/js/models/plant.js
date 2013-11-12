define(['backbone'], function(Backbone){

	var Factory = Backbone.Model.extend({
		defaults:{
			type:null,
			state:0,
			transport:null,
			selling_price:0,
			actual_value:0,
			products_last_day:0,
			shut_down:false,
		}
		
	});
	
	var Factories = Backbone.Collection.extend({
		model: Factory,
		url:'/api/factories',
		parse:function(response){
			var product = null;
			for (i in response){
				product = App.ProductIndustries.findWhere({id:response[i].type_id});
				if (product != null)
					response[i].type = product.attributes;
				state = App.States.findWhere({id:response[i].state_id});
				if (state != null)
					response[i].state = state.attributes;
			}
			return response;
		},
		comparator:function(model){
			return -1*model.get('actual_value');
		},
	});
	
	var Powerplant = Backbone.Model.extend({
		defaults:{
			type:{},
			state:{},
			actual_value:0,
			shut_down:false,
		},
	});
	
	var Powerplants = Backbone.Collection.extend({
		model: Powerplant,
		url:'/api/powerplants',
		
		parse:function(response){
			var energy = null;
			for (i in response){
				energy = App.EnergyIndustries.findWhere({id:response[i].type_id});
				if (energy != null)
					response[i].type = energy.attributes;
				state = App.States.findWhere({id:response[i].state_id});
				if (state != null)
					response[i].state = state.attributes;
			}
			return response;
		},
		comparator:function(model){
			return -1*model.get('actual_value');
		},
	});
	
	return {
		Factories : Factories,
		Powerplants : Powerplants
	};
});