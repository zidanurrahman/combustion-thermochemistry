# Combustion Thermochemistry & Energy Analysis — Natural Gas Fired Industrial Plant

> **Independent Chemical Engineering Project**
> Chemical Thermodynamics · Combustion Chemistry · Flue Gas Analysis · Heat Recovery
> *Chemistry and Engineering of Organic Compounds | Petrochemistry and Carbochemistry*

---

## What This Project Does

Performs a **chemical thermodynamic analysis of natural gas combustion** applied to the Siddhirganj 335MW Combined Cycle Power Plant, Narayanganj, Bangladesh — analyzed from a **chemical engineering perspective** focused on combustion chemistry, flue gas behavior, and heat recovery potential.

This is the same type of analysis used to design and optimize **fired heaters, reformer furnaces, and process burners** in petrochemical plants.

---

## Why This Is Relevant to Petrochemistry

Every petrochemical facility uses fired heaters and combustion systems:

| Petrochemical Application | Combustion Role |
|--------------------------|----------------|
| Naphtha reforming | Fired heater to reach reaction temperature |
| Steam cracking | Cracking furnace — combustion controls severity |
| Distillation columns | Reboiler fired duty |
| Hydrogen production | Steam methane reformer furnace |
| Carbochemical plants | Coal/coke combustion for process heat |

Understanding combustion enthalpy, flue gas composition, adiabatic flame temperature, and heat recovery directly applies to all of the above.

---

## Analysis Performed

### 1. Combustion Enthalpy (Hess's Law)
```
CH₄ + 2O₂ → CO₂ + 2H₂O(g)
ΔH°comb = ΣΔHf°(products) − ΣΔHf°(reactants)
        = −802.3 kJ/mol CH₄
LHV     ≈ 50,040 kJ/kg
```

### 2. Air Requirement (Stoichiometric & Excess)
```
Stoichiometric O₂     : 2.0 mol / mol CH₄
Stoichiometric air    : 9.52 mol / mol CH₄
Mass air/fuel ratio   : 17.2 kg air / kg CH₄
At 20% excess air     : 11.43 mol air / mol CH₄
```

### 3. Flue Gas Composition (at 20% excess air)

| Component | Moles (per mol CH₄) | Wet % | Dry % |
|-----------|--------------------|----|-----|
| CO₂ | 1.000 | 8.4% | 10.6% |
| H₂O | 2.000 | 16.7% | — |
| N₂ | 9.043 | 75.6% | 85.8% |
| O₂ (excess) | 0.381 | 3.2% | 3.6% |

### 4. Adiabatic Flame Temperature
```
Estimated T_adiabatic ≈ 2,030°C (stoichiometric)
Actual flame T lower due to heat losses and dissociation
Excess air reduces flame temperature — key operational tradeoff
```

### 5. Heat Recovery Analysis
```
Reducing stack temperature: 400°C → 150°C
Recoverable heat: ~12–15% of LHV
→ Every 55°C reduction in stack temperature ≈ 1% efficiency gain
```

---

## Key Engineering Insight

**Lowering stack temperature is the single most effective way to improve fired heater efficiency.** The plot of thermal efficiency vs stack temperature shows clearly that operating below 150°C stack temperature is the target in modern petrochemical plant design — and this is achievable through economizers and air preheaters, which recover energy from the flue gas stream before it exits to atmosphere.

---

## Plots Generated

| Plot | Description |
|------|-------------|
| Flue gas composition | CO₂, H₂O, N₂, O₂ vs excess air % |
| Flame temperature | Adiabatic flame temperature vs excess air |
| Efficiency curve | Thermal efficiency vs stack temperature with optimal zone marked |

---

## How to Run

```bash
pip install numpy matplotlib
python combustion_analysis.py
```

Output: full thermochemistry report in terminal + `combustion_analysis_results.png`

---

## Data Sources

- Thermodynamic data (ΔHf°): NIST WebBook standard values
- Plant reference data: publicly available information, Siddhirganj 335MW CCPP, Bangladesh
- AIChE thermodynamics curriculum (reference for method)

---

## Skills Demonstrated

- Combustion thermochemistry (Hess's Law, enthalpy calculations)
- Stoichiometric and excess air calculations
- Flue gas composition analysis
- Adiabatic flame temperature estimation
- Heat recovery and thermal efficiency analysis
- Python scientific computing applied to chemical engineering problems

---

*Zidanur Rahman | Independent Chemical Engineering Study | 2025*
*Narayanganj, Bangladesh | Prepared as part of Romanian Government Scholarship application*
