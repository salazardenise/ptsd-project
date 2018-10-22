"use strict";

$('#programSearchForm').on('submit', (evt) => {
    evt.preventDefault();

    let search_text = $('#search_text').val();
    let search_type = $('#search_type').val();

    let data = {'search_text': search_text, 'search_type': search_type}
    $.get('/programs.json', data, (results) => {
        // results is a JSON object with all the programs that match the search
        
        if (results.length == 0) {
            $('#programsResults').empty()
            $('#programsResults').html("No results found. Try again with a different search."); 
            $('#programsMap').hide()
        } 
        else { 
            /////////////////////////////////////////////////////////
            // PROCESS PROGRAMS RESULTS TO GET SET OF facilities with addresses attached
            


            // /////////////////////////////////////////////////////////
            // // DISPLAY PROGRAMS RESULTS LOCATIONS IN MAP
            // $('#programsMap').show()

            // // create map
            // let defaultLocationUS= {lat: 39, lng: -95};
            // let map = new google.maps.Map(document.querySelector('#programsMap'), {
            //     center: defaultLocationUS,
            //     zoom: 6});

            // // determine where to center map
            // function setCenterOfMap(search_text) {
            //     let location = new google.maps.Geocoder();

            //     location.geocode({'address': search_text}, 
            //         function (results, status) {
            //             console.log(status);
            //             if (status === google.maps.GeocoderStatus.OK) {
            //                 console.log(status);
            //                 map.setCenter(results[0].geometry.location);
            //             } else {
            //                 console.log('Geocode was not successful for the following reason: ' + status);
            //             }
            //         }
            //     )
            // }
            // setCenterOfMap(search_text);

            // // add each program to map with marker and info window
            // function addProgramLocationByAddress(programName, programFullAddress) {
            //     let programLocation = new google.maps.Geocoder();
            //     let address = programFullAddress;
            //     programLocation.geocode(
            //         {'address': address, 'region': 'US'},
            //         function(results, status) {
            //             console.log(status);
            //             if (status == google.maps.GeocoderStatus.OK) {
            //                 let programLatLng = results[0].geometry.location;
            //                 let programMarker = new google.maps.Marker({
            //                     position: programLatLng,
            //                     map: map,
            //                     title: programName,
            //                 }); 
            //             } else {
            //                 console.log('Geocode not successful for ' + address)
            //             }
            //         }
            //     )
            // }

            // for (let i in results) {
            //     let programFullAddress = results[i].address + ', ' + 
            //                          results[i].city + ', ' + 
            //                          results[i].state;
            //     addProgramLocationByAddress(results[i].program_name, programFullAddress);
            // }

            ///////////////////////////////////////////////////////////
            // DISPLAY PROGRAMS RESULTS IN TABLE      
            // add table headers
            $('#programsResults').empty()
            $('#programsResults').append("<table>");
            let table_heading = "<tr><th>Favorite</th><th>Facility</th><th>Program</th><th>Address</th><th>City</th><th>State</th><th>Zipcode</th></tr>";
            $('#programsResults').append(table_heading);

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
                let fac_name = results[i].fac_name;
                row += `<td>${fac_name}</td>`
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
                $('#programsResults').append(row);
            }
            $('#programsResults').append("</table>");
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