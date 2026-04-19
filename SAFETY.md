# SAFETY.md — Plasma Dream-Web Safety Protocol

**Version:** 2.2
**Date:** 19 April 2026
**Compliance:** Health Canada RIAQG, CSA C22.1:24

---

## ⚠️ GENERAL WARNINGS

This project involves **high-voltage electrical discharges** (3–15 kV AC), **ultraviolet radiation**, and **reactive oxygen species (ROS)**. Improper construction or operation can cause **electrical shock, burns, eye damage, or respiratory harm**.

**Do not build or operate any prototype without:**
1. Reading this entire document
2. Understanding basic high-voltage safety
3. Having appropriate personal protective equipment (PPE)
4. Verifying ozone levels with a calibrated sensor

---

## 1. Electrical Safety (CSA C22.1:24 Compliance)

### 1.1 Power Envelope
- All prototypes operate at **<50 W input power**
- Input voltage: 12–24 VDC from commercial power supply
- Output: 3–15 kV AC at 20–50 kHz (ZVS resonant)

### 1.2 Mandatory Precautions
- **Enclosure:** All high-voltage components must be enclosed in insulating housing
- **Grounding:** Chassis ground connected to power supply ground
- **Isolation:** High-voltage output isolated from low-voltage control (Arduino)
- **Silicone sealing:** All electrode edges sealed with high-voltage silicone
- **Fusing:** 5A fuse on 12V input; thermal fuse on flyback transformer
- **Labeling:** "DANGER: HIGH VOLTAGE" labels on all enclosures (bilingual English/French for NB compliance)

### 1.3 Capacitor Discharge
- ZVS tank capacitor (0.68 µF at up to 400V) stores lethal energy
- **Always discharge capacitors** with a 10 kΩ bleeder resistor before servicing
- Wait minimum 5 minutes after power-off before touching any component

---

## 2. Ozone Exposure (Health Canada RIAQG)

### 2.1 Regulatory Limit
- **Maximum residential exposure:** 20 ppb (40 µg/m³) averaged over 8 hours
- Source: Health Canada Residential Indoor Air Quality Guideline for Ozone

### 2.2 Monitoring Protocol
- **MQ-131 ozone sensor** connected to Arduino Nano
- Continuous monitoring during all atmospheric-pressure DBD operation
- **Auto-shutoff threshold:** 15 ppb (75% of limit, providing safety margin)
- **Audible alarm threshold:** 10 ppb (early warning)

### 2.3 Ventilation Requirements
- Minimum room ventilation: 2 air changes per hour (ACH)
- Recommended: operate near open window or with exhaust fan
- **Never operate in sealed/unventilated space**

### 2.4 Argon Low-Pressure DBD
- At <10 Torr argon pressure: ozone production is **near zero**
- No Health Canada ozone compliance issue for sealed argon systems
- Verify seal integrity before each operation

---

## 3. Ultraviolet Radiation

### 3.1 Atmospheric DBD
- UV-C emission (200–280 nm) at low intensity
- Standard borosilicate glass absorbs >99% of UV below 300 nm
- **No direct viewing** of bare discharge without glass barrier

### 3.2 Argon Excimer (172 nm VUV)
- VUV radiation absorbed by air within **millimeters**
- No exposure risk at >5 cm in atmosphere
- **MgF₂ or LiF windows** required if VUV transmission is desired (e.g., sterilization applications)
- **Never look directly** at VUV source through transmitting optics
- UV-rated safety glasses required when working with VUV-transmitting windows

---

## 4. MHD / Magnetic Field Safety

### 4.1 Permanent Magnets
- N52 neodymium magnets are **extremely strong** — pinch hazard
- Keep magnets away from electronic devices, credit cards, pacemakers
- **Pacemaker/medical implant exclusion zone: 30 cm minimum**

### 4.2 Electromagnet Coils
- Coils may reach 60–80 °C under sustained operation
- **Thermal shutdown at 85 °C** (thermistor + Arduino control)
- Burn hazard — do not touch coils during or immediately after operation

### 4.3 Mechanical Failure
- If feedback control fails, levitated orb will fall
- **Soft landing pad** (foam or silicone mat) required beneath orb
- Borosilicate sphere may shatter on hard impact — eye protection required

---

## 5. Gas Safety (Argon Systems)

### 5.1 Argon Properties
- Inert, non-toxic, non-flammable
- Heavier than air (density 1.784 kg/m³ vs air 1.225 kg/m³)
- **Asphyxiation risk** in enclosed spaces with large volumes (>100 L release)

### 5.2 Vacuum Vessel
- Borosilicate vessels rated for <1 Torr adequate for small volumes (<1 L)
- **Implosion risk** — do not use cracked or chipped glass
- Safety shield (polycarbonate) recommended around vacuum vessels >500 mL
- Pressure relief valve required on vessels >1 L

---

## 6. Prototype-Specific Warnings

| Prototype | Additional Hazard | Mitigation |
|-----------|-------------------|------------|
| 1 (MHD Orb) | Falling sphere, strong magnets | Landing pad, magnet handling gloves |
| 2 (Greenhouse) | Plant proximity to HV, ozone on plants | Sealed electrode panel, sensor |
| 3 (Zero-G) | Vacuum vessel, argon release | Safety shield, ventilation |
| 4 (Underwater) | Water + electricity | IP68 rating mandatory, GFCI on all circuits |
| 5 (Wall) | Large panel, audio coupling | Secure mounting, hearing protection at >85 dB |
| 6 (Canopy) | Sleep proximity, prolonged ozone | Ultra-low ozone threshold (5 ppb), timer limit 8 hr |
| 7 (Urban) | Scale, public exposure | Professional electrical installation, municipal permits |

---

## 7. Emergency Procedures

### Electrical Shock
1. **Do not touch the person** if they are still in contact with the circuit
2. Disconnect power at the source (unplug or switch off breaker)
3. Call 911 / administer CPR if trained
4. All ZVS systems have <50 W capacity but flyback output is potentially lethal

### Ozone Overexposure
1. Move to fresh air immediately
2. Symptoms: coughing, chest tightness, shortness of breath
3. Seek medical attention if symptoms persist
4. Auto-shutoff should prevent overexposure — verify sensor function before each session

### Glass Breakage
1. Do not handle broken borosilicate with bare hands
2. Sweep, do not vacuum (fine glass particles)
3. If argon vessel breaks: ventilate room, no immediate toxicity concern

---

## 8. PPE Requirements

| Activity | Required PPE |
|----------|-------------|
| ZVS assembly/testing | Insulating gloves (Class 0), safety glasses |
| Atmospheric DBD operation | Ozone monitor, ventilation |
| Argon/vacuum work | Safety glasses, hearing protection |
| MHD magnet handling | Magnet-rated gloves, eye protection |
| VUV optics work | UV-rated safety glasses |

---

## 9. Disclaimer

This project is provided for **educational and research purposes only**. The authors are not responsible for injuries, damages, or regulatory violations resulting from construction or operation of any prototype described herein. All builders assume full responsibility for compliance with local electrical codes, safety regulations, and building permits.

**Always consult a licensed electrician** for permanent installations (especially Prototype 7 — Urban Lattice).

---

*Safety is not optional. Verify before you energize.*
