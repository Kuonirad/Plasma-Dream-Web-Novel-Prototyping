#!/usr/bin/env python3
"""
Bill of Materials Generator for Plasma Dream-Web
=================================================

Generates formatted BOM with pricing from Bathurst-sourced suppliers.
All prices in CAD. Shipping estimates for Bathurst, NB.

Author: Kevin Kull — KullAILabs
Date: 19 April 2026
License: MIT
"""

import json

BOM_CORE = [
    {
        "item": "IRFP250 N-Channel MOSFET",
        "quantity": 2,
        "unit_price_cad": 4.25,
        "source": "DigiKey.ca",
        "shipping": "Next-day to Bathurst",
        "notes": "ZVS Mazilli half-bridge"
    },
    {
        "item": "MKP Capacitor 0.68 µF 400V",
        "quantity": 1,
        "unit_price_cad": 4.20,
        "source": "DigiKey.ca",
        "shipping": "Next-day to Bathurst",
        "notes": "ZVS tank capacitor"
    },
    {
        "item": "CRT Flyback Transformer (salvaged)",
        "quantity": 1,
        "unit_price_cad": 5.00,
        "source": "Local recycling / eBay",
        "shipping": "Local pickup or 5-day",
        "notes": "High-voltage step-up. Salvage preferred."
    },
    {
        "item": "Arduino Nano (ATmega328P)",
        "quantity": 1,
        "unit_price_cad": 12.00,
        "source": "Amazon.ca / The Source (Moncton)",
        "shipping": "2-day / same-day pickup",
        "notes": "PWM + ozone monitoring controller"
    },
    {
        "item": "Copper Foil Tape 25mm × 30m",
        "quantity": 1,
        "unit_price_cad": 14.00,
        "source": "Amazon.ca",
        "shipping": "2-day to Bathurst",
        "notes": "Electrode web fabrication"
    },
    {
        "item": "Borosilicate Glass 200×200×2mm",
        "quantity": 1,
        "unit_price_cad": 18.00,
        "source": "Amazon.ca",
        "shipping": "2-day to Bathurst",
        "notes": "Dielectric substrate. UV-absorbing."
    },
    {
        "item": "High-Voltage Silicone Sealant",
        "quantity": 1,
        "unit_price_cad": 9.00,
        "source": "Amazon.ca",
        "shipping": "2-day to Bathurst",
        "notes": "Edge sealing for discharge containment"
    },
    {
        "item": "Misc (wire, connectors, PCB, resistors)",
        "quantity": 1,
        "unit_price_cad": 12.00,
        "source": "DigiKey.ca",
        "shipping": "Next-day to Bathurst",
        "notes": "Assorted passives and interconnects"
    },
    {
        "item": "MQ-131 Ozone Sensor Module",
        "quantity": 1,
        "unit_price_cad": 8.50,
        "source": "Amazon.ca",
        "shipping": "2-day to Bathurst",
        "notes": "Health Canada compliance monitoring"
    },
    {
        "item": "12V 5A DC Power Supply",
        "quantity": 1,
        "unit_price_cad": 13.20,
        "source": "Amazon.ca",
        "shipping": "2-day to Bathurst",
        "notes": "Main system power"
    }
]


def generate_bom(components=None, output_format="markdown"):
    """Generate formatted BOM."""
    if components is None:
        components = BOM_CORE
    
    total_first = sum(c["quantity"] * c["unit_price_cad"] for c in components)
    # Subsequent units: exclude one-time items (flyback, misc)
    reusable_savings = 5.00 + 12.00  # flyback + misc already on hand
    total_subsequent = total_first - reusable_savings
    # Also subtract reduced copper foil usage
    total_subsequent -= 5.00
    
    if output_format == "markdown":
        lines = [
            "# Bill of Materials — Plasma Dream-Web Core Build",
            "",
            f"**Location:** Bathurst, New Brunswick, Canada",
            f"**Date:** 19 April 2026",
            f"**Currency:** CAD",
            "",
            "| # | Item | Qty | Unit Price | Total | Source |",
            "|---|------|-----|-----------|-------|--------|"
        ]
        
        for i, c in enumerate(components, 1):
            total = c["quantity"] * c["unit_price_cad"]
            lines.append(
                f"| {i} | {c['item']} | {c['quantity']} | "
                f"${c['unit_price_cad']:.2f} | ${total:.2f} | {c['source']} |"
            )
        
        lines.extend([
            "",
            f"**Total (first unit): ${total_first:.2f} CAD**",
            f"**Total (subsequent units): ~${total_subsequent:.2f} CAD**",
            "",
            "## Shipping Notes",
            ""
        ])
        
        for c in components:
            lines.append(f"- **{c['item']}**: {c['shipping']} — {c['notes']}")
        
        return "\n".join(lines)
    
    elif output_format == "json":
        return json.dumps({
            "bom": components,
            "total_first_unit_cad": total_first,
            "total_subsequent_cad": total_subsequent,
            "location": "Bathurst, NB, Canada",
            "date": "2026-04-19"
        }, indent=2)


if __name__ == "__main__":
    print(generate_bom())
    print("\n\n--- JSON Format ---\n")
    print(generate_bom(output_format="json"))
