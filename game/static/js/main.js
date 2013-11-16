requirejs.config({
    baseUrl: settings.static_prefix+"js/",
    paths: {
        'jquery': ['libs/jquery.min','http://ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min'],
        'lodash': 'libs/lodash.min',
        'domReady':'libs/domReady.min',
        'text':'libs/text.min',
        'backbone': 'libs/backbone.min',
        'jsfxlib' : 'libs/jsfxlib.min',
    },
    shim: {
        'backbone': {
	    deps:['lodash','jquery'], 
	    exports: 'Backbone'
	},
	'lodash': {
	    exports: '_'
	}
    }
});

// Event Loaders, Dom Interaction
require(['jquery','domReady','backbone','models/state','models/industry','models/transport','text!templates.html'],
		function($,domReady,Backbone,States,Industries,Transports,templates){
	
	$(document.body).append(templates);
	
	// A global event. Can be referenced anywhere in the code.
	// Use like: globalEvent.trigger("some:event",{key:value});
	// and also: globalEvent.on("some:event",function(data){});
	globalEvent = {}
	globalEvent = _.extend({}, Backbone.Events);
	
	// All app related functions will be used here.
	App = {}
	App.States = new States(settings.states);
	App.ProductIndustries = new Industries.ProductIndustries(settings.productIndustries);
	App.EnergyIndustries = new Industries.EnergyIndustries(settings.energyIndustries);
	App.Transports = new Transports.Transports(settings.transports);
	
	//Page load
    domReady(function(){
    	
    	// Url routing, Actions and SVG Loading. triggers change:state or change:transportState when state is changed.
    	require(['modules/routes','modules/svgLoader','modules/actions'],function(router, highlight){
    		App.router = router;
    		App.highlight = highlight;
    	});
    	
    	// Main stuff
    	require(['views/state','views/user','views/plant','views/transport','views/govt','views/office','views/rank'],
    			function(StateView,User,PlantView,Transports,Govt,Office,Rank){
    		var state = new StateView();
    		var gameDate = new User.GameDate();
    		var office = new Office.HistoryView();
    		var accountsView = new Office.AccountsView();
    		var plant = new PlantView();
    		var transport = new Transports.TransportView();
    		var myTransport = new Transports.MyTransportView();
    		var loan = new Govt.LoanView();
    		var market = new Govt.MarketView();
    		var user = new User.UserView();
    		var ranks = new Rank.Ranks();
    	});
    	
    	// Other boring event listeners and triggers
    	require(['modules/effects']);
    	
    	
    });
    return {};
});