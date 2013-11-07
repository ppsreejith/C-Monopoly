require(['jquery'],function($){
	
	$("nav.gameNavigation").on("click","a",function(){
		$(this).parent().find("a.navSelected").removeClass("navSelected");
		$(this).addClass("navSelected");
	});
	$("nav.gameNavigation").find("a[href='"+location.hash+"']").addClass("navSelected");
	
	$("div.bigWrapper").css({opacity:1});
	$("img.splashScreen").css({opacity:0});
	//return true;
});