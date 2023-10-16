Django Models Documentation
==========================

Listing Model
-------------

Introduction
^^^^^^^^^^^^
The `Listing` model represents a property or accommodation listing and stores information about the owner, property name, address, total rooms, price per room, description, and amenities.

Fields
^^^^^^
- `owner` (ForeignKey to User): The owner of the listing.
- `name` (CharField): The name of the property.
- `address` (CharField): The address of the property.
- `total_rooms` (PositiveIntegerField): The total number of rooms available.
- `price_per_room` (DecimalField): The price per room.
- `description` (TextField, optional): Description of the property.
- `amenities` (TextField, optional): Amenities provided by the property.

Reservation Model
----------------

Introduction
^^^^^^^^^^^^
The `Reservation` model represents a reservation for a listing, containing information about the listing, customer, start date, end date, total price, number of rooms, special requests, and status.

Fields
^^^^^^
- `listing` (ForeignKey to Listing): The listing for which the reservation is made.
- `customer` (ForeignKey to User): The customer making the reservation.
- `start_date` (DateField): The start date of the reservation.
- `end_date` (DateField): The end date of the reservation.
- `total_price` (DecimalField): The total price of the reservation.
- `num_rooms` (PositiveIntegerField, default: 1): The number of rooms booked.
- `special_requests` (TextField, optional): Special requests or notes.
- `status` (CharField): The status of the reservation.

ReservedDate Model
------------------

Introduction
^^^^^^^^^^^^
The `ReservedDate` model stores information about dates reserved for a listing, helping manage room availability for specific dates.

Fields
^^^^^^
- `listing` (ForeignKey to Listing): The listing associated with the reserved date.
- `date` (DateField): The reserved date.
- `num_rooms_reserved` (PositiveIntegerField, default: 0): The number of rooms reserved for the date.
