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
		assignView:$('div.assignScreen'),
		detailTemplate:_.template($("#myTransportInfo").html()),
		assignTemplate:_.template($("#myAssignInfo").html()),
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
			globalEvent.on("assign:transport",function(data){
				that.renderAssign(data.factory.attributes);
			});
			globalEvent.on("view:transport",function(data){
				that.renderDetails(data.id);
				App.router.navigate("game/transports",{trigger:true});
			});
			this.assignView.on("click","div.detailScreenInfo ul > li",function(ev){
				var id =$(ev.target).data("id"), state_id =$(ev.target).data("state");
				that.renderDetails(id);
				var state = App.States.findWhere({id:state_id}).attributes;
				$("div.transportsMap").find("svg").find("path[coordx="+state.coordx+"][coordy="+state.coordy+"]").attr("class","availableState chosenState");
				$(ev.target).parent().find("li.chosenState").removeClass("chosenState");
				$(ev.target).addClass("chosenState");
			});
		},
		renderDetails:function(id){
			var attrs = this.transports.findWhere({id:id}).attributes;
			var states = _.map(App.States.getStates(attrs['states']),function(state){ return state.attributes; });
			App.highlight(states,true,true);
			this.detailView.html(this.detailTemplate(attrs));
			(function(id,that){
				that.detailView.find("div.buy.sell").click(function(ev){
					globalEvent.trigger("sell:transport",{id:id});
				});
			})(id,this);
		},
		renderAssign:function(factory){
			var state = factory.state.id, attrs = {};
			var transports = this.transports.filter(function(transport){
				return (transport.attributes.states.indexOf(state) > -1);
			});
			if (transports.length == 0){
				this.assignView.find("div.detailScreenInfo").html("<div class='detailBox'><h1>No transports available for this factory</h1></div>");
				this.assignView.show();
				return;
			}
			attrs['transports'] = transports;
			attrs['factory'] = factory;
			this.assignView.find("div.detailScreenInfo").html(this.assignTemplate(attrs));
			this.assignView.find("div.detailScreenInfo").find("div.buy.choose").click(function(ev){
				var chosen = $(ev.target).parent().find("li.chosenState");
				if(chosen.length == 0){
					return;
				}
				var data = {factory:chosen.data("factory"), transport:chosen.data("id")};
				globalEvent.trigger("assigned:transport",data);
			});
			this.assignView.show();
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