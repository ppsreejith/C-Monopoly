define(['backbone'], function(Backbone){
	
	var Transport = Backbone.Model.extend({
		defaults:{
			name:"",
			initial_cost:0,
			states:[],
			travel_rate:0,
			stopping_cost:0,
			max_stops:0,
			energy_rate:0,
			carbon_cost_rate:0,
		},
	});
	
	var Transports = Backbone.Collection.extend({
		model:Transport,
	});
	
	var CreatedTransport = Backbone.Model.extend({
		defaults:{
			transport:null,
			states:[],
			distance:0,
		},
	});
	
	var CreatedTransports = Backbone.Collection.extend({
		model:CreatedTransport,
		
		parse:function(response){
			var transport = null;
			for (i in response){
				transport = App.Transports.findWhere({id:response[i].transport_id});
				if (transport != null)
					response[i].transport = transport.attributes;
			}
			return response;
		},
		url:'/api/transports',
	});
	
	return {
		Transports:Transports,
		CreatedTransports:CreatedTransports,
		};
});