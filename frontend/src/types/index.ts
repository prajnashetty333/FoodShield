export type ResilienceProfile = "A" | "B" | "C" | "D";

export interface ProfileDistribution {
  profile: ResilienceProfile;
  count: number;
  percentage: number;
}

export interface OverviewResponse {
  total_scenarios: number;
  mean_replacement_rate: number;
  type_a_percentage: number;
  type_c_percentage: number;
  profile_distribution: ProfileDistribution[];
}

export interface CountryOptions {
  countries: string[];
  commodities: string[];
  years: number[];
}

export interface CountryAnalysisResponse {
  importer: string;
  commodity: string;
  year: number;
  baseline_imports: number;
  supplier_count: number;
  largest_supplier_share: number;
  top3_supplier_share: number;
  HHI: number;
  import_dependence: number;
  lost_supply: number;
  shock_loss_share: number;
  remaining_import_share: number;
  replacement_rate: number;
  tier1_replacement: number;
  tier2_replacement: number;
  tier3_replacement: number;
  unreplaced_supply: number;
  new_origin_share: number;
  resilience_profile: ResilienceProfile;
}

export interface CommodityAnalysisResponse {
  commodity: string;
  total_scenarios: number;
  mean_replacement_rate: number;
  mean_shock_loss_share: number;
  mean_hhi: number;
  profile_distribution: ProfileDistribution[];
}

export interface ShockAnalysisResponse {
  importer: string;
  commodity: string;
  year: number;
  supplier_rank: number;
  shocked_supplier: string;
  lost_supply_tonnes: number;
  shock_loss_share: number;
  remaining_import_share: number;
}

export interface ReplacementAnalysisResponse {
  importer: string;
  commodity: string;
  year: number;
  shock_rank: number;
  shocked_supplier: string;
  lost_supply: number;
  tier1_replacement: number;
  tier2_replacement: number;
  tier3_replacement: number;
  unreplaced_supply: number;
  replacement_rate: number;
  new_origin_share: number;
  outcome_type: string;
  capacity_status: string;
}

export interface ProfileTransitions {
  A_to_C: number;
  C_to_D: number;
}

export interface SensitivitySummaryItem {
  experiment: string;
  mean_replacement_rate: number;
  type_A_share: number;
}

export interface SensitivityAnalysisResponse {
  summaries: SensitivitySummaryItem[];
  transitions_100_to_25: ProfileTransitions;
}

export interface PolicyRecommendation {
  profile: string;
  name: string;
  directions: string[];
}

export interface PolicyResponse {
  framework: PolicyRecommendation[];
  disclaimer: string;
}

export interface MethodologyResponse {
  limitations: string[];
  disclaimer: string;
}
