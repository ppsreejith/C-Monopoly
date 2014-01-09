require(['jquery'],function($){
	
	/*$("nav.gameNavigation").on("click","a",function(){
		$(this).parent().find("a.navSelected").removeClass("navSelected");
		$(this).addClass("navSelected");
	});*/
	$("nav.gameNavigation").find("a[href='"+location.hash+"']").addClass("navSelected");
	globalEvent.on("wait:wait",function(data){
		console.log(data);
		$("div.cover").show();
	});
	globalEvent.on("resume:resume",function(data){
		console.log(data);
		$("div.cover").hide();
	});
	$("div.govtInfo, div.officeInfo").find("ul.insideNav > li").click(screenAnimation);
	$("div.bigWrapper").css({opacity:1});
	$("img.splashScreen").css({opacity:0});
	
	function screenAnimation(ev){
		var target = $(ev.target);
		var name = target.attr("name"), parent = $(ev.target).parent().parent().parent();
		target.parent().find("li.selected").removeClass("selected");
		target.addClass("selected");
		parent.find("div.insideTile.active").removeClass("active");
		parent.find("div.insideTile."+name).addClass("active");
	}
	
	//return true;
});