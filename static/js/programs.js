"use strict";

$('#programSearchForm').on('submit', (evt) => {
    evt.preventDefault();

    let search_text = $('#search_text').val();
    let search_type = $('#search_type').val();

    let data = {'search_text': search_text, 'search_type': search_type}
    $.get('/programs.json', data, (results) => {
        // results is a JSON object with all the programs that match the search

        $('#programResults').empty(); 
        
        if (results.length == 0) {
            $('#programResults').html("No results found. Try again with a different search."); 
        } 
        else {       
            // add table headers
            $('#programResults').append("<table>");
            let table_heading = "<tr><th>Favorite</th><th>Program</th><th>Address</th><th>City</th><th>State</th><th>Zipcode</th></tr>";
            $('#programResults').append(table_heading);

            // add each row for the table
            for (let i in results) {
                let program_id = results[i].program_id;
                let row = '<tr>';
                if (results[i].favorite == 1) {
                    // this is a favorite
                    row += `<td><i class='program-star fas fa-star' data-programid='${program_id}'></i></td>`;
                } else {
                    row += `<td><i class='program-star far fa-star' data-programid='${program_id}'></i></td>`;
                }
                let program_name = results[i].program_name;
                row += `<td>${program_name}</td>`;
                let address = results[i].address;
                row += `<td>${address}</td>`;
                let city = results[i].city;
                row += `<td>${city}</td>`;
                let state = results[i].state;
                row += `<td>${state}</td>`;
                let zipcode = results[i].zipcode;
                row += `<td>${zipcode}</td>`;
                row += '</tr>';
                $('#programResults').append(row);
            }
            $('#programResults').append("</table>");
        }
        
    });  

});

$(document).on('click', '.program-star', (evt) => {
    let programStar = $(evt.target);
    let program_id = programStar.data('programid');
    $.get('/toggle_favorite_program', {'program_id': program_id}, (results) => {
        console.log(results);
        if (results.user_logged_in == true) {
            // A user is logged in 
            if (results.favorite == true) {
                // user favorited the program, toggle star to solid
                programStar.removeClass('far').addClass('fas');
            } else {
                // user unfavorited the program, toggle star to regular
                programStar.removeClass('fas').addClass('far');
            }
        } else {
            // A user is not logged in, show error message
            $('#programsErrorMessage').fadeIn(400, () => {
                setTimeout(() => {$('#programsErrorMessage').fadeOut(400,)}, 5000);
            });
        }
    });
});