(function (factory) {
  factory(jQuery, moment, _);
}(function ($, moment, _) {
   var pluginName = 'calendar';

  function Calendar(element) {
    this.element = element;

    this._name = pluginName;

    this.init();
  }

  Calendar.prototype.init = function() {
    var daysInMonth = [];

    var day = moment();
    _.times(day.daysInMonth(), function (n) {
      daysInMonth.push(day.format('D'));  // your format
      day.add(1, 'day');
    });

    console.log(daysInMonth);
  }

  $.fn.calendar = function() {
    var calendarInstance;

    if (this.length > 1) {
      throw new Error(
        "CLNDR does not support multiple elements yet. Make sure " +
        "your clndr selector returns only one element."
      );
    }

    if (!this.length) {
      throw new Error(
        "CLNDR cannot be instantiated on an empty selector."
      );
    }

    if (!this.data('plugin_calendar')) {
      calendarInstance = new Calendar(this);
      this.data('plugin_calendar', calendarInstance);
      return calendarInstance;
    }

    return this.data('plugin_calendar');
  };
}));
