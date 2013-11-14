define(['backbone'], function(Backbone){
	var Loan = Backbone.Model.extend({
		defaults:{
			amount:0,
			time:0,
			industries:[],
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
	
	return {
		Loans:Loans,
		LogBook:LogBook,
	};
});