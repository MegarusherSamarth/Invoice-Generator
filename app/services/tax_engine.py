from decimal import Decimal, ROUND_HALF_UP
from app.models.invoice import Invoice
from app.models.tax_breakdown import TaxLine, TaxBreakdown

def is_inter_state(supplier_state: str, pos_state: str) -> bool:
    return supplier_state != pos_state

def quantize_money(x: Decimal) -> Decimal:
    return x.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

def round_invoice(total: Decimal, mode: str)-> tuple[Decimal, Decimal]:
    rounded = total.quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    adjustment = rounded - total
    return rounded, quantize_money(adjustment)

def compute_invoice_tax(inv: Invoice)-> TaxBreakdown:
    inter = is_inter_state(inv.supplier.state_code, inv.place_of_supply_state)
    lines = []
    cgst_total = sgst_total = igst_total = cess_total = subtotal = total_taxable = Decimal("0")
    
    for item in inv.items:
        base = item.quantity * item.unit_price - item.discount_pre_tax
        base = quantize_money(base)
        
        if inv.supplier.composition or item.is_exempt or item.tax_rate == 0:
            line_total = base - item.discount_post_tax
            line_total = quantize_money(line_total)
            lines.append(TaxLine(description= item.description, hsn_sac= item.hsn_sac, quantity=item.quantity, unit_price=item.unit_price, taxable_value=base, cgst=Decimal("0"), sgst=Decimal("0"), igst=Decimal("0"), cess=Decimal("0"), total=line_total))
            subtotal += line_total
            total_taxable += base
            continue
        rate = item.tax_rate / Decimal("100")
        cess_rate = item.cess_rate / Decimal("100")
        
        if inter:
            igst = quantize_money(base*rate)
            cgst = sgst = Decimal("0")
        else: 
            cgst = quantize_money(base*(rate/2))
            sgst = quantize_money(base*(rate/2))
            igst = Decimal("0")
            
        cess = quantize_money(base*cess_rate)
        line_total = base + cgst + sgst + igst + cess - item.discount_post_tax
        line_total = quantize_money(line_total)
        
        lines.append(TaxLine(description=item.description, hsn_sac=item.hsn_sac, quantity=item.quantity, unit_price=item.unit_price, taxable_value= base, cgst=cgst, sgst=sgst, igst=igst, cess=cess, total= line_total))
        
        cgst_total += cgst
        sgst_total += sgst
        igst_total += igst
        cess_total += cess
        subtotal += line_total
        total_taxable += base
        
    # Add Freight, Insurance, Other charges to taxable base
    extras = inv.freight + inv.insurance + inv.other_charges
    extras = quantize_money(extras)
    
    if (extras>0):
        rate = Decimal("18") / Decimal("100") # Decimal rate for extras
        
        if inter:
            igst = quantize_money(extras*rate)
            igst_total += igst
        else:
            half = quantize_money(extras*(rate/2))
            cgst_total += half
            sgst_total += half
        subtotal += extras
        total_taxable += extras
    
    grand_total, rounding_adj = round_invoice(subtotal, inv.rounding)
    
    return TaxBreakdown(
        lines=lines, total_taxable=quantize_money(total_taxable), cgst_total=quantize_money(cgst_total), sgst_total=quantize_money(sgst_total), igst_total= quantize_money(igst_total), cess_total=quantize_money(cess_total), subtotal=quantize_money(subtotal), rounding_adjustment=rounding_adj, grand_total=grand_total
    )