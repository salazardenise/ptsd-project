"use strict";

function toggleFavorite(program_id) {
    $.get('/toggle_favorite', {'program_id': program_id}, (result) => {
        if (result == 'favorite') {
            $(`#program-id-${program_id}`).removeClass('far fa-star').addClass('fas fa-star');
        } else if (result == 'unfavorite') {
            $(`#program-id-${program_id}`).removeClass('fas fa-star').addClass('far fa-star');
        }   

    });
}

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
            // add table headers
            $('#programResults').append("<table>");
            let table_heading = "<tr><th>Favorite</th><th>Program</th><th>Address</th><th>City</th><th>State</th><th>Zipcode</th></tr>"
            $('#programResults').append(table_heading);

            // add each row for the table
            for (let i in results) {
                let program_id = results[i].program_id;
                let row = `<tr onclick='toggleFavorite(${program_id});'>`
                if (results[i].favorite == 1) {
                    // this is a favorite
                    row += `<td><i id='program-id-${program_id}' class='fas fa-star'></i></td>`
                } else {
                    row += `<td><i id='program-id-${program_id}' class='far fa-star'></i></td>`
                }

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