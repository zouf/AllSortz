$.fn.spin = function(opts) {
  this.each(function() {
    var $this = $(this),
        data = $this.data();

    if (data.spinner) {
      data.spinner.stop();
      delete data.spinner;
    }
    if (opts !== false) {
      data.spinner = new Spinner($.extend({color: $this.css('color')}, opts)).spin(this);
    }
  });
  return this;
};

(function($) {
    $(document).ready(function(){
        $("a.endless_more").live("click", function() {
        	
        	
        	var opts = {
        			  lines: 13, // The number of lines to draw
        			  length: 7, // The length of each line
        			  width: 4, // The line thickness
        			  radius: 10, // The radius of the inner circle
        			  rotate: 0, // The rotation offset
        			  color: '#000', // #rgb or #rrggbb
        			  speed: 1, // Rounds per second
        			  trail: 60, // Afterglow percentage
        			  shadow: false, // Whether to render a shadow
        			  hwaccel: false, // Whether to use hardware acceleration
        			  className: 'spinner', // The CSS class to assign to the spinner
        			  zIndex: 2e9, // The z-index (defaults to 2000000000)
        			  top: 'auto', // Top position relative to parent in px
        			  left: 'auto' // Left position relative to parent in px
        			};

        			
            var container = $(this).closest(".endless_container");
            var loading = container.find(".endless_loading");
            $(this).hide();
            loading.show();
            var data = "querystring_key=" + $(this).attr("rel").split(" ")[0];
            $.get($(this).attr("href"), data, function(data) {
                container.before(data);
                container.remove();
            });
            return false;
        });
        $("a.endless_page_link").live("click", function() {
            var page_template = $(this).closest(".endless_page_template");
        	var opts = {
      			  lines: 13, // The number of lines to draw
      			  length: 7, // The length of each line
      			  width: 4, // The line thickness
      			  radius: 10, // The radius of the inner circle
      			  rotate: 0, // The rotation offset
      			  color: '#000', // #rgb or #rrggbb
      			  speed: 1, // Rounds per second
      			  trail: 60, // Afterglow percentage
      			  shadow: false, // Whether to render a shadow
      			  hwaccel: false, // Whether to use hardware acceleration
      			  className: 'spinner', // The CSS class to assign to the spinner
      			  zIndex: 2e9, // The z-index (defaults to 2000000000)
      			  top: 'auto', // Top position relative to parent in px
      			  left: 'auto' // Left position relative to parent in px
      			};
        	

       
            if (!page_template.hasClass("endless_page_skip")) {
                var data = "querystring_key=" + $(this).attr("rel").split(" ")[0];
                var hgt = page_template.height()
                var wdth = page_template.width()
                page_template.empty()
                page_template.height(hgt)
                page_template.spin(opts)
                page_template.load($(this).attr("href"), data);
                return false;
            };
        }); 
    });
})(jQuery);
