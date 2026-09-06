# FOODSHIELD Commodity Methodology

## WHEAT
**Definition:** Wheat grain representing the primary traded staple.
**Core trade representation:** Wheat (CPC: '0111)
**Exclusions:** Wheat flour, pasta, bakery products (Processed); bran (Byproduct).
**Double-counting rationale:** Excluding flour and processed foods ensures that downstream processing volumes do not artificially inflate the physical supply dependency.
**Limitations:** Assumes primary wheat grain trade dominates the physical dependency relationship.

## RICE
**Definition:** Rice (paddy or milled) representing the primary grain.
**Core trade representation:** Rice (CPC: '0113)
**Exclusions:** Husked/milled splits (where redundant), rice flour, beverages.
**Double-counting rationale:** Only the aggregate 'Rice' category is included as the primary node. Sub-stages are excluded to avoid counting the same harvest twice.
**Limitations:** Data granularity forces a combined rice view.

## MAIZE
**Definition:** Maize (corn) grain.
**Core trade representation:** Maize (corn) (CPC: '0112)
**Exclusions:** Maize flour, starch, sweet corn, forage (Feed).
**Double-counting rationale:** Excluding downstream processing products like starch and flour. Feed maize is excluded as the focus is human food supply.
**Limitations:** Differentiating human-food maize from feed maize at the border is difficult; 'Maize (corn)' may include some dual-purpose flows.

## PALM OIL
**Definition:** Crude or refined palm oil.
**Core trade representation:** Palm oil (CPC: '2165)
**Exclusions:** Palm kernel, palm kernel oil.
**Double-counting rationale:** Palm oil and palm kernel oil are distinct commodities with distinct markets.
**Limitations:** None significant.

## SUGAR
**Definition:** Centrifugal sugar in raw equivalent terms.
**Core trade representation:** Raw cane or beet sugar (centrifugal only) (CPC: '2351f), Cane sugar, non-centrifugal.
**Exclusions:** Refined sugar, molasses, sugar crops (beet/cane), confectionery.
**Double-counting rationale:** Treating raw sugar as the core bottleneck and excluding refined sugar prevents counting the sugar twice (once entering the refinery, once exiting).
**Limitations:** Some countries might exclusively import refined sugar rather than raw, potentially undercounting their dependency if refined is strictly excluded.

## SUNFLOWER OIL
**Definition:** Crude or refined sunflower oil.
**Core trade representation:** Sunflower-seed oil, crude (CPC: '21631.01)
**Exclusions:** Sunflower seed, cake, meal.
**Double-counting rationale:** Seed and cake are structurally distinct from the pressed oil market.
**Limitations:** Crude vs refined distinction.
