(function(){
    orbital = this;

    var host = 'ws://' + window.location.host + '/';
    var maxLayers = 60;
    var dateKeyFunc = function(){
        return new Date().getMinutes();
    };
    var lastDateKey = null;
    var element = null;
    var layers = [];
    var activeLayer;
    var adjustOffset = 0;
    var targetHeight = 1800;
    var targetWidth = 3600;
    var setHeight;
    var setWidth;
    var currentData = [];
    var lastMessage = null;

    function sizePageElements() {
        var $geo = $("#geo");
        $geo.css("height", $("body").height() - adjustOffset);
        if ($geo.width() / $geo.height() > 2) {
            orbital.scale = $geo.height() / targetHeight;
        } else {
            orbital.scale = $geo.width() / targetWidth;
        }
        element.css({
            "top": $geo.height() - targetHeight * orbital.scale,
            "left": ($geo.width() - targetWidth * orbital.scale) / 2
        });

        setWidth = element.width();
        setHeight = element.height();

        $('#mapdata').css({
            "-moz-transform": "scale(" + orbital.scale + ")",
            "-webkit-transform": "scale(" + orbital.scale + ")",
            "-ms-transform": "scale(" + orbital.scale + ")",
            "-o-transform": "scale(" + orbital.scale + ")"
        });
        $("canvas").css({
            width: setWidth + "px",
            height: setHeight + "px"
        });
        $("canvas").attr('width', setWidth);
        $("canvas").attr('height', setHeight);
    }

    orbital.addMessage = function(data, x, y){
        if (lastMessage) {
            return;
        }

        var post = data.post;

        lastMessage = $('<div class="overlay">' +
          '<img class="avatar" src="' + post.avatar_url + '"/>' +
          '<img src="http://disqus.com/api/forums/favicons/' + post.forum_id + '.jpg" class="favicon"/>' +
          '<h2 class="title">' + post.thread_title + '</h2>' +
          '<p class="message"><strong class="author">' + post.author_name + '</strong> <strong class="location">' + data.loc + '</strong></p>' +
          '</div>').hide().appendTo(element).css({
            'left': x,
            'top': y
        }).show();

        setTimeout(function(){
            lastMessage.fadeOut('fast', function(){
                lastMessage.remove();
                lastMessage = null;
            });
        }, 3000);
    };

    orbital.addData = function(data) {
        var x = ~~((parseFloat(data.lng) + 180) * 10) * orbital.scale,
            y = ~~((-parseFloat(data.lat) + 90) * 10) * orbital.scale;

        // render and animate our point
        var point = jc.circle(x, y,
            5, "rgba(255, 255, 255, 1)", 1)
          .animate({radius:1, opacity:0.4}, 700, function(){
              point.del();
              activeLayer.fillStyle = "rgba(255, 255, 255, 0.2)";
              activeLayer.beginPath();
              activeLayer.arc(x, y, 1, 0, Math.PI * 2, false);
              activeLayer.fill();
          });

        this.addMessage(data, x, y);
    };

    orbital.connect = function(){
        orbital.socket = new WebSocket(host);
        orbital.socket.onclose = function(e){
            setTimeout(function(){
                orbital.connect();
            }, 3000);
        };
        orbital.socket.onmessage = function(msg){
            var data = JSON.parse(msg.data);
            orbital.addData(data);
        };
    };

    orbital.createLayer = function(dateKey){
        var layer = $('<canvas data-date-key="' + dateKey + '"></canvas>').css({
            width: setWidth + 'px',
            height: setHeight + 'px'
        }).attr({
            width: setWidth,
            height: setHeight
        });
        element.append(layer);
        layers.push(layer);

        return layer;
    };

    orbital.watchActiveLayer = function() {
        dateKey = dateKeyFunc();

        if (dateKey == lastDateKey) {
            setTimeout(orbital.watchActiveLayer, 3000);
            return;
        }

        lastDateKey = dateKey;

        // create a new layer
        layer = orbital.createLayer(dateKey);

        // set the new layer as the active layer
        activeLayer = layer[0].getContext("2d");

        // remove excess layers
        var excess = layers.slice(maxLayers, layers.length);
        orbital.layers = layers.slice(0, maxLayers);
        for (var i=0; i<excess.length; i++) {
            console.log('Removing layer ( ' + excess[i].attr('data-date-key') + ' )');
            excess[i].remove();
        }

        setTimeout(orbital.watchActiveLayer, 3000);
    };

    orbital.init = function(el) {
        element = el;

        sizePageElements();

        jc.start('pings', true);

        orbital.watchActiveLayer();

        orbital.connect();
    };
})();
