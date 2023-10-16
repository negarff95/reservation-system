from django.shortcuts import render
from django.views import View

from listing.models import Listing


class ReservationsReportView(View):
    template_name = "reservation_report.html"

    def get(self, request):
        _listing = request.GET.get("listing")

        exceptions = []
        listing = None
        listing_id = None
        listing_name = None
        reservations = None
        if _listing:
            try:
                listing_id = int(_listing)
            except Exception:
                listing_name = _listing
            try:
                if listing_id:
                    listing = Listing.objects.get(id=listing_id)
                else:
                    listing = Listing.objects.get(name=listing_name)
            except Exception:
                pass

            if listing:
                try:
                    reservations = listing.reservations.all()
                except Exception as e:
                    exceptions.append(str(e))
        return render(
            request,
            self.template_name,
            {
                "exceptions": exceptions,
                "listing": listing,
                "reservations": reservations,
            },
        )
