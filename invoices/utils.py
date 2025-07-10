from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Guest, Booking, Invoice, Owner
from .serializers import GuestSerializer, BookingSerializer, InvoiceSerializer
from datetime import date
from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse

class CreateInvoiceView(APIView):

    def post(self, request):
        # Extract data from request
        guest_data = request.data.get('guest')
        booking_data = request.data.get('booking')
        breakdown = request.data.get('breakdown')  # list of dicts [{quantity, description, unit_price}]

        # Save Guest
        guest_serializer = GuestSerializer(data=guest_data)
        if guest_serializer.is_valid():
            guest = guest_serializer.save()
        else:
            return Response(guest_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Save Booking linked to guest
        booking_data['guest'] = guest.id
        booking_serializer = BookingSerializer(data=booking_data)
        if booking_serializer.is_valid():
            booking = booking_serializer.save()
        else:
            guest.delete()
            return Response(booking_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Calculate amount for each item and total
        for item in breakdown:
            quantity = item.get('quantity', 1)
            unit_price = item.get('unit_price', 0)
            item['amount'] = quantity * unit_price

        # Generate invoice number (for demo, just use current year + count)
        invoice_number = Invoice.objects.filter(receipt_date__year=date.today().year).count() + 1

        # Save Invoice
        invoice = Invoice.objects.create(
            booking=booking,
            receipt_date=date.today(),
            invoice_number=invoice_number,
            breakdown=breakdown
        )

        # Generate PDF and return
        pdf_buffer = self.generate_pdf(invoice)

        response = HttpResponse(pdf_buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="invoice_{invoice.invoice_number}.pdf"'
        return response

    def generate_pdf(self, invoice):
        buffer = BytesIO()
        p = canvas.Canvas(buffer)

        # Owner data
        owner = Owner.objects.first()

        # HEADER
        p.setFont("Helvetica-Bold", 14)
        p.drawString(50, 800, owner.name if owner else "Accommodation Name")
        p.setFont("Helvetica", 10)
        if owner:
            p.drawString(50, 785, f"TAX ID: {owner.tax_id}")
            p.drawString(50, 770, f"Address: {owner.address}")
            p.drawString(50, 755, f"Phone: {owner.phone}")
            p.drawString(50, 740, f"Email: {owner.email}")

        p.drawString(400, 800, f"Invoice {invoice.receipt_date.year} - {invoice.invoice_number}")
        p.drawString(400, 785, f"Date: {invoice.receipt_date}")

        # Guest data
        p.drawString(50, 710, f"Guest: {invoice.booking.guest.full_name}")
        p.drawString(50, 695, f"ID: {invoice.booking.guest.id_number}")
        p.drawString(50, 680, f"Address: {invoice.booking.guest.address}")
        p.drawString(50, 665, f"Contact: {invoice.booking.guest.contact}")

        # Booking details
        p.drawString(50, 640, f"Check-in: {invoice.booking.check_in}")
        p.drawString(200, 640, f"Check-out: {invoice.booking.check_out}")
        p.drawString(350, 640, f"Guests: {invoice.booking.number_of_guests}")
        p.drawString(450, 640, f"Unit: {invoice.booking.unit}")

        # Table headers
        y = 610
        p.drawString(50, y, "Quantity")
        p.drawString(120, y, "Description")
        p.drawString(320, y, "Unit Price")
        p.drawString(420, y, "Amount")

        # Table rows
        y -= 20
        for item in invoice.breakdown:
            p.drawString(50, y, str(item.get('quantity', '')))
            p.drawString(120, y, item.get('description', ''))
            p.drawString(320, y, f"{item.get('unit_price', 0):.2f}")
            p.drawString(420, y, f"{item.get('amount', 0):.2f}")
            y -= 20

        # Totals
        y -= 10
        p.drawString(350, y, "Subtotal:")
        p.drawString(420, y, f"{invoice.subtotal:.2f}")
        y -= 20
        p.drawString(350, y, f"VAT ({owner.vat_percentage if owner else 21}%):")
        p.drawString(420, y, f"{invoice.vat:.2f}")
        y -= 20
        p.drawString(350, y, "Total:")
        p.drawString(420, y, f"{invoice.total:.2f}")

        p.showPage()
        p.save()

        buffer.seek(0)
        return buffer
