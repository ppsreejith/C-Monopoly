define(['backbone'], function(Backbone){
	
	var Player = Backbone.Model.extend({
	    defaults: {
		"rank":0,
		"username":settings.user.username,
		"capital":0,
		"netWorth":0,
	    },
	});
	
	var User = Player.extend({
		url:'/api/user',
	});

	var Leaderboard = Backbone.Collection.extend({
	    model:Player,
	    url:'/api/leaderboard',
	    
	    comparator:function(model){
	    	return model.get('rank');
	    },
	});
	
	var GameDate = Backbone.Model.extend({
		defaults:{
			current_day:1,
			current_month:1,
			current_year:1970,
		},
		url:'/api/date',
	});
	
	return {
		Leaderboard: Leaderboard,
		Player: Player,
		User: User,
		GameDate: GameDate,
	};
});