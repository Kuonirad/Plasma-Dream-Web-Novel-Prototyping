/**
 * Digital Twin Validation Tests
 * ==============================
 * 
 * Validates core spectral template, Bayesian tracker,
 * and point cloud generator against known physics.
 * 
 * Run: node tests/digital-twin-validation.js
 */

const {
  CONFIG,
  lorentzian,
  generatePlasmaTemplate,
  BayesianBetaTracker,
  SpectrogramPointCloud
} = require('../src/digital-twin/spectrogram-4d.js');

let passed = 0;
let failed = 0;

function assert(condition, message) {
  if (condition) {
    console.log(`  ✅ ${message}`);
    passed++;
  } else {
    console.log(`  ❌ FAIL: ${message}`);
    failed++;
  }
}

function assertApprox(actual, expected, tolerance, message) {
  const diff = Math.abs(actual - expected);
  assert(diff < tolerance, `${message} (got ${actual.toFixed(6)}, expected ~${expected}, tol=${tolerance})`);
}

// ============================================================
console.log('\n1. Lorentzian Line Profile Tests');
// ============================================================

// Peak value at center
const peakVal = lorentzian(35000, 35000, 2000);
assert(peakVal > 0, 'Lorentzian peak is positive');

// Symmetry
const left = lorentzian(33000, 35000, 2000);
const right = lorentzian(37000, 35000, 2000);
assertApprox(left, right, 1e-10, 'Lorentzian is symmetric');

// HWHM: value at f0 ± gamma should be half the peak
const halfMax = lorentzian(35000 + 2000, 35000, 2000);
assertApprox(halfMax / peakVal, 0.5, 0.001, 'HWHM is correct');

// ============================================================
console.log('\n2. Spectral Template Tests');
// ============================================================

const template = generatePlasmaTemplate();

assert(template.length === CONFIG.FREQ_BINS, `Template has ${CONFIG.FREQ_BINS} bins`);
assert(Math.max(...template) === 1.0, 'Template normalized to 1.0');
assert(Math.min(...template) >= 0, 'Template has no negative values');

// Peak should be near carrier frequency bin
const carrierBin = Math.round(
  (CONFIG.CARRIER_FREQ - CONFIG.FREQ_MIN) / 
  (CONFIG.FREQ_MAX - CONFIG.FREQ_MIN) * CONFIG.FREQ_BINS
);
assert(template[carrierBin] > 0.9, 'Peak near carrier frequency');

// ============================================================
console.log('\n3. Bayesian Beta Tracker Tests');
// ============================================================

const tracker = new BayesianBetaTracker();

// Initial state
assertApprox(tracker.unison, 0.5, 0.01, 'Initial unison is ~0.5');
assert(tracker.variance > 0, 'Initial variance is positive');

// Feed high-coherence measurements
for (let i = 0; i < 100; i++) {
  tracker.update(0.9);
}
assert(tracker.unison > 0.8, 'Unison rises with high-coherence input');

// Feed low-coherence measurements
for (let i = 0; i < 200; i++) {
  tracker.update(0.2);
}
assert(tracker.unison < 0.5, 'Unison drops with low-coherence input');

// Reset
tracker.reset();
assertApprox(tracker.unison, 0.5, 0.01, 'Reset returns to prior');

// Texture depth mapping
tracker.update(0.95);
tracker.update(0.95);
tracker.update(0.95);
for (let i = 0; i < 50; i++) tracker.update(0.95);
assert(tracker.textureDepth >= 1 && tracker.textureDepth <= 5, 'Texture depth in [1,5]');

// ============================================================
console.log('\n4. Point Cloud Generator Tests');
// ============================================================

const cloud = new SpectrogramPointCloud();

// Generate one frame
const frame = cloud.update(1/60);

assert(frame.positions.length === CONFIG.NUM_POINTS * 3, 'Correct position array size');
assert(frame.colors.length === CONFIG.NUM_POINTS * 4, 'Correct color array size (RGBA)');
assert(frame.coherences.length === CONFIG.NUM_POINTS, 'Correct coherence array size');
assert(typeof frame.unison === 'number', 'Unison is a number');
assert(frame.unison >= 0 && frame.unison <= 1, 'Unison in [0, 1]');
assert(frame.textureDepth >= 1 && frame.textureDepth <= 5, 'Texture depth valid');

// PWM control
cloud.setPWM(7.5, 0.7);
const frame2 = cloud.update(1/60);
assert(typeof frame2.pwmValue === 'number', 'PWM value returned after setPWM');

// Multiple frames stability
let stable = true;
for (let i = 0; i < 100; i++) {
  try {
    cloud.update(1/60);
  } catch (e) {
    stable = false;
    break;
  }
}
assert(stable, '100 consecutive frames without error');

// ============================================================
console.log('\n' + '='.repeat(50));
console.log(`Results: ${passed} passed, ${failed} failed`);
console.log('='.repeat(50));

if (failed > 0) {
  process.exit(1);
}
