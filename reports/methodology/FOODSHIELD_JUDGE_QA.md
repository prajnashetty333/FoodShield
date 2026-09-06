# FOODSHIELD — Judge Q&A

**Q1. Why did you choose these commodities?**
- **Answer**: The six commodities (Wheat, Rice, Maize, Palm Oil, Sugar, Sunflower Oil) represent core components of the global food system with established trade data and varying levels of concentration.
- **Evidence**: Locked commodity universe.
- **Limitation**: The model only evaluates these six and does not account for commodity substitution.

**Q2. Why did you choose Rank-1 supplier shocks?**
- **Answer**: A Rank-1 shock isolates the specific vulnerability of relying on a single dominant supplier. It provides a clear, standardized counterfactual to test replacement capacity across all systems.
- **Evidence**: Figure 02 shows that this shock averages a massive 67.17% loss, making it a rigorous stress test.
- **Limitation**: This is not a geopolitical scenario prediction or a multi-supplier collapse.

**Q3. Why not include domestic production?**
- **Answer**: The research question focuses exclusively on international trade resilience and network structures.
- **Limitation**: The model evaluates trade replacement feasibility, not domestic production adaptation or absolute food security.

**Q4. Why not allow substitution between commodities?**
- **Answer**: Substitution requires assumptions about consumer preferences and nutritional equivalencies that cannot be accurately determined from bilateral trade volumes alone.
- **Limitation**: Real-world shocks might be mitigated by commodity substitution not captured here.

**Q5. How do you know another country has spare capacity?**
- **Answer**: We use the Historical Export Expansion Capacity (HEEC) proxy, based on historically observed outward trade behavior. It models what a supplier has demonstrated it can expand by in the past.
- **Evidence**: The model uses strict tiers prioritizing current and historical suppliers before allowing new origins.
- **Limitation**: HEEC is a proxy, not guaranteed spare physical capacity or actual future supplier willingness.

**Q6. Isn't HEEC an unrealistic assumption?**
- **Answer**: We acknowledge it is a proxy, which is exactly why we performed rigorous sensitivity testing.
- **Evidence**: Figure 06 and 07 show that even scaling HEEC down to 25% (a massive stress test), the replacement rate stays at 98.91%, though the pathway shifts away from Type A (dropping to 79.98%).
- **Limitation**: HEEC relies on historical maximums and does not directly represent future capabilities.

**Q7. Why does your replacement rate reach almost 100%?**
- **Answer**: The 99.83% rate reflects the mathematical capacity of the global trade network to reallocate supply based on historical maximums under an isolated Rank-1 shock. It reveals the network's theoretical flexibility.
- **Evidence**: Figure 03 and Figure 04 support this.
- **Limitation**: Does not mean food security or account for transport constraints.

**Q8. Does 99.83% replacement mean food security?**
- **Answer**: No. FOODSHIELD evaluates trade replacement feasibility, not food security. High aggregate replacement rates do not prove food security.
- **Evidence**: Our findings distinguish explicitly between theoretical replacement and true resilience.
- **Limitation**: The model does not directly represent prices, transport constraints, or consumer-level food insecurity.

**Q9. Why are Type C and D important if they are a minority?**
- **Answer**: Because they highlight systemic bottlenecks. While 87.04% of cases resolve easily (Type A), identifying the 224 country–commodity systems with repeated Type C behavior and 9 with Type D behavior allows policymakers to target specific persistent vulnerabilities.
- **Evidence**: Figure 05 isolates these persistent constraints.
- **Limitation**: These systems are exceptions, not representative of the majority.

**Q10. Why does Rice have higher shock loss?**
- **Answer**: Rice exhibits higher supplier concentration among the six commodities, resulting in an average modeled shock loss of approximately 77.9%. 
- **Evidence**: Figure 02 data.
- **Limitation**: This evaluates trade structure, not global rice availability.

**Q11. Why do you use historical suppliers?**
- **Answer**: A historical supplier (Tier 2) demonstrates an existing institutional or logistical relationship that was active in at least two previous years, making it a more realistic fallback than a completely new origin (Tier 3).
- **Evidence**: The hierarchy (Tier 1 → Tier 2 → Tier 3) structures the replacement pathways.
- **Limitation**: Historical connections do not guarantee a contract will be re-established.

**Q12. Why is 2010 excluded from the primary capacity analysis?**
- **Answer**: 2010 is used to establish historical baseline data for relationships and capacities. The period 2011–2023 provides a consistent window for the capacity-valid scenarios evaluated. 
- **Evidence**: Primary scenario count of 10,953 relies on this consistent window.
- **Limitation**: Limited to the 2011–2023 timeframe.

**Q13. Why don't you use machine learning?**
- **Answer**: The goal is to provide a transparent, deterministic evaluation of trade network capacity. ML could obscure the structural mechanics (the pathways) we are specifically trying to isolate.
- **Evidence**: The transparent hierarchy rules yield 99.83% replacement without complex, uninterpretable models.
- **Limitation**: No forecasts or predictive models are utilized.

**Q14. Can this predict future food crises?**
- **Answer**: No. This is a counterfactual stress test of historical network structures, not a forecast of future geopolitical or climate events.
- **Evidence**: Results are strictly limited to evaluating what happened "in the model" given historical conditions.
- **Limitation**: Does not predict future food security or actual future supplier willingness.

**Q15. What would you improve with more data?**
- **Answer**: Incorporating price elasticities, actual port infrastructure constraints, and contractual obligations would improve the realism of replacement feasibility.
- **Evidence**: The explicit limitations section addresses these gaps.
- **Limitation**: Current limitations include lack of prices, contracts, and transport constraints.
