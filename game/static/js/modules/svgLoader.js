define(['jquery','text!'+settings.static_prefix+'images/india.svg!strip'],function($,svg){
	
	//Industries map
	;(function(){
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
		globalEvent.trigger("change:state",App.States.findWhere({coordx:parseInt($(this).attr("coordx")), coordy:parseInt($(this).attr("coordy"))}));
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
	}());
	
	//Tranports map
	var highlight = (function(){
	var transportsMap = $("div.transportsInfo > div.transportsMap");
	transportsMap.html(svg);
	transportsMap.on("click","path[class=availableState], path[class='availableState takenState']",function(ev){
		var el = $(ev.target);
		var set = el.attr("class") == "availableState";
		var data = {coordx:el.attr("coordx"),coordy:el.attr("coordy")};
		highlight(data,set);
	});
	function highlight(vals, set, taken){
		set = set || false;
		taken = taken || false;
		var className = "", query = [];
		className = set?"availableState takenState":"availableState";
		if (taken == true) className = "takenState";
		vals = vals || {};
		if($.isEmptyObject(vals)){
			transportsMap.find("path.availableState").attr("class","");
		}
		else if ($.isArray(vals)){
			transportsMap.find("path.availableState").attr("class","");
			transportsMap.find("path.takenState").attr("class","");
			$.each(vals,function(index, value){
				query.push("path[coordx="+value.coordx+"][coordy="+value.coordy+"]");
			});
			transportsMap.find(query.join(",")).attr("class",className);
		}
		else if (vals.hasOwnProperty("coordx") && vals.hasOwnProperty("coordy")){
			transportsMap.find("path[coordx="+vals.coordx+"][coordy="+vals.coordy+"]").attr("class",className);
		}
		globalEvent.trigger("change:transportState",App.States.where(vals));
	}
	
		return highlight;
	}());
	
	return highlight;
});