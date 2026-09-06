from services.data_loader import data_loader
from schemas.overview import OverviewResponse, ProfileDistribution

def get_overview_metrics() -> OverviewResponse:
    df = data_loader.get_resilience_metrics()
    
    total_scenarios = len(df)
    
    if total_scenarios == 0:
        return OverviewResponse(
            total_scenarios=0,
            mean_replacement_rate=0.0,
            type_a_percentage=0.0,
            type_c_percentage=0.0,
            profile_distribution=[]
        )
        
    mean_replacement_rate = df['replacement_rate'].mean()
    
    profile_counts = df['resilience_profile'].value_counts()
    
    type_a_count = profile_counts.get("Existing-network resilient", 0)
    type_b_count = profile_counts.get("Historically recoverable", 0)
    type_c_count = profile_counts.get("New-origin dependent", 0)
    type_d_count = profile_counts.get("Structurally constrained", 0)
    
    type_a_percentage = (type_a_count / total_scenarios) * 100
    type_c_percentage = (type_c_count / total_scenarios) * 100
    
    return OverviewResponse(
        total_scenarios=total_scenarios,
        mean_replacement_rate=mean_replacement_rate * 100, # as percentage
        type_a_percentage=type_a_percentage,
        type_c_percentage=type_c_percentage,
        profile_distribution=[
            ProfileDistribution(profile="A", count=int(type_a_count), percentage=(type_a_count/total_scenarios)*100),
            ProfileDistribution(profile="B", count=int(type_b_count), percentage=(type_b_count/total_scenarios)*100),
            ProfileDistribution(profile="C", count=int(type_c_count), percentage=(type_c_count/total_scenarios)*100),
            ProfileDistribution(profile="D", count=int(type_d_count), percentage=(type_d_count/total_scenarios)*100),
        ]
    )
