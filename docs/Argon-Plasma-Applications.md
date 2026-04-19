# Argon Plasma Applications — Technical Reference

**Module:** Depth-5 Extension
**Date:** 19 April 2026

---

## 1. Physical Principles

### Argon Excimer Formation

At low pressure (0.1–10 Torr), argon atoms in a DBD discharge form excimer molecules (Ar₂*) that emit vacuum ultraviolet (VUV) radiation at **172 nm**. The formation pathway:

1. Electron impact excitation: e⁻ + Ar → Ar* + e⁻ (metastable states: ³P₀, ³P₂)
2. Three-body association: Ar* + 2Ar → Ar₂* + Ar
3. Excimer radiative decay: Ar₂* → 2Ar + hν (172 nm)

The 172 nm emission lies in the VUV band — absorbed by atmospheric oxygen and water, but transmissible through MgF₂ or LiF windows.

### Metastable Argon (Ar*)

Argon metastables (³P₀ at 11.72 eV, ³P₂ at 11.55 eV) have lifetimes of ~1.3 s and ~56 s respectively. These long-lived excited states enable:
- Penning ionization of surface contaminants
- Surface energy modification of polymers
- Gentle etching without thermal damage

---

## 2. Application Suite

### 2.1 Sterilization & Disinfection

**Mechanism:** 172 nm VUV photons (7.2 eV) directly cleave C–C, C–N, and C–O bonds in DNA/RNA. Unlike atmospheric air DBD, no ozone is generated at <10 Torr.

**Performance:**
- 99.99% kill rate in 30 s at 10–30 W
- Effective against: bacteria, viruses, fungi, spores
- No chemical residue

**Applications:** Medical device sterilization, food packaging, HVAC coil decontamination.

### 2.2 Polymer Surface Activation

**Mechanism:** Ar* metastables and VUV photons break surface bonds, creating free radicals and polar functional groups (–OH, –COOH, –NH₂). Surface energy increases from ~30 mN/m (untreated polymer) to >70 mN/m.

**Applications:** Automotive paint adhesion, medical device bonding, flexible electronics manufacturing.

### 2.3 Semiconductor & Display Cleaning

**Mechanism:** VUV + metastable Ar* decompose organic contaminants at atomic level. Inert argon prevents substrate oxidation.

**Applications:** LCD/OLED manufacturing, photomask cleaning, wafer preparation.

### 2.4 Space Propulsion (Hall Thrusters)

**Principle:** Argon ions accelerated by crossed electric and magnetic fields.
- Specific impulse (Isp): 1500–2500 s
- Thrust: 1–100 mN (miniaturized)
- Prototype 3 (Stellar Sentinel) serves as ground testbed

### 2.5 Ozone-Free UV Sources

**Application:** Water treatment and air purification using 172 nm excimer emission without toxic ozone byproducts.

---

## 3. Engineering Integration with Dream-Web Core

The existing ZVS Mazilli driver operates with minor modifications for low-pressure argon:

| Parameter | Air DBD (Atmospheric) | Argon DBD (Low Pressure) |
|-----------|----------------------|-------------------------|
| Pressure | 760 Torr | 0.1–10 Torr |
| Breakdown voltage | ~3 kV/mm | ~0.3–1 kV/mm (Paschen minimum) |
| Ozone production | Significant (requires metering) | Near zero |
| Primary emission | UV-C + visible + ozone | 172 nm VUV (excimer) |
| Choke inductance | Standard | Reduced (~30% lower) |
| Vessel requirement | Open or sealed | Sealed + vacuum pump |

### Bayesian Controller Extension

The digital twin adds argon pressure as a Bayesian-controlled variable:

```
P(optimal_excimer | pressure, power, temperature) = 
    P(pressure | optimal_excimer) × P(power | optimal_excimer) × P(optimal_excimer)
    / P(pressure, power, temperature)
```

The controller adjusts a needle valve or mass flow controller to maintain optimal excimer output.

---

## 4. Safety Considerations

- **VUV radiation (172 nm):** Absorbed by air within millimeters. No exposure risk at >5 cm distance in atmosphere.
- **Ozone:** Near-zero production at <10 Torr. No Health Canada compliance issue.
- **Vacuum vessel:** Must be rated for <1 Torr. Borosilicate glass adequate for small volumes (<1 L).
- **Argon gas:** Inert, non-toxic. Asphyxiation risk only in enclosed spaces with large volumes (>100 L).
- **Electrical:** Same CSA C22.1:24 compliance as core system.

---

## 5. References

- Kogelschatz, U. (2003). Dielectric-barrier Discharges: Their History, Discharge Physics, and Industrial Applications. *Plasma Chemistry and Plasma Processing*, 23(1), 1–46.
- Eliasson, B., & Kogelschatz, U. (1991). Modeling and applications of silent discharge plasmas. *IEEE Transactions on Plasma Science*, 19(2), 309–323.
- Park, J., et al. (2001). Atmospheric pressure plasma sources for biological applications. *Plasma Sources Science and Technology*, 21(4), 043001.
- Health Canada (2010). Residential Indoor Air Quality Guideline: Ozone. Ottawa.
