// Function to show booking details
    function showDetails(bookingId) {
        // Make an AJAX call to retrieve booking details
        fetch(`/easystay/booking_details/${bookingId}/`)
            .then(response => response.json())
            .then(data => {
                let details = JSON.parse(data);

                document.getElementById('details').innerHTML = `
                    <p><strong>Reference Number: </strong>${details.ref_num}</p>
                    <p><strong>Room Type: </strong>${details.room_type}</p>
                    <p><strong>Room Number:</strong> ${details.room_number}</p>
                    <p><strong>Reserved Name:</strong> ${details.reserved_name}</p>
                    <p><strong>Reserved Phone:</strong> ${details.reserved_phone}</p>
                    <p><strong>Booking Time:</strong> ${details.booking_date}</p>
                    <p><strong>Booked Check-in Date:</strong> ${details.bcheck_in_date}</p>
                    <p><strong>Booked Check-out Date:</strong> ${details.bcheck_out_date}</p>
                    <p><strong>Total Days:</strong> ${details.total_days}</p>
                    <p><strong>Total Price:</strong> £${details.total_price}</p>
                    <p><strong>Check-in Time:</strong> ${details.check_in_date}</p>
                    <p><strong>Check-out Time:</strong> ${details.check_out_date}</p>

                `;
                document.getElementById('details-backdrop').style.display = 'flex';
            })
            .catch(error => {
                console.error('Error fetching details:', error);
            });
    }

    // Function to hide booking details
    function hideDetails() {
        document.getElementById('details-backdrop').style.display = 'none';
    }