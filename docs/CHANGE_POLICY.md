# FOODSHIELD Change Policy

## Safe to change

Documentation, README text, comments, release metadata, `.gitignore`, unused starter assets, and nonfunctional UI styling.

## Requires caution

Backend services, API schemas, visualization code, pipeline scripts, configuration, and frontend request/presentation code. Validate affected paths.

## Do not change without explicit analytical review

Locked analytical CSVs; FAOSTAT sources; commodity/country mappings; Sugar aggregation; exposure/shock logic; replacement tiers; HEEC; resilience profiles; sensitivity definitions; research findings; policy framework; and figure calculations.

Primary replacement is Rank 1 only. Rank 2/3 shocks remain independent Supplier Shock scenarios and must not be made cumulative.
