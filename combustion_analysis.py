"""
=============================================================
Combustion Thermochemistry & Energy Analysis
Natural Gas Fired Industrial Plant — Siddhirganj, Bangladesh
=============================================================
Author      : Zid
Field       : Chemical Thermodynamics / Energy Systems
Subject     : Chemistry and Engineering of Organic Compounds,
              Petrochemistry and Carbochemistry
Description :
    Chemical thermodynamic analysis of natural gas combustion
    and flue gas behavior, applied to the Siddhirganj 335MW
    Combined Cycle Power Plant, Narayanganj, Bangladesh.

    Focuses on combustion chemistry, flue gas composition,
    heat recovery potential, and thermal efficiency —
    all directly relevant to fired heaters and furnaces
    in petrochemical plant design.

Key Topics:
    - Standard enthalpy of combustion (Hess's Law)
    - Adiabatic flame temperature estimation
    - Stoichiometric and excess air calculations
    - Flue gas composition analysis
    - Heat recovery from exhaust streams
    - Thermal efficiency and specific fuel consumption
=============================================================
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


# ─────────────────────────────────────────────────────────────
# THERMODYNAMIC DATA
# ─────────────────────────────────────────────────────────────

# Standard enthalpies of formation at 298 K (kJ/mol)
# Source: NIST Webbook standard values
Hf_298 = {
    'CH4':  -74.87,    # methane (natural gas primary component)
    'O2':     0.00,    # oxygen (reference element)
    'N2':     0.00,    # nitrogen (reference element)
    'CO2': -393.51,    # carbon dioxide
    'H2O': -241.82,    # water vapor (flue gas state)
    'CO':  -110.53,    # carbon monoxide (incomplete combustion)
}

# Molar masses (g/mol)
MW = {'CH4': 16.04, 'O2': 32.00, 'N2': 28.01,
      'CO2': 44.01, 'H2O': 18.02, 'air': 28.97}

# Average Cp values for flue gas components (J/mol·K, ~1000°C)
Cp_high_T = {'CO2': 54.3, 'H2O': 38.5, 'N2': 32.7, 'O2': 34.9}


# ─────────────────────────────────────────────────────────────
# 1. COMBUSTION ENTHALPY (HESS'S LAW)
# ─────────────────────────────────────────────────────────────

def combustion_enthalpy():
    """
    Calculate standard enthalpy of combustion for methane.
    Reaction: CH4 + 2O2 → CO2 + 2H2O(g)
    ΔH°comb = ΣΔHf°(products) − ΣΔHf°(reactants)
    """
    dH = (Hf_298['CO2'] + 2*Hf_298['H2O']) - (Hf_298['CH4'] + 2*Hf_298['O2'])
    dH_per_kg = dH / MW['CH4'] * 1000  # kJ/kg
    LHV = abs(dH_per_kg)               # Lower Heating Value

    print("\n" + "="*60)
    print("  1. COMBUSTION ENTHALPY — Hess's Law")
    print("="*60)
    print(f"\n  Reaction: CH₄ + 2O₂ → CO₂ + 2H₂O(g)")
    print(f"\n  Enthalpies of formation used:")
    for s in ['CH4','O2','CO2','H2O']:
        print(f"    ΔHf°({s:>4}) = {Hf_298[s]:>8.2f} kJ/mol")
    print(f"\n  ΔH°combustion = {dH:.2f} kJ/mol CH₄")
    print(f"  ΔH°combustion = {dH_per_kg:.1f} kJ/kg CH₄")
    print(f"  Lower Heating Value (LHV) ≈ {LHV:.0f} kJ/kg")

    return dH, LHV


# ─────────────────────────────────────────────────────────────
# 2. STOICHIOMETRIC AIR CALCULATION
# ─────────────────────────────────────────────────────────────

def air_requirement(excess_air_pct=20.0):
    """
    Calculate stoichiometric and actual air requirements.
    CH4 + 2O2 → CO2 + 2H2O
    Air is 21% O2 by volume (79% N2).

    Parameters:
        excess_air_pct : excess air percentage (industrial furnaces: 10–30%)
    """
    mol_O2_stoich = 2.0
    mol_air_stoich = mol_O2_stoich / 0.21
    mass_air_stoich = mol_air_stoich * MW['air'] / MW['CH4']  # kg/kg fuel

    factor = 1 + excess_air_pct / 100
    mol_air_actual  = mol_air_stoich * factor
    mass_air_actual = mass_air_stoich * factor

    print(f"\n{'='*60}")
    print(f"  2. AIR REQUIREMENT  |  Excess air: {excess_air_pct}%")
    print(f"{'='*60}")
    print(f"  Stoichiometric O₂  : {mol_O2_stoich:.2f} mol / mol CH₄")
    print(f"  Stoichiometric air : {mol_air_stoich:.3f} mol / mol CH₄")
    print(f"  Stoich. mass ratio : {mass_air_stoich:.3f} kg air / kg CH₄")
    print(f"  Actual air (λ={factor:.2f}) : {mol_air_actual:.3f} mol / mol CH₄")
    print(f"  Actual mass ratio  : {mass_air_actual:.3f} kg air / kg CH₄")

    return mol_air_stoich, mol_air_actual, factor


# ─────────────────────────────────────────────────────────────
# 3. FLUE GAS COMPOSITION
# ─────────────────────────────────────────────────────────────

def flue_gas_composition(excess_air_pct=20.0):
    """
    Calculate molar composition of flue gas on dry and wet basis.
    With excess air: some O2 passes through unreacted.
    """
    factor = 1 + excess_air_pct / 100
    mol_air = (2.0 / 0.21) * factor

    # Moles of each component per mole of CH4 burned
    n = {
        'CO2': 1.0,
        'H2O': 2.0,
        'N2':  mol_air * 0.79,
        'O2':  mol_air * 0.21 - 2.0,  # excess O2
    }
    total_wet = sum(n.values())
    total_dry = total_wet - n['H2O']

    print(f"\n{'='*60}")
    print(f"  3. FLUE GAS COMPOSITION  |  Excess air: {excess_air_pct}%")
    print(f"{'='*60}")
    print(f"  {'Component':<8}  {'Moles':>8}  {'Wet %':>8}  {'Dry %':>8}")
    print(f"  {'-'*38}")
    for comp, moles in n.items():
        wet_pct = moles / total_wet * 100
        dry_pct = moles / total_dry * 100 if comp != 'H2O' else 0
        dry_str = f"{dry_pct:>8.2f}" if comp != 'H2O' else "    —   "
        print(f"  {comp:<8}  {moles:>8.3f}  {wet_pct:>8.2f}  {dry_str}")
    print(f"  {'TOTAL':<8}  {total_wet:>8.3f}  {'100.00':>8}")

    return n, total_wet


# ─────────────────────────────────────────────────────────────
# 4. ADIABATIC FLAME TEMPERATURE
# ─────────────────────────────────────────────────────────────

def adiabatic_flame_temperature(excess_air_pct=0.0):
    """
    Estimate adiabatic flame temperature (stoichiometric combustion).
    Energy released = energy absorbed by flue gas products.
    Q = Σ(n_i · Cp_i · ΔT)
    """
    dH, _ = combustion_enthalpy()
    Q_released = abs(dH) * 1000  # J/mol CH4

    factor   = 1 + excess_air_pct / 100
    mol_air  = (2.0 / 0.21) * factor
    n_flue   = {'CO2': 1.0, 'H2O': 2.0,
                'N2': mol_air*0.79, 'O2': mol_air*0.21 - 2.0}

    # Σ(n_i · Cp_i) for flue gas mixture
    heat_capacity = sum(n_flue[c] * Cp_high_T[c] for c in n_flue)

    T_initial    = 298.15  # K (25°C reactants)
    T_adiabatic  = T_initial + Q_released / heat_capacity

    print(f"\n{'='*60}")
    print(f"  4. ADIABATIC FLAME TEMPERATURE")
    print(f"{'='*60}")
    print(f"  Heat released      : {Q_released/1000:.2f} kJ/mol CH₄")
    print(f"  Flue gas Cp total  : {heat_capacity:.2f} J/mol·K")
    print(f"  T_adiabatic        : {T_adiabatic:.0f} K  ({T_adiabatic-273.15:.0f}°C)")
    print(f"  (Actual T will be lower due to heat losses & dissociation)")

    return T_adiabatic


# ─────────────────────────────────────────────────────────────
# 5. HEAT RECOVERY ANALYSIS
# ─────────────────────────────────────────────────────────────

def heat_recovery_analysis(T_flue_exit=150.0, T_ref=25.0):
    """
    Estimate heat recoverable from flue gas before stack discharge.
    This is the basis for economizer/HRSG design in petrochemical plants.

    Parameters:
        T_flue_exit : flue gas exit temperature to atmosphere (°C)
        T_ref       : reference temperature (°C)
    """
    # Per mole of CH4 burned at 20% excess air
    mol_air  = (2.0 / 0.21) * 1.20
    n_flue   = {'CO2': 1.0, 'H2O': 2.0,
                'N2': mol_air*0.79, 'O2': mol_air*0.21 - 2.0}

    # Cp at lower temperature (flue gas cooling range ~150–400°C)
    Cp_low_T = {'CO2': 45.0, 'H2O': 35.0, 'N2': 30.0, 'O2': 32.0}

    T_flue_high = 400.0  # °C — assumed flue gas temperature before economizer
    dT = T_flue_high - T_flue_exit

    Q_recoverable = sum(n_flue[c] * Cp_low_T[c] for c in n_flue) * dT  # J/mol CH4
    LHV_J = 802300.0  # J/mol (from combustion enthalpy)
    recovery_pct = Q_recoverable / LHV_J * 100

    print(f"\n{'='*60}")
    print(f"  5. HEAT RECOVERY FROM FLUE GAS")
    print(f"{'='*60}")
    print(f"  Flue gas temperature range: {T_flue_exit}°C → {T_flue_high}°C")
    print(f"  Recoverable heat    : {Q_recoverable/1000:.2f} kJ/mol CH₄")
    print(f"  As % of LHV         : {recovery_pct:.1f}%")
    print(f"  → Reducing stack T from {T_flue_high}°C to {T_flue_exit}°C recovers")
    print(f"    {recovery_pct:.1f}% of fuel energy — key efficiency lever in")
    print(f"    petrochemical fired heaters and reformer furnaces.")

    return Q_recoverable, recovery_pct


# ─────────────────────────────────────────────────────────────
# 6. THERMAL EFFICIENCY vs STACK TEMPERATURE
# ─────────────────────────────────────────────────────────────

def efficiency_vs_stack_temp():
    """
    Show how lowering stack temperature improves thermal efficiency.
    Directly relevant to fired heater optimization in petrochemical plants.
    """
    T_stack = np.linspace(100, 500, 300)
    LHV_J   = 802300.0
    mol_air  = (2.0/0.21) * 1.20
    n_flue   = {'CO2':1.0,'H2O':2.0,'N2':mol_air*0.79,'O2':mol_air*0.21-2.0}
    Cp_avg   = {'CO2':45.0,'H2O':35.0,'N2':30.0,'O2':32.0}
    T_ref    = 25.0

    Q_loss   = np.array([
        sum(n_flue[c]*Cp_avg[c] for c in n_flue) * (T - T_ref)
        for T in T_stack
    ])
    eta = (1 - Q_loss / LHV_J) * 100
    return T_stack, eta


# ─────────────────────────────────────────────────────────────
# PLOTS
# ─────────────────────────────────────────────────────────────

def plot_results():
    fig = plt.figure(figsize=(14, 10))
    fig.suptitle(
        "Combustion Thermochemistry & Energy Analysis — Natural Gas Fired Plant\n"
        "Chemical Engineering Perspective | Siddhirganj, Narayanganj, Bangladesh",
        fontsize=13, fontweight='bold', y=0.98
    )
    gs = gridspec.GridSpec(2, 2, hspace=0.42, wspace=0.38)

    # Plot 1: Flue gas composition vs excess air
    ax1 = fig.add_subplot(gs[0, 0])
    ea_range = np.linspace(0, 50, 200)
    co2_pct, h2o_pct, n2_pct, o2_pct = [], [], [], []
    for ea in ea_range:
        f = 1 + ea/100
        mol_air = (2.0/0.21)*f
        n = {'CO2':1.0,'H2O':2.0,'N2':mol_air*0.79,'O2':mol_air*0.21-2.0}
        tot = sum(n.values())
        co2_pct.append(n['CO2']/tot*100)
        h2o_pct.append(n['H2O']/tot*100)
        n2_pct.append(n['N2']/tot*100)
        o2_pct.append(n['O2']/tot*100)

    ax1.plot(ea_range, co2_pct, color='#E07B39', linewidth=2, label='CO₂')
    ax1.plot(ea_range, h2o_pct, color='#1B3A6B', linewidth=2, label='H₂O')
    ax1.plot(ea_range, n2_pct,  color='#888888', linewidth=2, label='N₂', linestyle='--')
    ax1.plot(ea_range, o2_pct,  color='#0D7377', linewidth=2, label='O₂ (excess)')
    ax1.axvline(20, color='red', linestyle=':', alpha=0.7, label='Design (20% EA)')
    ax1.set_xlabel("Excess Air (%)", fontsize=10)
    ax1.set_ylabel("Flue Gas Composition (mol%)", fontsize=10)
    ax1.set_title("Flue Gas Composition vs Excess Air", fontsize=11, fontweight='bold')
    ax1.legend(fontsize=8); ax1.grid(True, alpha=0.3)

    # Plot 2: Adiabatic flame temp vs excess air
    ax2 = fig.add_subplot(gs[0, 1])
    T_ad = []
    for ea in ea_range:
        f       = 1 + ea/100
        mol_air = (2.0/0.21)*f
        n_f     = {'CO2':1.0,'H2O':2.0,'N2':mol_air*0.79,'O2':mol_air*0.21-2.0}
        Cp_f    = {'CO2':54.3,'H2O':38.5,'N2':32.7,'O2':34.9}
        Cp_tot  = sum(n_f[c]*Cp_f[c] for c in n_f)
        T_ad.append(298.15 + 802300/Cp_tot - 273.15)

    ax2.plot(ea_range, T_ad, color='#CC3333', linewidth=2.5)
    ax2.axvline(20, color='red', linestyle=':', alpha=0.7, label='Design (20% EA)')
    ax2.set_xlabel("Excess Air (%)", fontsize=10)
    ax2.set_ylabel("Adiabatic Flame Temperature (°C)", fontsize=10)
    ax2.set_title("Flame Temperature vs Excess Air", fontsize=11, fontweight='bold')
    ax2.legend(fontsize=8); ax2.grid(True, alpha=0.3)

    # Plot 3: Thermal efficiency vs stack temperature
    ax3 = fig.add_subplot(gs[1, :])
    T_stack, eta = efficiency_vs_stack_temp()
    ax3.plot(T_stack, eta, color='#1B3A6B', linewidth=2.5)
    ax3.axvline(150, color='green', linestyle='--', alpha=0.7,
                label='Good practice: 150°C stack temp')
    ax3.axvline(300, color='orange', linestyle='--', alpha=0.7,
                label='Poor practice: 300°C stack temp')
    ax3.fill_between(T_stack, eta, eta.min(),
                     where=(T_stack <= 200), alpha=0.1, color='green',
                     label='High efficiency zone')
    ax3.set_xlabel("Stack (Flue Gas Exit) Temperature (°C)", fontsize=11)
    ax3.set_ylabel("Thermal Efficiency (%)", fontsize=11)
    ax3.set_title(
        "Thermal Efficiency vs Stack Temperature\n"
        "Lower stack temperature = more heat recovered = higher efficiency",
        fontsize=11, fontweight='bold'
    )
    ax3.legend(fontsize=9); ax3.grid(True, alpha=0.3)
    ax3.set_xlim([100, 500])

    plt.savefig("combustion_analysis_results.png", dpi=150, bbox_inches='tight')
    print("\nPlot saved → combustion_analysis_results.png")
    plt.show()


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n" + "="*60)
    print("  COMBUSTION THERMOCHEMISTRY & ENERGY ANALYSIS")
    print("  Natural Gas Fired Plant — Siddhirganj, Bangladesh")
    print("="*60)

    combustion_enthalpy()
    air_requirement(excess_air_pct=20.0)
    flue_gas_composition(excess_air_pct=20.0)
    adiabatic_flame_temperature(excess_air_pct=0.0)
    heat_recovery_analysis(T_flue_exit=150.0)
    plot_results()
