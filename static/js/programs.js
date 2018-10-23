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
            // DISPLAY PROGRAMS RESULTS LOCATIONS IN MAP
            $('#programsMap').show()

            // create map
            let map;

            // determine where to center map
            function setCenterOfMap(search_text) {
                let location = new google.maps.Geocoder();

                location.geocode({'address': search_text}, 
                    function (results, status) {
                        if (status === google.maps.GeocoderStatus.OK) {
                            map = new google.maps.Map(document.querySelector('#programsMap'), {
                                center: results[0].geometry.location,
                                zoom: 6
                            });
                        } else {
                            let defaultLocationUS= {lat: 39, lng: -95};
                            map = new google.maps.Map(document.querySelector('#programsMap'), {
                                center: defaultLocationUS,
                                zoom: 2
                            });
                        }
                    }
                )
            }
            setCenterOfMap(search_text);

            let infoWindow = new google.maps.InfoWindow({
                width: 150
            });

            // add each facility to map with marker and info window
            function addFacilityLocationByAddress(facilityName, facilityFullAddress) {
                let facilityLocation = new google.maps.Geocoder();
                let address = facilityFullAddress;
                facilityLocation.geocode(
                    {'address': address, 'region': 'US'},
                    function(results, status) {
                        if (status == google.maps.GeocoderStatus.OK) {
                            let facilityLatLng = results[0].geometry.location;
                            let facilityMarker = new google.maps.Marker({
                                position: facilityLatLng,
                                map: map,
                                title: facilityName,
                            }); 
                            // Define the content of the infoWindow
                            let html = (
                                '<div>' +
                                '<p>' + facilityName + '</p>' +
                                '<p>' + facilityFullAddress + '</p>' +
                                '</div>'
                            );
                            // bind an infowindow to the marker
                            google.maps.event.addListener(facilityMarker, 'click', function () {
                                infoWindow.close();
                                infoWindow.setContent(html);
                                infoWindow.open(map, facilityMarker);
                            });
                        } else {
                            console.log('Geocode not successful for ' + address)
                        }
                    }
                )
            }

            for (let i in results) {
                let facilityFullAddress = results[i].address + ', ' + 
                                     results[i].city + ', ' + 
                                     results[i].state;
                addFacilityLocationByAddress(results[i].fac_name, facilityFullAddress);
            }

            ///////////////////////////////////////////////////////////
            // DISPLAY PROGRAMS RESULTS IN TABLE      
            // add table headers
            $('#programsResults').empty()
            $('#programsResults').append("<table>");
            let table_heading = "<tr><th>Favorite</th><th>Facility</th><th>Address</th><th>City</th><th>State</th><th>Zipcode</th></tr>";
            $('#programsResults').append(table_heading);

            // add each row for the table
            for (let i in results) {
                let fac_id = results[i].fac_id;
                let row = '<tr>';
                if (results[i].favorite == 1) {
                    // this is a favorite
                    row += `<td><i class='facility-star fas fa-star' data-facid='${fac_id}'></i></td>`;
                } else {
                    row += `<td><i class='facility-star far fa-star' data-facid='${fac_id}'></i></td>`;
                }
                // add facility name
                let fac_name = results[i].fac_name;
                row += `<td class='facility-name' data-facid='${fac_id}'>${fac_name}</td>`
                // add address
                let address = results[i].address;
                row += `<td>${address}</td>`;
                // add city
                let city = results[i].city;
                row += `<td>${city}</td>`;
                // add state
                let state = results[i].state;
                row += `<td>${state}</td>`;
                // add zipcode
                let zipcode = results[i].zipcode;
                row += `<td>${zipcode}</td>`;
                row += '</tr>';
                $('#programsResults').append(row);
            }
            $('#programsResults').append("</table>");
        }
        
    });  

});

$(document).on('click', '.facility-star', (evt) => {
    let facilityStar = $(evt.target);
    let fac_id = facilityStar.data('facid');
    $.get('/toggle_favorite_facility', {'fac_id': fac_id}, (results) => {
        if (results.user_logged_in == true) {
            // A user is logged in 
            if (results.favorite == true) {
                // user favorited the program, toggle star to solid
                facilityStar.removeClass('far').addClass('fas');
            } else {
                // user unfavorited the program, toggle star to regular
                facilityStar.removeClass('fas').addClass('far');
            }
        } else {
            // A user is not logged in, show error message
            $('#programsErrorMessage').fadeIn(400, () => {
                setTimeout(() => {$('#programsErrorMessage').fadeOut(400,)}, 5000);
            });
        }
    });
});

$(document).on('click', '.facility-name', (evt) => {
    let facilityName = $(evt.target);
    let fac_id = facilityName.data('facid');
    if (facilityName.find('ul').length == 0) {
        $.get('/programs_by_facility.json', {'fac_id': fac_id}, (results) => {
            let lst = "<ul class='programsList'>";
            for (let i in results) {
                lst += `<li>${results[i].program_name}</li>`
            }
            lst += '</ul>'
            facilityName.append(lst);
            // do not allow clicking on facilityName's children
            facilityName.children().click( (e) => {e.stopPropagation()});
        });
    } else {
        let programs_lst = facilityName.find('ul');
        programs_lst.remove();
    }
});