"""
Bayesian Beta Controller for Plasma Dream-Web
==============================================

Real-time Bayesian feedback controller using Beta distribution
for coherence/unison tracking in DBD plasma systems.

Integrates with:
- 4D Digital Twin spectrogram (WebGL2)
- ZVS PWM modulation
- MHD stabilization coils (Prototype 1)
- Argon pressure control (Prototype 3)

Author: Kevin Kull — KullAILabs
Date: 19 April 2026
License: MIT
"""

import numpy as np
from dataclasses import dataclass, field
from typing import Optional, Tuple
import json
import time


@dataclass
class BayesianBetaController:
    """
    Bayesian Beta distribution controller for plasma coherence tracking.
    
    The controller maintains a Beta(alpha, beta) posterior over the
    'unison' (coherence) parameter, updating in real-time from
    spectral measurements.
    
    Unison > 0.85 indicates stable, coherent plasma filament patterns.
    """
    
    # Prior parameters (weakly informative)
    alpha: float = 2.0
    beta: float = 2.0
    
    # Control thresholds
    unison_target: float = 0.85
    unison_critical: float = 0.60
    
    # Gain scheduling
    k_nominal: float = 1.0
    gamma_sensitivity: float = 2.0
    
    # Safety limits
    max_pwm_duty: float = 0.95
    min_pwm_duty: float = 0.05
    max_coil_current_a: float = 2.0
    thermal_shutdown_c: float = 85.0
    ozone_shutdown_ppb: float = 15.0
    
    # State tracking
    history: list = field(default_factory=list)
    _loop_count: int = 0
    
    @property
    def unison(self) -> float:
        """Current unison estimate (mean of Beta posterior)."""
        return self.alpha / (self.alpha + self.beta)
    
    @property
    def unison_variance(self) -> float:
        """Variance of unison estimate."""
        ab = self.alpha + self.beta
        return (self.alpha * self.beta) / (ab ** 2 * (ab + 1))
    
    @property
    def confidence_interval_95(self) -> Tuple[float, float]:
        """95% credible interval for unison."""
        from scipy import stats
        dist = stats.beta(self.alpha, self.beta)
        return (dist.ppf(0.025), dist.ppf(0.975))
    
    @property
    def effective_gain(self) -> float:
        """Gain-scheduled control gain based on current unison."""
        if self.unison >= self.unison_target:
            return self.k_nominal
        deficit = self.unison_target - self.unison
        return self.k_nominal * (1 + self.gamma_sensitivity * deficit)
    
    def update(self, coherence_measurement: float) -> dict:
        """
        Update Bayesian posterior with new coherence measurement.
        
        Args:
            coherence_measurement: Float in [0, 1] from spectral analysis.
                1.0 = perfectly coherent filaments
                0.0 = completely stochastic
        
        Returns:
            dict with control outputs and diagnostics
        """
        # Input sanitization and bounds check (Security: Prevent DoS via crash)
        try:
            val = float(coherence_measurement)
            if np.isnan(val):
                val = 0.0
        except (ValueError, TypeError):
            val = 0.0
        coherence_measurement = float(np.clip(val, 0.0, 1.0))

        # Bayesian update: Beta-Bernoulli conjugate
        # Treat measurement as soft evidence
        self.alpha += coherence_measurement
        self.beta += (1.0 - coherence_measurement)
        
        # Prevent posterior from becoming too peaked (memory decay)
        decay = 0.999
        self.alpha *= decay
        self.beta *= decay
        
        # Ensure minimum values
        self.alpha = max(self.alpha, 1.0)
        self.beta = max(self.beta, 1.0)
        
        self._loop_count += 1
        
        # Compute control outputs
        outputs = self._compute_control_outputs(coherence_measurement)
        
        # Log
        record = {
            "loop": self._loop_count,
            "timestamp": time.time(),
            "measurement": coherence_measurement,
            "unison": self.unison,
            "variance": self.unison_variance,
            "gain": self.effective_gain,
            "outputs": outputs
        }
        self.history.append(record)
        
        return outputs
    
    def _compute_control_outputs(self, measurement: float) -> dict:
        """Compute all control outputs from current state."""
        gain = self.effective_gain
        
        # PWM duty cycle: higher unison → smoother, lower duty
        pwm_duty = np.clip(
            0.5 + 0.3 * (self.unison - self.unison_target) * gain,
            self.min_pwm_duty,
            self.max_pwm_duty
        )
        
        # PWM frequency: 1-10 Hz modulation
        pwm_freq_hz = np.clip(
            5.0 - 3.0 * (self.unison - self.unison_target) * gain,
            1.0,
            10.0
        )
        
        # Texture depth: 1-5 layers based on unison
        texture_depth = int(np.clip(
            1 + 4 * self.unison,
            1, 5
        ))
        
        # MHD coil current (Prototype 1 only)
        coil_current = np.clip(
            1.0 * gain * (1.0 - self.unison + 0.5),
            0.0,
            self.max_coil_current_a
        )
        
        # System status
        if self.unison >= self.unison_target:
            status = "STABLE"
        elif self.unison >= self.unison_critical:
            status = "ADJUSTING"
        else:
            status = "CRITICAL"
        
        return {
            "pwm_duty": round(float(pwm_duty), 4),
            "pwm_freq_hz": round(float(pwm_freq_hz), 2),
            "texture_depth": texture_depth,
            "coil_current_a": round(float(coil_current), 3),
            "effective_gain": round(float(gain), 3),
            "status": status,
            "unison": round(float(self.unison), 4),
            "alpha": round(float(self.alpha), 2),
            "beta": round(float(self.beta), 2)
        }
    
    def check_safety(self, ozone_ppb: float, temperature_c: float) -> dict:
        """
        Check safety thresholds and return shutdown signals.
        
        Args:
            ozone_ppb: Current ozone level from MQ-131 sensor
            temperature_c: Coil/system temperature
        
        Returns:
            dict with safety status and any required actions
        """
        actions = []
        safe = True
        
        if ozone_ppb > self.ozone_shutdown_ppb:
            actions.append(f"OZONE_SHUTDOWN: {ozone_ppb:.1f} ppb > {self.ozone_shutdown_ppb} ppb limit")
            safe = False
        
        if temperature_c > self.thermal_shutdown_c:
            actions.append(f"THERMAL_SHUTDOWN: {temperature_c:.1f}°C > {self.thermal_shutdown_c}°C limit")
            safe = False
        
        if ozone_ppb > 10.0:
            actions.append(f"OZONE_WARNING: {ozone_ppb:.1f} ppb approaching limit")
        
        if temperature_c > 70.0:
            actions.append(f"THERMAL_WARNING: {temperature_c:.1f}°C elevated")
        
        return {
            "safe": safe,
            "actions": actions,
            "ozone_ppb": ozone_ppb,
            "temperature_c": temperature_c
        }
    
    def export_state(self) -> str:
        """Export current state as JSON for digital twin communication."""
        return json.dumps({
            "alpha": self.alpha,
            "beta": self.beta,
            "unison": self.unison,
            "variance": self.unison_variance,
            "gain": self.effective_gain,
            "loop_count": self._loop_count,
            "history_length": len(self.history)
        }, indent=2)
    
    def reset(self):
        """Reset to prior state."""
        self.alpha = 2.0
        self.beta = 2.0
        self.history = []
        self._loop_count = 0


def simulate_plasma_session(duration_s: int = 60, dt: float = 0.01):
    """
    Simulate a plasma session with synthetic coherence data.
    
    Demonstrates controller behavior during startup, stable operation,
    and perturbation recovery.
    """
    controller = BayesianBetaController()
    
    print("=" * 60)
    print("Plasma Dream-Web — Bayesian Beta Controller Simulation")
    print("=" * 60)
    
    steps = int(duration_s / dt)
    
    for i in range(steps):
        t = i * dt
        
        # Synthetic coherence signal
        # Phase 1 (0-10s): startup ramp
        # Phase 2 (10-40s): stable with noise
        # Phase 3 (40-50s): perturbation
        # Phase 4 (50-60s): recovery
        if t < 10:
            base = 0.3 + 0.05 * t
        elif t < 40:
            base = 0.85 + 0.05 * np.sin(2 * np.pi * 0.1 * t)
        elif t < 50:
            base = 0.5 + 0.1 * np.sin(2 * np.pi * 0.5 * t)
        else:
            base = 0.7 + 0.02 * (t - 50)
        
        measurement = np.clip(base + np.random.normal(0, 0.05), 0, 1)
        
        outputs = controller.update(measurement)
        
        # Print status every 5 seconds
        if i % int(5 / dt) == 0:
            print(f"\nt={t:.1f}s | Status: {outputs['status']}")
            print(f"  Unison: {outputs['unison']:.4f} | Gain: {outputs['effective_gain']:.3f}")
            print(f"  PWM: {outputs['pwm_duty']:.3f} @ {outputs['pwm_freq_hz']:.1f} Hz")
            print(f"  Texture: {outputs['texture_depth']}/5 | Coil: {outputs['coil_current_a']:.3f} A")
    
    print("\n" + "=" * 60)
    print("Simulation complete.")
    print(f"Total loops: {controller._loop_count}")
    print(f"Final unison: {controller.unison:.4f}")
    print(controller.export_state())


if __name__ == "__main__":
    simulate_plasma_session()
