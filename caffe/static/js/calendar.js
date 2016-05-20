(function (factory) {
  factory(jQuery, moment, _);
}(function ($, moment, _) {
  moment.locale('pl');

  function Calendar(element) {
    this.element = element;
    this.template =
      "<div class='calendar__control'>" +
        "<div class='calendar__previous__button'><i class='fa fa-chevron-left' aria-hidden='true'></i></div>" +
        "<div class='calendar__month'><%= month %> <%= year %></div>" +
        "<div class='calendar__next__button'><i class='fa fa-chevron-right' aria-hidden='true'></i></div>" +
      "</div>" +
      "<table class='table--red table--hover--cell' border='0' cellspacing='0' cellpadding='0'>" +
        "<thead>" +
         "<tr>" +
           "<% for(var i = 0; i < daysOfTheWeek.length; i++) { %>" +
             "<th class='center'><%= daysOfTheWeek[i] %></th>" +
           "<% } %>" +
         "</tr>" +
        "</thead>" +
        "<tbody>" +
          "<% for(var i = 0; i < numberOfRows; i++){ %>" +
           "<tr>" +
           "<% for(var j = 0; j < 7; j++) { %>" +
           "<% var d = j + i * 7; %>" +
              "<td class='table__cell--center <%= days[d].class %>'>" +
                "<a href='/calendar/<%= days[d].date %>'><%= days[d].day %></a>" +
              "</td>" +
           "<% } %>" +
           "</tr>" +
          "<% } %>" +
        "</tbody>" +
      "</table>";

    this.date = moment().clone();
    this.compiledTempalte = _.template(this.template);

    this.init();
  }

  Calendar.prototype.init = function() {
    this.element
      .on('click', '.calendar__previous__button', {context: this}, this.backAction)
      .on('click', '.calendar__next__button', {context: this}, this.forwardAction)

    this.render();
  }

  Calendar.prototype.backAction = function(event) {
    event.data.context.date = event.data.context.date.subtract(1, 'month');
    event.data.context.render();
  }

  Calendar.prototype.forwardAction = function(event) {
    event.data.context.date = event.data.context.date.add(1, 'month');
    event.data.context.render();
  }

  Calendar.prototype.render = function() {
    var days = [];
    var weekdays = [];
    var month = this.date.startOf('month').startOf('day');

    for (var i = 0; i < 7; ++i) {
      var weekday = moment().startOf('week').weekday(i).format('dddd');
      weekdays.push(_.upperFirst(weekday));
    }

    // add days from previous month to fill first weekday
    var tmpDate = month.clone();
    for (var i = 0; i < parseInt(month.format('e')); ++i) {
      tmpDate.subtract(1, 'day');
      days.push({
        'day': tmpDate.format('D'),
        'date': tmpDate.format('DD-MM-YYYY'),
        'class': 'table__cell--disabled'
      });
    }
    days = _.reverse(days);

    // add days from current month
    tmpDate = month.clone();
    _.times(month.daysInMonth(), function() {
      days.push({
        'day': tmpDate.format('D'),
        'date': tmpDate.format('DD-MM-YYYY'),
        'class': (tmpDate.diff(moment().startOf('day'), 'days') == 0 ? 'table__cell--highlight' : '')
      });

      tmpDate.add(1, 'day');
    });

    // add days from next month to fill last weekday
    while (days.length % 7 != 0) {
      days.push({
        'day': tmpDate.format('D'),
        'date': tmpDate.format('DD-MM-YYYY'),
        'class': 'table__cell--disabled'
      });

      tmpDate.add(1, 'day');
    }

    var data = {
      'month': _.upperFirst(this.date.format('MMMM')),
      'year': this.date.format('YYYY'),
      'daysOfTheWeek': weekdays,
      'numberOfRows': days.length / 7,
      'days': days
    }

    this.element.html(this.compiledTempalte(data));
  }

  $.fn.calendar = function() {
    var calendarInstance;

    if (this.length > 1) {
      throw new Error(
        "Calendar does not support multiple elements yet. Make sure " +
        "your clndr selector returns only one element."
      );
    }

    if (!this.length) {
      throw new Error(
        "Calendar cannot be instantiated on an empty selector."
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
