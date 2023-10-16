Django APIs Documentation
=========================

CheckAvailability API
---------------------

Introduction
^^^^^^^^^^^^
The `CheckAvailability` API provides an endpoint to check room availability for a specific listing within a specified date range, allowing users to verify room availability by providing details such as the number of rooms, listing ID, and start and end dates.

Endpoints
^^^^^^^^^

- **Check Room Availability (GET)**: Checks room availability for a listing within a specified date range.

Parameters
^^^^^^^^^^
- `num_rooms` (integer): The number of rooms required.
- `listing_id` (integer): The unique ID of the listing.
- `start_date` (date): The start date for room reservation.
- `end_date` (date): The end date for room reservation.

Response
^^^^^^^^
- **200 OK**: Rooms are available, returning a success status with room availability message.
- **404 Not Found**: Listing not found, returning an error status with a message.
- **409 Conflict**: Rooms are unavailable, returning an error status with an explanation for unavailability.

Reservations API
----------------

Introduction
^^^^^^^^^^^^
The `Reservations` API enables users to make reservations for a listing. It provides endpoints for creating reservations and checking room availability before making a reservation.

Endpoints
^^^^^^^^^

- **Create Reservation (POST)**: Creates a new reservation for a listing.

Parameters
^^^^^^^^^^
- `num_rooms` (integer): The number of rooms required.
- `listing_id` (integer): The unique ID of the listing.
- `start_date` (date): The start date for room reservation.
- `end_date` (date): The end date for room reservation.
- `name` (string): The name of the customer making the reservation.
- `special_requests` (string, optional): Special requests or notes from the customer.

Response
^^^^^^^^
- **201 Created**: Reservation successfully created, returning a success status with reservation details.
- **404 Not Found**: Listing not found, returning an error status with a message.
- **409 Conflict**: Rooms are unavailable, returning an error status with an explanation for unavailability.
- **400 Bad Request**: Missing required entries, returning an error status with a message.

This documentation provides a foundation for your Django models and APIs. You can expand on this base, include usage examples, request and response schemas, and authentication requirements to create more comprehensive documentation for your project.