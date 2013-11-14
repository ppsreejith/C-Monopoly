define(['jquery','lodash','backbone','models/user'],function($,_,Backbone, User, Plant){

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

return UserView;

});