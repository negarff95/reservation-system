Django Views Documentation
=========================

ReservationsReportView
---------------------

Introduction
^^^^^^^^^^^^
The `ReservationsReportView` is a Django class-based view that provides an endpoint for generating a reservations report for a specific listing. It renders an HTML template to display information about the listing and its reservations.

Attributes
^^^^^^^^^^
- `template_name` (str): The name of the HTML template used to render the reservations report.

Methods
^^^^^^^

`get(self, request)`
--------------------

**Description:**
This method handles GET requests and generates a reservations report for a specific listing.

**Parameters:**
- `request` (HttpRequest): The HTTP request object.

**Returns:**
- `HttpResponse`: The rendered HTML template containing the reservations report.

**Behavior:**
1. Parse the `listing` parameter from the request's GET parameters.
2. Initialize an empty list `exceptions` to capture any exceptions.
3. Initialize variables for `listing`, `listing_id`, `listing_name`, and `reservations` to `None`.
4. Check if a `listing` parameter is provided.
   - If provided, attempt to parse it as an integer (`listing_id`).
   - If parsing as an integer fails, assume `listing` is a string (`listing_name`).
5. Try to fetch the listing using the `listing_id` or `listing_name`. Handle exceptions if the listing is not found.
6. If a valid listing is obtained:
   - Try to fetch the reservations associated with the listing.
   - Capture any exceptions and append them to the `exceptions` list.
7. Render the HTML template, passing in the following context:
   - `exceptions`: A list of exceptions captured during the process.
   - `listing`: The listing object (if found).
   - `reservations`: The reservations associated with the listing (if found).

**Usage:**
- Access the view by making a GET request to the corresponding URL endpoint.
- Provide the `listing` parameter to specify the listing for which you want to generate the reservations report.

**Template:**
The view uses the HTML template specified by the `template_name` attribute to render the reservations report. The template should include placeholders for displaying exceptions, listing information, and reservations.

**Example URL Endpoint:**
- `listing/reservations-report/?listing=123`

**Response:**
The view renders an HTML page displaying the reservations report for the specified listing. It may include exceptions, listing details, and reservations, if available.
