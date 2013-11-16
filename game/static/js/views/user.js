define(['jquery','lodash','backbone','models/user'],function($,_,Backbone, User){

var UserView = Backbone.View.extend({
    els:$('div.userInfo'),
    user:null,
    template:_.template($("#userTemplate").html()),
    update:function(){
    	var that = this;
    	this.user.fetch({success:function(){
    		settings.user = that.user.attributes;
    		$("div.notifBar").find("span").find("span").html(settings.user.user__username);
    		that.render();
    		globalEvent.trigger("updated:user",{});
    	}});
    },    
    initialize:function(){
    	this.user = new User.User();
    	this.update();
    },
    render:function(){
    	this.els.html(this.template(this.user.attributes));
    },
});

var GameDate = Backbone.View.extend({
	date:null,
	el:'div.gameDate',
	initialize:function(){
		this.date = new User.GameDate();
		(function(that){
			that.date.fetch({success:function(){
				settings.date = that.date.attributes;
				that.render();
				globalEvent.trigger("updated:date");
			}});
		}(this));
	},
	render:function(){
		var d = this.date.attributes,
			months = ["January","February","March","April","May","June","July","August","September","October","November","December"];
		this.$el.html(months[d.current_month-1]+" &nbsp;"+d.current_day+" &nbsp;"+d.current_year);
	},
});

return {
	UserView:UserView,
	GameDate:GameDate,
	};

});