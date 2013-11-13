define(['jquery','backbone'],function($,Backbone){
	var Urls = Backbone.Router.extend({

        routes: {
            "" : "game",
            "game" : "game",
            "game/:option" : "changeInfo",
            "rules" : "rules",
            "about" : "about",
        },
        
        switchTo:function(option){
        	$("div.mainScreen.active").removeClass("active");
            $("div.mainScreen."+option+"Screen").addClass("active");
        },
        
        gameSwitchTo:function(option){
        	this.switchTo("game");
        	var nav = $("nav.gameNavigation"), url = "#game/"+option;
        	nav.find("a.navSelected").removeClass("navSelected");
        	nav.find("a[href='"+url+"']").addClass("navSelected");
        	$("div.screenInfo.active").removeClass("active");
            $("div.screenInfo."+option+"Info").addClass("active");
        },
        
        game:function(){
            this.gameSwitchTo("industries");
        },
        changeInfo:function(option){
        	this.gameSwitchTo(option);
        },
        rules:function(){
        	this.switchTo("rules");
        },
        about:function(){
        	this.switchTo("about");
        }

    });
	var urlRouter = new Urls();
	Backbone.history.start();
	
	return urlRouter;
});