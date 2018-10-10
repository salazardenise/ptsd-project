"use strict";

$('#programSearchForm').on('submit', (evt) => {
    evt.preventDefault();

    let search_text = $('#search_text').val();
    let search_type = $('#search_type').val();

    let data = {'search_text': search_text, 'search_type': search_type}
    $.get('/search_programs', data, (results) => {
        // results is a JSON object with all the programs that match the search

        $('#programResults').empty(); 
        
        if (results.length == 0) {
            $('#programResults').html("No results found. Try again with a different search."); 
        } 
        else {       
            $('#programResults').append("<table>");
            let table_heading = "<tr><th>Favorite</th><th>Program</th><th>Address</th><th>City</th><th>State</th><th>Zipcode</th></tr>"
            $('#programResults').append(table_heading);

            for (let i in results) {
                let row = "<tr><td><i class='far fa-star'></i></td>"
                let program_name = results[i].program_name;
                row += `<td>${program_name}</td>`
                let address = results[i].address;
                row += `<td>${address}</td>`
                let city = results[i].city;
                row += `<td>${city}</td>`
                let state = results[i].state;
                row += `<td>${state}</td>`
                let zipcode = results[i].zipcode;
                row += `<td>${zipcode}</td></tr>`
                $('#programResults').append(row);
            }
            $('#programResults').append("</table>");
        }
        
    });

});