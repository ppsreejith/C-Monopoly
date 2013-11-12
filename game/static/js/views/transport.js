define(['jquery','lodash','backbone','models/transport'],function($,_,Backbone,Transport){
	
	var TransportView = Backbone.View.extend({
		el:'div.transportList',
		template:_.template($("#transportListTemplate").html()),
		detailTemplate:_.template($("#transportInfo").html()),
		detailView:$('div.transportDetail'),
		events:{
			"click ul.Transports > li":"transportInfo",
		},
		transportInfo:function(ev){
			var id = $(ev.target).data("id");
			this.renderDetails(id);
		},
		initialize:function(){
			this.render();
		},
		renderDetails:function(id){
			var attrs = App.Transports.findWhere({id:id}).attributes;
			var states = _.map(App.States.getStates(attrs['states']),function(state){ return state.attributes; });
			App.highlight(states);
			this.detailView.html(this.detailTemplate(attrs));
			this.detailView.find("div.buy").click(function(ev){
				var data = _.map($("path[class='availableState takenState']"),function(path){
					return {coordx:parseInt($(path).attr("coordx")), coordy:parseInt($(path).attr("coordy"))}
				});
				globalEvent.trigger("buy:transport",{data:data});
			});
		},
		render:function(){
			var transports = App.Transports.map(function(transport){
				return transport.attributes;
			});
			this.$el.html(this.template({transports:transports}));
		},
	});
	
	var MyTransportView = Backbone.View.extend({
		el:'div.myTransports',
		template:_.template($("#myTransportsList").html()),
		transports:null,
		detailView:$('div.transportDetail'),
		detailTemplate:_.template($("#myTransportInfo").html()),
		events:{
			"click ul.Transports > li":"transportInfo",
		},
		transportInfo:function(ev){
			var id = $(ev.target).data("id");
			this.renderDetails(id);
		},
		initialize:function(){
			var that = this;
			this.transports = new Transport.CreatedTransports();
			this.transports.fetch({success:function(){
				that.render();
			}});
		},
		renderDetails:function(id){
			var attrs = this.transports.findWhere({id:id}).attributes;
			var states = _.map(App.States.getStates(attrs['states']),function(state){ return state.attributes; });
			App.highlight(states,true,true);
			this.detailView.html(this.detailTemplate(attrs));
			(function(id,that){
				that.detailView.find("div.buy").click(function(ev){
					globalEvent.trigger("sell:transport",{id:id});
				});
			})(id,this);
		},
		render:function(){
			var transports = this.transports.map(function(transport){
				return transport.attributes;
			});
			this.$el.html(this.template({transports:transports}));
		},
	});
	
	return {
		TransportView:TransportView,
		MyTransportView:MyTransportView
		};
});