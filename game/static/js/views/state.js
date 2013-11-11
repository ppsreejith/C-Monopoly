define(['jquery','lodash','backbone'],function($,_,Backbone){
	
	var StateView = Backbone.View.extend({
		el:'div.stateInfo',
		detailEl:$("div.detailScreen"),
		template:_.template($("#stateTemplate").html()),
		state:null,
		events:{
			"click ul.ProductIndustriesList > li":"productInfo",
			"click ul.EnergyIndustriesList > li":"energyInfo",
		},
		productInfo:function(ev){
			this.renderInfo("Product",ev);
		},
		energyInfo:function(ev){
			this.renderInfo("Energy",ev);
		},
		renderInfo:function(type,ev){
			var id = $(ev.target).data("id"), typeL = type.toLowerCase();
			var stateId = this.state == null?0:this.state.id;
			var template = _.template($("#"+typeL+"InfoTemplate").html());
			var attr = App[type+"Industries"].findWhere({id:id}).attributes;
			attr['currentstate'] = stateId;
			this.detailEl.find("div.detailScreenInfo").html(template(attr));
			if (stateId != 0){
				this.detailEl.find("div.detailScreenInfo > div.detailBox > div.buy").click(function(ev){
					globalEvent.trigger("buy:"+typeL,{type:id,state:stateId});
				});
			}
			this.detailEl.show();
		},
		initialize:function(){
			var that = this;
			globalEvent.on("change:state",function(state){
				that.state = state;
				that.render();
			});
			this.render();
		},
		renderDefault:function(){
			var content = "<h1>All Industries</h1>";
			content+="<ul class='ProductIndustriesList'>";
			App.ProductIndustries.each(function(model){
				content+="<li data-id='"+model.attributes.id+"'>"+model.attributes.name+"</li>";
			});
			content+="</ul>";
			content += "<h1>All Power Plants</h1>";
			content+="<ul class='EnergyIndustriesList'>";
			App.EnergyIndustries.each(function(model){
				content+="<li data-id='"+model.attributes.id+"'>"+model.attributes.name+"</li>";
			});
			content+="</ul>";
			this.$el.html(content);
			
		},
		render:function(){
			if(this.state == null){
				this.renderDefault();
				return;
			}
			var productIndustries = this.state.findProductIndustries(),
				energyIndustries = this.state.findEnergyIndustries();
			var products = productIndustries.map(function(model){ return model.attributes;}),
				energies = energyIndustries.map(function(model){ return model.attributes;});
			this.$el.html( this.template( {state:this.state.attributes, products:products, energies:energies} ));
		},
	});
	
	return StateView;
});