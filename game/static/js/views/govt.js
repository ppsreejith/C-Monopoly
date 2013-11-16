define(['jquery','lodash','backbone','models/govt'],function($,_,Backbone,Govt){

var LoanView = Backbone.View.extend({
	loan:null,
	factories:[],
	el:'div.insideTile.loans',
	templateEmpty:_.template($("#noloan").html()),
	template:_.template($("#loan").html()),
	events:{
		"change input.payAmount":"payAmountUpdate",
		"change input.viewLoanAmount":"viewLoanAmountUpdate",
		"click div.mortaged_industries.noloan":"toggleSelected",
		"click div.buy.take":"takeLoan",
		"click div.buy.pay":"payLoan",
	},
	toggleSelected:function(ev){
		var el = $(ev.target), sum = 0;
		el.toggleClass("selected");
		el.parent().find("div.mortaged_industries.selected").each(function(index,sel){
			sum += $(sel).data("amount");
		});
		var slider = el.parent().find("input.payAmount");
		slider.attr("max",sum);
		this.payAmountUpdate({target:slider});
	},
	takeLoan:function(ev){
		var ids = [], el = $(ev.target);
		el.parent().find("div.mortaged_industries.selected").each(function(index,sel){
			ids.push($(sel).data("id"));
		});
		var amount = el.parent().find("input.viewLoanAmount").val();
		globalEvent.trigger("take:loan",{ids:ids,amount:amount});
	},
	payLoan:function(ev){
		var el = $(ev.target);
		var amount = el.parent().find("input.viewLoanAmount").val();
		globalEvent.trigger("pay:loan",{amount:amount});
	},
	payAmountUpdate:function(ev){
		var el = $(ev.target);
		el.parent().find("input.viewLoanAmount").val(el.val());
	},
	viewLoanAmountUpdate:function(ev){
		var el = $(ev.target);
		el.parent().find("input.payAmount").val(el.val());
	},
	update:function(){
		
		this.loans.reset();
		(function(that){
		that.loans.fetch({
			success:function(){
				if(that.loans.length == 0)
					globalEvent.trigger("pass:factoryIds",{ids:[]});
				else{
					var factories = that.loans.models[0].attributes.factories;
					globalEvent.trigger("pass:factoryIds",{ids:factories});
				}
			},
		});
		}(this));
		
	},
	initialize:function(){
		this.loans = new Govt.Loans();
		this.update();
		
		(function(that){
		globalEvent.on("passed:factories",function(data){
			that.factories = data.factories;
			that.render();
		});
		}(this));
		
		(function(that){
			globalEvent.on("passed:allFactories",function(data){
				that.factories = data.factories;
				that.renderEmpty();
			});
		}(this));
		
	},
	render:function(){
		this.$el.html(this.template({factories:this.factories,loan:this.loans.models[0].attributes}));
	},
	renderEmpty:function(){
		this.$el.html(this.templateEmpty({factories:this.factories}));
	},
});

var MarketView = Backbone.View.extend({
	el:'div.insideTile.energy',
	market:null,
	templateTop:_.template($("#energyMarketTop").html()),
	template:_.template($("#energyMarket").html()),
	templateButtons:_.template($("#energyMarketButtons").html()),
	events:{
		"click div.buy.propose":"proposeOffer",
		"click div.buy.refresh":"update",
		"click div.energySellerBox":"toggleSelected",
		"change input.onoffswitch-checkbox":"setSellingEnergy",
		},
	setSellingEnergy:function(ev){
		var checkBoxSelected = this.$el.find("input.onoffswitch-checkbox").is(":checked");
		globalEvent.trigger("set:sellingenergy",{value:checkBoxSelected});
	},
	proposeOffer:function(ev){
		var id = this.$el.find("div.energySellerBox.selected").data("id"),
			amount = parseInt(this.$el.find("input.energyMarketInput.energyAmount").val()) || 0,
			cost = parseInt(this.$el.find("input.energyMarketInput.energyCost").val()) || 0;
		globalEvent.trigger("propose:energy",{id:id,amount:amount,cost:cost});
	},
	toggleSelected:function(ev){
		this.$el.find("div.energySellerBox.selected").removeClass("selected");
		$(ev.currentTarget).addClass("selected");
	},
	update:function(){
		var that = this;
		this.market.reset();
		this.market.fetch({success:function(){
			that.render();
		}});
	},
	initialize:function(){
		this.market = new Govt.EnergyMarket();
		this.update();
		(function(that){
		globalEvent.on("updated:user",function(){
			that.renderTop();
		});
		
		globalEvent.on("proposed:offer",function(data){
			that.renderWait();
		});
		}(this));
		this.renderTop();
	},
	renderTop:function(){
		this.$el.find("div.selling_energy_switchBox").html(this.templateTop({selling:settings.user.selling_energy}));
	},
	renderWait:function(){
		this.$el.find("div.market_box").html("<h2 style='color:lightblue;text-align:center;'>You've submitted an offer. Waiting for a response to your offer</h2><br/><div class='buy refresh'>Cancel</div>");
	},
	render:function(){
		var html = "", that = this;
		this.market.each(function(seller){
			html += that.template({seller:seller.attributes});
		});
		html += that.templateButtons();
		this.$el.find("div.market_box").html(html);
	},
});

return {
	LoanView:LoanView,
	MarketView:MarketView,
	};

});