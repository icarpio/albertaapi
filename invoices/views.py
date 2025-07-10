from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Guest, Booking, Invoice, Owner
from .serializers import GuestSerializer, BookingSerializer, InvoiceSerializer
from datetime import date
from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from rest_framework.permissions import AllowAny
from datetime import datetime
import os

    
class CreateInvoiceView(APIView):
    
    authentication_classes = []  # disable authentication
    permission_classes = [AllowAny]  # allow all users

    def post(self, request):
        guest_data = request.data.get('guest')
        booking_data = request.data.get('booking')
        breakdown = request.data.get('breakdown')  # list of dicts [{quantity, description, unit_price}]

        # Guardar Guest
        guest_serializer = GuestSerializer(data=guest_data)
        if guest_serializer.is_valid():
            guest = guest_serializer.save()
        else:
            return Response(guest_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Guardar Booking ligado al guest
        booking_data['guest'] = guest.id
        booking_serializer = BookingSerializer(data=booking_data)
        if booking_serializer.is_valid():
            booking = booking_serializer.save()
        else:
            guest.delete()
            return Response(booking_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Calcular días entre check_in y check_out
        check_in_str = booking_data.get('check_in')
        check_out_str = booking_data.get('check_out')

        try:
            check_in_date = datetime.strptime(check_in_str, '%Y-%m-%d').date()
            check_out_date = datetime.strptime(check_out_str, '%Y-%m-%d').date()
            delta_days = (check_out_date - check_in_date).days
            if delta_days < 1:
                return Response({"error": "Check-out must be after Check-in"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "Invalid check-in or check-out date format"}, status=status.HTTP_400_BAD_REQUEST)

        # Actualizar quantity para todos los items al número de días
        for item in breakdown:
            item['quantity'] = delta_days
            unit_price = item.get('unit_price', 0)
            item['amount'] = delta_days * unit_price

        # Generar número de factura reiniciando cada año
        current_year = date.today().year
        count = Invoice.objects.filter(receipt_date__year=current_year).count() + 1
        invoice_number = count

        # Crear factura
        invoice = Invoice.objects.create(
            booking=booking,
            receipt_date=date.today(),
            invoice_number=invoice_number,
            breakdown=breakdown
        )

        pdf_buffer = self.generate_pdf(invoice)

        response = HttpResponse(pdf_buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="C{invoice.invoice_number:03d}_{invoice.receipt_date.strftime("%y")}.pdf"'
        print(response['Content-Disposition'])
        return response

    
    def generate_pdf(self, invoice):
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.units import inch
        from reportlab.lib import colors

        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        owner = Owner.objects.first()


        # --- HEADER IMAGE ---
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        # Ruta completa al logo.png
        logo_path = os.path.join(BASE_DIR, "logo.png")
        logo_width = 120  # ajusta según necesidad
        logo_height = 40  # ajusta según necesidad

        # Coordenadas para centrar imagen
        x = (width - logo_width) / 2
        y = height - 100  # más abajo si el logo es más alto

        try:
            p.drawImage(logo_path, x, y, width=logo_width, height=logo_height, mask='auto')
        except Exception as e:
            # Fallback: muestra texto si no se encuentra la imagen
            p.setFont("Helvetica-Bold", 16)
            header_text = owner.name if owner else "Accommodation Name"
            p.drawCentredString(width / 2, height - 50, header_text)
   
        p.setFont("Helvetica", 12)  
        y = height - 150
        if owner:
            owner_y = y - 30  # baja más
            p.drawString(50, owner_y, f"CIF: {owner.tax_id}")
            p.drawString(50, owner_y - 15, f"{owner.fist_name}")   
            p.drawString(50, owner_y - 30, f"{owner.address}")
            p.drawString(50, owner_y - 45, f"{owner.phone}")

        p.drawRightString(
            width - 50,
            y,
            f"Factura:   C{invoice.invoice_number:03d}/{invoice.receipt_date.strftime('%y')}"
        )
        p.drawRightString(width - 50, y - 15, f"Fecha:{invoice.receipt_date.strftime('%d-%m-%Y')}")

        # --- Detalles de la reserva ---  
        y = height - 300  # Bajamos un poco para evitar superposición
        p.setFont("Helvetica-Bold", 14)
        p.drawString(50, y, "Detalles de la reserva")

        y -= 20
        p.setFont("Helvetica", 11)
        p.drawString(50, y, f"{invoice.booking.guest.full_name}")
        p.drawString(50, y - 15, f"NIF/CIF: {invoice.booking.guest.id_number}")
        p.drawString(50, y - 30, f"{invoice.booking.guest.address}")


        y -= 70
        p.setFont("Helvetica", 11)

        centered_text = (
            f"Check-in: {invoice.booking.check_in.strftime('%d-%m-%Y')}   "
            f"Check-out: {invoice.booking.check_out.strftime('%d-%m-%Y')}   "
            f"Unidad: {invoice.booking.unit}"
        )

        p.drawCentredString(width / 2, y, centered_text)

        # --- Tabla de factura ---
        x_offset = 30  # Ajusta este valor para mover toda la tabla más a la derecha
        y -= 100
        row_height = 20

        # Encabezado con fondo gris claro
        p.setFillColor(colors.lightgrey)
        p.rect(50 + x_offset, y - row_height, 460, row_height, fill=1, stroke=0)

        p.setFillColor(colors.black)
        p.setFont("Helvetica-Bold", 12)
        p.drawString(55 + x_offset, y - 15, "Cantidad")
        p.drawString(120 + x_offset, y - 15, "Descripción")
        p.drawString(370 + x_offset, y - 15, "Precio Unitario")
        p.drawString(480 + x_offset, y - 15, "Total")

        # Línea bajo encabezado
        p.setStrokeColor(colors.black)
        p.line(50 + x_offset, y - row_height, 510 + x_offset, y - row_height)

        # Dibujar filas
        y -= row_height
        p.setFont("Helvetica", 11)

        for item in invoice.breakdown:
            p.rect(50 + x_offset, y - row_height, 460, row_height, fill=0, stroke=1)

            p.drawRightString(110 + x_offset, y - 15, str(item.get('quantity', '')))
            p.drawString(120 + x_offset, y - 15, item.get('description', ''))
            p.drawRightString(440 + x_offset, y - 15, f"{item.get('unit_price', 0):.2f}")
            p.drawRightString(510 + x_offset, y - 15, f"{item.get('amount', 0):.2f}")
            y -= row_height

        # Totales
        y -= 30
        p.setFont("Helvetica-Bold", 12)

        p.drawString(300 + x_offset, y, "Base Imponible:")
        p.drawRightString(510 + x_offset, y, f"{invoice.subtotal:.2f} €")
        y -= 20

        p.drawString(300 + x_offset, y, f"IVA ({owner.vat_percentage if owner else 21}%):")
        p.drawRightString(510 + x_offset, y, f"{invoice.vat:.2f} €")
        y -= 20

        p.line(300 + x_offset, y, 510 + x_offset, y)
        y -= 15

        p.drawString(300 + x_offset, y, "Total:")
        p.drawRightString(510 + x_offset, y, f"{invoice.total:.2f} €")

        # Finalizar y guardar PDF
        p.showPage()
        p.save()

        buffer.seek(0)
        return buffer

    