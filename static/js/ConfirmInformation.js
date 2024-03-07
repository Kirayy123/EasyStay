function confirmInformation() {
    return confirm('Are you sure you want to delete this record?');
}

function confirmBooking() {
            // 使用 window.confirm 显示对话框
            var userConfirmed = window.confirm("Are you sure you want to confirm this booking?");
            if (userConfirmed) {
                alert("Booking confirmed!");
                window.location.href = '/easystay/userProfile/';
            }
        }

function confirmCancelBooking(bookingId) {
    var userConfirmed = window.confirm("Are you sure you want to cancel this booking?");
    if (userConfirmed) {
        fetch(`/easystay/booking/cancel/${bookingId}/`)
            .then(response => {
                if (response.ok) {
                    // redirect to user_booking
                    window.location.href = response.url;
                } else {
                    alert('Something went wrong while trying to cancel the booking.');
                }
            })
            .catch(error => console.error('Error:', error));
    }
}

function changePassword(event) {
    // Prevent the default form submission
    event.preventDefault();

    // Use window.confirm to ask for user confirmation
    var userConfirmed = window.confirm("Are you sure you want to change your password?");
    if (userConfirmed) {
        // If confirmed, show an alert
        alert("Password change successfully!");

        // Then submit the form manually
        event.target.form.submit();
    }
}