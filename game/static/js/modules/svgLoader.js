require(['jquery','text!'+static_prefix+'images/india.svg!strip'],function($,svg){
	
	var IndustryMap = $("div.industriesInfo > div.indiaMap");
	IndustryMap.html(svg);
	var scale = 1;
	var oldColor = "",oldEl = null;
	IndustryMap.find("path").click(function(event){
		if (this.classList.contains("nostate")){
			return;
		}
		if ($(this).attr("fill") == "yellow"){
			$(this).attr("fill",oldColor);
			scale = 1;
			oldEl = null;
			$(this.parentElement).css({'-webkit-transform':''});
			globalEvent.trigger("change:state",null);
			return;
		}
		$(oldEl).attr("fill",oldColor);
		oldColor = $(this).attr("fill");
		$(this).attr("fill","yellow");
		oldEl = this;
		globalEvent.trigger("change:state",{coordx:$(this).attr("coordx"), coordy:$(this).attr("coordy")});
		var dims = this.getBoundingClientRect(),parent = $(this.parentElement),
					parentDims = this.parentElement.getBoundingClientRect(),
					actualDims = this.getBBox();
		var left = dims.left +dims.width/2, top = dims.top + dims.height/2;
		var center = {left:parentDims.left + parentDims.width/2, top:parentDims.top + parentDims.height/2};
		var x = center.left - left, y = center.top - top;
		x = x/scale, y = y/scale;
		var scaleW = IndustryMap.width()/actualDims.width, scaleY = IndustryMap.height()/actualDims.height;
		scale = Math.min(scaleW,scaleY);
		parent.css({'-webkit-transform':'scale('+scale+') translate('+x+'px,'+y+'px)'});
	});
	
	
});