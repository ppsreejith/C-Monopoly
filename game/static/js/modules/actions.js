define(['backbone'],function(Backbone){
	globalEvent.on("buy:product",function(data){
		console.log(data);
	});
	globalEvent.on("buy:energy",function(data){
		console.log(data);
	});
});