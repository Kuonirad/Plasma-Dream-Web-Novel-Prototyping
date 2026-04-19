# MHD Levitation Engineering — Technical Reference

**Module:** Depth-5 Extension
**Date:** 19 April 2026

---

## 1. Governing Physics

### 1.1 Lorentz Force

The volumetric Lorentz force on a current-carrying plasma in an external magnetic field:

**F = ∫ (J × B) dV**

For levitation equilibrium:

**∫ (J × B) dV = mg (vertical component)**

Where:
- **J** = plasma current density vector (~10–100 A/m² in DBD filaments)
- **B** = external magnetic flux density (0.02–0.05 T from Nd magnets or electromagnets)
- **V** = plasma volume
- **m** = mass of levitated object (plasma orb + substrate)
- **g** = gravitational acceleration (9.81 m/s²)

### 1.2 Earnshaw's Theorem

Earnshaw's theorem (1842) proves that no static configuration of charges, magnets, or gravitational masses can produce a stable equilibrium in free space. For a weakly diamagnetic plasma, this means:

**∇²Φ = 0** (Laplace's equation for magnetic potential)

implies no local minimum exists in the magnetic potential energy landscape. Any equilibrium point is a saddle point — stable in some directions, unstable in others.

**Consequence:** Passive magnetic levitation of a plasma orb is impossible. Active feedback is mandatory.

### 1.3 Exceptions and Engineering Workarounds

| Method | Mechanism | Applicable? |
|--------|-----------|-------------|
| Diamagnetic levitation | χ < 0 materials in strong B gradient | Partially (plasma χ ~ -10⁻⁶) |
| Superconducting levitation | Meissner effect | No (requires cryogenics) |
| Active electromagnetic feedback | PID/Bayesian control of B(t) | **Yes — selected approach** |
| Electrodynamic (eddy current) | Time-varying B induces stabilizing currents | Partially (secondary mechanism) |

---

## 2. Engineering Implementation (Prototype 1)

### 2.1 Hardware Configuration

**Base Field Generator:**
- N52 neodymium ring magnet (OD 50 mm, ID 25 mm, H 10 mm) or
- Small electromagnet (200 turns, 0.5 A, ferrite core)
- Field strength at center: 0.02–0.05 T

**Stabilization Coils:**
- 4 orthogonal coils arranged in 2 pairs (X-axis, Y-axis)
- Each coil: 50 turns of 26 AWG magnet wire on 30 mm former
- Drive: H-bridge MOSFET driver (L298N or equivalent)
- Bandwidth: >100 Hz for stable feedback

**Position Sensing:**
- Primary: 4× Hall-effect sensors (SS49E linear) at 90° intervals
- Secondary: Optical centroid from 4D spectrogram (digital twin error signal)
- Resolution: <0.1 mm displacement detection

**Plasma Vessel:**
- 6″ (152 mm) borosilicate sphere
- Internal copper-foil dreamcatcher web
- Sealed with high-voltage feedthroughs

### 2.2 Power Budget

| Subsystem | Power (W) |
|-----------|----------|
| ZVS plasma driver | 20–40 |
| Stabilization coils (4×) | 5–15 |
| Sensors + Arduino | 1–2 |
| **Total** | **<60** |

### 2.3 Control Architecture

```
               ┌─────────────┐
               │  4D Digital  │
               │    Twin      │
               │ (WebGL2)     │
               └──────┬───────┘
                      │ unison score
                      │ + centroid error
               ┌──────▼───────┐
               │   Bayesian   │
               │   Beta       │
               │   Controller │
               └──────┬───────┘
                      │ gain K, coil currents
           ┌──────────┼──────────┐
           ▼          ▼          ▼
      ┌────────┐ ┌────────┐ ┌────────┐
      │ X-coils│ │ Y-coils│ │ Z-base │
      └────────┘ └────────┘ └────────┘
           ▲          ▲          ▲
           │          │          │
      ┌────────┐ ┌────────┐ ┌────────┐
      │Hall X  │ │Hall Y  │ │Hall Z  │
      └────────┘ └────────┘ └────────┘
```

---

## 3. Stability Analysis

### 3.1 Lyapunov Function

Define the energy-like Lyapunov candidate:

**V(x, ẋ) = ½k·x² + ½m·ẋ²**

where x is displacement from equilibrium, k is effective magnetic stiffness (negative in unstable directions without feedback).

With active feedback adding restoring force F_fb = -K_p·x - K_d·ẋ:

**V̇ = -K_d·ẋ² < 0** (for K_d > 0)

This guarantees asymptotic stability in the Lyapunov sense.

### 3.2 Bayesian Gain Scheduling

The Bayesian Beta distribution tracks the "unison" (coherence) of the plasma filament pattern:

**P(unison) = α / (α + β)**

When P(unison) > 0.85, the gain K is set to nominal. Below 0.85, gains increase proportionally to compensate for plasma instability:

**K_effective = K_nominal × (1 + γ × (0.85 - P(unison)))**

where γ is a tunable sensitivity parameter (default: 2.0).

### 3.3 Loop Timing

| Parameter | Value |
|-----------|-------|
| Sensor sampling rate | 1 kHz |
| Control loop period | <10 ms |
| Digital twin update rate | 60–120 Hz |
| Coil response time | <5 ms (L/R time constant) |

---

## 4. Emergent Behavior

When the Bayesian controller achieves stable levitation with unison >0.85:

- **Plasma breathing:** Orb radius modulates 5–10% in phase with 1–10 Hz PWM
- **Filament coherence:** Streamers self-organize into stable patterns visible through borosilicate
- **Acoustic coupling:** Plasma modulation produces faint audible tones at PWM frequency

These emergent behaviors are impossible in ground-based (non-levitated) DBD systems, where electrode proximity constrains filament dynamics.

---

## 5. Safety Warnings

- **Magnetic fields:** Pacemaker/implant exclusion zone of 30 cm from base magnet
- **Mechanical failure:** Borosilicate sphere may fall if feedback fails — soft landing pad required
- **High voltage:** ZVS output is lethal — enclosed within sealed sphere, but feedthroughs must be insulated to CSA C22.1:24
- **Hot surfaces:** Coils may reach 60–80 °C under sustained operation — thermal shutdown at 85 °C

---

## 6. References

- Earnshaw, S. (1842). On the nature of the molecular forces which regulate the constitution of the luminiferous ether. *Trans. Cambridge Phil. Soc.*, 7, 97–112.
- Brandt, E. H. (1989). Levitation in physics. *Science*, 243(4889), 349–355.
- Simon, M. D., Heflinger, L. O., & Ridgway, S. L. (1997). Spin stabilized magnetic levitation. *American Journal of Physics*, 65(4), 286–292.
- Fridman, A. (2008). *Plasma Chemistry*. Cambridge University Press.
