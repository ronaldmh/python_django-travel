
document.addEventListener('DOMContentLoaded', function() {
    // get data
    var startDate = new Date('{{ start_date }}');
    var endDate = new Date('{{ end_date }}');

    // months array 
    var monthNames = ["ENE", "FEB", "MAR", "ABR", "MAY", "JUN", "JUL", "AGO", "SEP", "OCT", "NOV", "DIC"];

    // start date Format
    var startDay = startDate.getDate();
    var startMonth = monthNames[startDate.getMonth()];
    var startYear = startDate.getFullYear();
    var formattedStartDate = startDay + " " + startMonth;

    // end date Format
    var endDay = endDate.getDate();
    var endMonth = monthNames[endDate.getMonth()];
    var endYear = endDate.getFullYear();
    var formattedEndDate = endDay + " " + endMonth;

    // display
    document.getElementById('formatted-dates').textContent = formattedStartDate;
    document.getElementById('formatted-dates-end').textContent = formattedEndDate;
});