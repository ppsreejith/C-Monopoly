require(['jquery'],function($){
	
	/*$("nav.gameNavigation").on("click","a",function(){
		$(this).parent().find("a.navSelected").removeClass("navSelected");
		$(this).addClass("navSelected");
	});*/
	$("nav.gameNavigation").find("a[href='"+location.hash+"']").addClass("navSelected");
	$("div.govtInfo").find("ul.govtNav > li").click(function(ev){
		var target = $(ev.target);
		var name = target.attr("name"), parent = $(ev.target).parent().parent().parent();
		target.parent().find("li.selected").removeClass("selected");
		target.addClass("selected");
		parent.find("div.govtTile.active").removeClass("active");
		parent.find("div.govtTile."+name).addClass("active");
	});
	$("div.bigWrapper").css({opacity:1});
	$("img.splashScreen").css({opacity:0});
	//return true;
});