define(['backbone'],function(Backbone){
	globalEvent.on("buy:product",function(data){
		console.log(data);
	});
	globalEvent.on("buy:energy",function(data){
		console.log(data);
	});
	globalEvent.on("change:factoriesprice",function(data){
		console.log(data);
	});
	globalEvent.on("change:powerplantsprice",function(data){
		console.log(data);
	});
	globalEvent.on("sell:factories",function(data){
		console.log(data);
	});
	globalEvent.on("sell:powerplants",function(data){
		console.log(data);
	});
	globalEvent.on("toggle:factories",function(data){
		console.log(data);
	});
	globalEvent.on("toggle:powerplants",function(data){
		console.log(data);
	});
	globalEvent.on("buy:transport",function(data){
		console.log(data);
	});
	globalEvent.on("sell:transport",function(data){
		console.log(data);
	});
	globalEvent.on("assigned:transport",function(data){
		console.log(data);
	});
});