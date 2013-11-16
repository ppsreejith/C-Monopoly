define(['jquery','lodash','backbone','models/govt'],function($,_,Backbone,Govt){
	function drawChart(dataC){
        var data = google.visualization.arrayToDataTable(dataC);

        var options = {
          title: 'NetWorth and Capital Fluctuations',
          'backgroundColor':'white',
        };

        var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
        chart.draw(data, options);
	}
	
	var HistoryView = Backbone.View.extend({
		el:'div.insideTile.history',
		history:[],
		initData:function(){
			var data = [];
			data.push(["Day","Net Worth","Capital"]);
			data.push(["1",settings.user.netWorth,settings.user.capital]);
			data.push(["2",settings.user.netWorth,settings.user.capital]);
			this.history = data;
		},
		update:function(){
			
			(function(that){
				$("li[name=history]").on("click",function(){
					that.render();
					$(this).off("click",arguments.callee);
				});
			}(this));
			
			var last = this.history.slice(-1)[0];
			if (settings.user.netWorth == last[1] && settings.user.capital == last[2]){
				return;
			}
			this.history.push([""+(parseInt(last[0])+1), settings.user.capital, settings.user.netWorth]);
			localStorage.data = JSON.stringify(this.history);
			
		},
		initialize:function(){
			(function(that){
				globalEvent.on("updated:user",function(){
					if(localStorage.data == null){
						that.initData();
					}
					else{
						that.history = JSON.parse(localStorage.data);
					}
					that.update();
				});
			}(this));
		},
		render:function(){
			drawChart(this.history);
			this.$el.css({background:"white"});
		},
	});
	
	var AccountsView = Backbone.View.extend({
		el:'ul.accountsList.list',
		logBook:null,
		initialize:function(){
			this.logBook = new Govt.LogBook();
			this.update();
		},
		update:function(){
			this.logBook.reset();
			(function(that){
				that.logBook.fetch({success:function(){
					that.render();
				}});
			}(this));
		},
		render:function(){
			this.$el.html( "<li>"+this.logBook.pluck('message').join("</li><li>")+"</li>" );
		},
	});
	
	return {
		HistoryView: HistoryView,
		AccountsView: AccountsView,
	};
	
});