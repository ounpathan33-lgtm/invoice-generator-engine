from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors

def create_invoice(file_name, client_name, invoice_num, due_date, items, payment_info, tax_rate=0.08, discount_amount=0.00):
    pdf = canvas.Canvas(file_name, pagesize=letter)
    pdf.setTitle(f"Invoice - {client_name}")

    # 1. Header Banner Layout
    pdf.setFillColor(colors.HexColor("#1a365d"))
    pdf.rect(0, 720, 612, 80, fill=True, stroke=False)
    
    pdf.setFillColor(colors.white)
    pdf.setFont("Helvetica-Bold", 24)
    pdf.drawString(50, 750, "INVOICE")
    
    # Optional Text-Based Branding Logo Placeholder
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawRightString(562, 750, "MY BUSINESS LLC")

    # 2. Metadata Blocks
    pdf.setFillColor(colors.HexColor("#2d3748"))
    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, 685, "Billed To:")
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(50, 670, client_name)
    
    pdf.setFont("Helvetica", 10)
    pdf.setFillColor(colors.HexColor("#718096"))
    pdf.drawRightString(562, 685, f"Invoice #: {invoice_num}")
    pdf.drawRightString(562, 670, f"Due Date: {due_date}")

    # 3. Table Header Grid
    pdf.setFillColor(colors.HexColor("#edf2f7"))
    pdf.rect(50, 605, 512, 22, fill=True, stroke=False)
    
    pdf.setFillColor(colors.HexColor("#4a5568"))
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(55, 612, "Item Description")
    pdf.drawString(350, 612, "Quantity")
    pdf.drawString(450, 612, "Unit Price")
    pdf.drawString(520, 612, "Total")

    # 4. Dynamic Multi-Item Matrix Loop
    current_y = 585
    subtotal = 0.0
    row_count = 0

    for item in items:
        item_total = item["quantity"] * item["price"]
        subtotal += item_total

        if row_count % 2 == 0:
            pdf.setFillColor(colors.HexColor("#f7fafc"))
            pdf.rect(50, current_y - 4, 512, 18, fill=True, stroke=False)
        
        pdf.setFillColor(colors.HexColor("#2d3748"))
        pdf.setFont("Helvetica", 10)
        pdf.drawString(55, current_y, item["name"])
        pdf.drawString(350, current_y, str(item["quantity"]))
        pdf.drawString(450, current_y, f"${item['price']:.2f}")
        pdf.drawString(520, current_y, f"${item_total:.2f}")
        
        current_y -= 22
        row_count += 1

    # 5. Drawing Financial Totals
    current_y -= 15
    pdf.setLineWidth(1)
    pdf.setStrokeColor(colors.HexColor("#e2e8f0"))
    pdf.line(50, current_y + 15, 562, current_y + 15)
    
    tax_total = subtotal * tax_rate
    grand_total = (subtotal + tax_total) - discount_amount

    pdf.setFont("Helvetica", 10)
    pdf.setFillColor(colors.HexColor("#4a5568"))
    pdf.drawString(410, current_y, "Subtotal:")
    pdf.drawString(520, current_y, f"${subtotal:.2f}")
    
    current_y -= 20
    pdf.drawString(410, current_y, f"Tax ({int(tax_rate * 100)}%):")
    pdf.drawString(520, current_y, f"${tax_total:.2f}")
    
    current_y -= 25
    pdf.setFillColor(colors.HexColor("#1a365d"))
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(410, current_y, "Grand Total:")
    pdf.drawString(520, current_y, f"${grand_total:.2f}")

    # 6. Payment Instructions Engine Block
    current_y -= 45
    pdf.setStrokeColor(colors.HexColor("#cbd5e0"))
    pdf.line(50, current_y + 15, 562, current_y + 15)
    
    pdf.setFillColor(colors.HexColor("#2d3748"))
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(50, current_y, "Payment Instructions:")
    
    pdf.setFont("Helvetica", 9)
    pdf.setFillColor(colors.HexColor("#718096"))
    current_y -= 18
    pdf.drawString(50, current_y, f"Method / Details: {payment_info}")

    pdf.save()
    print(f"\n✨ Success! Complete invoice saved as '{file_name}'")

# --- Interactive Terminal Loop ---
print("=== Complete Professional Invoice Engine ===")
custom_client = input("Enter Client Name: ")
inv_number = input("Enter Invoice Number: ")
due_dt = input("Enter Due Date: ")

user_items = []
while True:
    print("\n--- Add an Item ---")
    item_name = input("Item Description (or type 'done'): ")
    if item_name.lower() == 'done':
        break
    try:
        item_qty = int(input("Quantity: "))
        item_price = float(input("Unit Price: "))
        user_items.append({"name": item_name, "quantity": item_qty, "price": item_price})
    except ValueError:
        print("❌ Invalid number. Row skipped.")

print("\n--- Payment Info ---")
pay_details = input("Enter Bank details or Payment terms (e.g., Bank Transfer, Acc No: 1234): ")

if user_items:
    output_filename = f"{custom_client.lower().replace(' ', '_')}_invoice.pdf"
    create_invoice(output_filename, custom_client, inv_number, due_dt, user_items, pay_details)
else:
    print("No items added. Cancelled.")