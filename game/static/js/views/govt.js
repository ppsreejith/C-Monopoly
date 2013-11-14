define(['jquery','lodash','backbone','models/govt'],function($,_,Backbone,Govt){

var LoanView = Backbone.View.extend({
	loan:null,
	factories:[],
	templateEmpty:_.template($("#noloan").html()),
	template:_.template($("#loan").html()),
	el:'div.govtTile.loans',
	events:{
		"click input.payAmount":"payAmountUpdate",
	},
	payAmountUpdate:function(ev){
		var el = $(ev.target);
		el.parent().find("input.viewLoanAmount").val(el.val());
	},
	update:function(){
		
		this.loans.reset();
		(function(that){
		that.loans.fetch({
			success:function(){
				if(that.loans.length == 0)
					globalEvent.trigger("pass:factoryIds",{ids:[]});
				else{
					var factories = that.loans.models[0].get('factories');
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
		this.$el.html(this.template({factories:this.factories,loan:this.loans.at(0).attributes}));
	},
	renderEmpty:function(){
		this.$el.html(this.templateEmpty(this.factories));
	},
});

return {
	LoanView:LoanView,
	
	};

});