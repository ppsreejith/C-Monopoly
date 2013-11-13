define(['jquery','lodash','backbone','models/plant'],function($,_,Backbone, Plant){

	var PlantView = Backbone.View.extend({
		el:'div.userIndustriesInfo',
		factories:null,
		detailEl:$("div.detailScreen"),
	    state:null,
	    currentFactories:[],
	    powerplants:null,
	    currentPowerplants:[],
	    template:_.template($("#plantTemplate").html()),
	    events:{
			"click ul.ProductIndustriesList > li":"productInfo",
			"click ul.EnergyIndustriesList > li":"energyInfo",
		},
		productInfo:function(ev){
			this.renderInfo("Factories",ev);
		},
		energyInfo:function(ev){
			this.renderInfo("Powerplants",ev);
		},
		renderInfo:function(type,ev){
			var id = $(ev.target).data("id"), typeL = type.toLowerCase();
			var attr = this[typeL].findWhere({id:id}).attributes;
			attr['statuscolor'] = attr['shut_down']?'red':'green';
			attr['status'] = attr['shut_down']?'Stopped':'Active';
			attr['halt'] = attr['shut_down']?'Restart':'Halt';
			var template = _.template($("#my"+type+"Details").html());
			this.detailEl.find("div.detailScreenInfo").html(template(attr));
			(function(that,id,typeL,trans_id){
				that.detailEl.find("input.selling_value").change(function(ev){
					$(ev.target).parent().find("span.setPriceButton").show();
				});
				that.detailEl.find("span.setPriceButton").click(function(ev){
					var newSp = $(ev.target).parent().find("input.selling_value").val();
					globalEvent.trigger("change:"+typeL+"price",{id:id,newSp:newSp});
				});
				that.detailEl.find("div.buy.sell").click(function(ev){
					globalEvent.trigger("sell:"+typeL,{id:id});
				});
				that.detailEl.find("div.buy.halt").click(function(ev){
					globalEvent.trigger("toggle:"+typeL,{id:id});
				});
				that.detailEl.find("div.buy.assign").click(function(ev){
					globalEvent.trigger("assign:transport",{factory:that.factories.findWhere({id:id})});
					App.router.navigate("game/transports",{trigger:true});
				});
				that.detailEl.find("div.buy.view").click(function(ev){
					globalEvent.trigger("view:transport",{id:trans_id});
				});
			})(this,id,typeL,attr['transport_id']);
			this.detailEl.show();
		},
	    fetch:function(){
	    	var ready = false, that = this;
	    	this.factories.fetch({success:function(){
	    		ready = ready?that.update():true;
	    	}});
	    	this.powerplants.fetch({success:function(){
	    		ready = ready?that.update():true;
	    	}});
	    },
	    update:function(){
	    	var state = this.state;
	    	if(state == null){
	    		this.currentFactories = this.factories.map(function(factory){return factory.attributes;});
	    		this.currentPowerplants = this.powerplants.map(function(plant){return plant.attributes;});
	    	}
	    	else{
	    		this.currentFactories = _.map(this.factories.where({state_id:state.id}),function(factory){return factory.attributes;});
	    		this.currentPowerplants = _.map(this.powerplants.where({state_id:state.id}), function(plant){return plant.attributes;});
	    	}
	    	this.render();
	    },
	    initialize:function(){
	    	this.factories = new Plant.Factories();
	    	this.powerplants = new Plant.Powerplants();
	    	this.fetch();
	    	var that = this;
	    	globalEvent.on("change:state",function(state){
	    		that.state = state;
	    		that.update();
	    	});
	    },
	    render:function(){
	    	this.$el.html(this.template({products:this.currentFactories,energies:this.currentPowerplants}));
	    },
	});
	
	return PlantView;
	
});
