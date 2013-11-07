requirejs.config({
    baseUrl: static_prefix+"js/",
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

//Event Loaders, Dom Interaction
require(['jquery','domReady','backbone',],function($,domReady,Backbone){

	//A global event. Can be referenced anywhere in the code.
	// Use like: globalEvent.trigger("some:event",{key:value});
	// and also: globalEvent.on("some:event",function(data){});
	globalEvent = {}
	globalEvent = _.extend({}, Backbone.Events);
	
	//Page load
    domReady(function(){
    	
    	//Url routing and SVG Loading. triggers change:state when state is changed.
    	require(['modules/routes','modules/svgLoader']);
    	
    	//Other boring event listeners and triggers
    	require(['modules/effects']);
    	
    	globalEvent.on("change:state",function(data){console.log(data);});
    });
    return {};
});