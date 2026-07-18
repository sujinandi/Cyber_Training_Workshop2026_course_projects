**PySCF Electronic-Structure Interface for Libra**  
This project provides a PySCF-based electronic-structure interface for nonadiabatic molecular dynamics (NAMD) in Libra. The implementation is built around a general electronic-structure abstraction that separates the Libra dynamics layer from the details of a specific electronic-structure method.  
PySCF CASSCF is used here as the primary implementation and demonstration of the interface.  
**1. Architecture**  
The main architectural feature of this project is the separation of the electronic-structure implementation from the Libra NAMD workflow through a common interface:  
Libra NAMD  
     |  
     v  
 strategy_compute_adi()  
     |  
     |  Libra input -> ES_Request  
     v  
 ES_Strategy  
     |  
     |  electronic-structure calculation  
     v  
 ES_Result  
     |  
     |  type/unit conversion  
     v  
 Libra Hamiltonian data  
   
The interface is organized around three main abstractions:  
- ES_Request specifies which electronic-structure properties are requested.  
- ES_Strategy defines the common interface implemented by an electronic-structure method.  
- ES_Result provides a common representation of the calculated electronic-structure data.  
The strategy_compute_adi() adapter connects this generic interface to Libra's dynamics machinery. It converts Libra inputs into the generic ES representation, invokes the selected ES_Strategy, and converts the resulting data back into Libra types.  
For time-overlap calculations, the adapter also manages the lifetime of consecutive electronic-structure snapshots:  
Frame n-1                    Frame n  
 ES(R[n-1])                   ES(R[n])  
      |                           |  
      +-------- overlap ----------+  
                   |  
                   v  
            S(R[n-1], R[n])  
   
This allows a high-level dynamics or preprocessing workflow to repeatedly call strategy_compute_adi() without explicitly managing previous and current electronic-structure objects.  
Although the implementations provided in this project use PySCF, the abstraction is designed so that the NAMD-facing adapter is not coupled to a specific electronic-structure strategy.  
The interface is located in the Libra devel source tree under:  
src/libra_py/packages/pyscf/  
   
The main components include the electronic-structure interfaces, PySCF implementations, and the methods.py adapter containing strategy_compute_adi().  
**2. CASSCF NBRA Phase-1 Workflow**  
The example script in the script/ directory demonstrates the first phase of a two-phase NBRA workflow using a LiF CASSCF calculation.  
The example defines a predetermined Li-F bond-stretch trajectory and repeatedly calls:  
strategy_compute_adi(q, model_params, full_id)  
   
For each geometry frame, the workflow obtains:  
1. Adiabatic electronic energies E_i(R_n)  
2. Time overlaps between neighboring electronic wavefunctions S_{ij}(R_{n-1}, R_n)  
3. The corresponding vibronic Hamiltonian H_{\mathrm{vib}}(t), where the time-derivative coupling is estimated from neighboring-frame time overlaps.  
The overall workflow is:  
Predetermined geometry trajectory  
 R0 -> R1 -> R2 -> ... -> RN  
         |  
         v  
 strategy_compute_adi()  
         |  
         +--> E(Rn)  
         |  
         +--> S(R[n-1], R[n])  
         |  
         +--> Hvib(tn)  
         |  
         v  
 Phase-1 output  
   
The example writes:  
- results/lif_nbra_phase1_table.csv, containing the geometry, energies, time-overlap matrix elements, and vibronic Hamiltonian matrix elements for inspection  
- results/lif_hvib_only.npz, containing the precomputed time-dependent H_{\mathrm{vib}} sequence intended for subsequent NBRA dynamics  
This demonstrates the separation between the two NBRA stages:  
Phase 1: Electronic structure  
   
 Geometry trajectory  
       |  
       v  
 PySCF CASSCF  
       |  
       v  
 Energies + time overlaps  
       |  
       v  
 Hvib(t)  
   
 Phase 2: Quantum dynamics  
   
 Precomputed Hvib(t)  
       |  
       v  
 NBRA / surface hopping  
       |  
       v  
 Electronic populations and transitions  
   
The electronic-structure calculations can therefore be performed independently of the subsequent ensemble of stochastic dynamics calculations.  
**3. PySCF CASSCF NACV Example**  
The low-level interface example demonstrates direct use of the PySCF CASSCF implementation through the generic electronic-structure interface.  
The example constructs a CASSCF strategy and an ES_Request requesting:  
- electronic energies,  
- nonadiabatic coupling vectors (NACVs), and  
- neighboring-geometry time overlaps.  
The calculation returns these quantities through a common ES_Result.  
For two electronic states and a two-atom LiF system, the NACV array has the structure:  
(nstates, nstates, natoms, 3)  
   
or:  
(2, 2, 2, 3)  
   
corresponding to the derivative couplings:  
 \mathbf{d}_{ij}^{A} = \left\langle \Psi_i \middle| \nabla_A \Psi_j \right\rangle   
The example also demonstrates the use of two consecutive CASSCF electronic-structure snapshots to evaluate the time-overlap matrix:  
 S_{ij}(R_n, R_{n+1}) = \left\langle \Psi_i(R_n) \middle| \Psi_j(R_{n+1}) \right\rangle   
This example serves as a direct test of the CASSCF implementation and the common ES_Request / ES_Result API, whereas the higher-level example demonstrates integration at the Libra strategy_compute_adi() adapter level.  
**Summary**  
These examples demonstrate two levels of the interface:  
Low-level ES interface test  
 ---------------------------  
   
 CASSCF  
   |  
   +--> ES_Request  
   |  
   +--> ES_Result  
          |  
          +--> energies  
          +--> NACVs  
          +--> time overlaps  
   
 High-level Libra integration  
 ----------------------------  
   
 Libra / NBRA workflow  
         |  
         v  
 strategy_compute_adi()  
         |  
         v  
 ES_Strategy abstraction  
         |  
         v  
 PySCF CASSCF  
         |  
         v  
 Libra-compatible  
 ham_adi / time_overlap_adi / hvib_adi  
   
The key design goal achieved here is to make electronic-structure methods interchangeable behind a common interface while keeping the Libra NAMD workflow independent of backend-specific implementation details.  
