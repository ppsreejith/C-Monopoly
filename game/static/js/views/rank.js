define(['jquery','lodash','backbone','models/user'],function($,_,Backbone,User){

var Ranks = Backbone.View.extend({
	ranks:null,
	el:'div.detailBox.leaderboard',
	template:_.template($("#leaderboardTemplate").html()),
	initialize:function(){
		this.ranks = new User.Leaderboard();
		var that = this;
		this.ranks.fetch({
			success:function(){
				that.render();
			}
		});
	},
	render:function(){
		var ranks = this.ranks.map(function(model){
			return model.attributes;
		});
		this.$el.html(this.template({ranks:ranks}));
	},
});

return {
		Ranks:Ranks
	};

});