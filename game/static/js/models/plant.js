define(['backbone'], function(Backbone){

	var Factory = Backbone.Model.extend({
		defaults:{
			type:0,
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
		
		comparator:function(model){
			return -1*model.get('actual_value');
		},
	});
	
	var Powerplant = Backbone.Model.extend({
		defaults:{
			type:0,
			state:0,
			actual_value:0,
			shut_down:false,
		}
	});
	
	var Powerplants = Backbone.Collection.extend({
		model: Powerplant,
		url:'/api/powerplants',
		
		comparator:function(model){
			return -1*model.get('actual_value');
		},
	});
	
	return {
		Factories : Factories,
		Powerplants : Powerplants
	};
});