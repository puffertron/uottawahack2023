from Structures.Map import Map
from Structures.Parcel import Parcel

# Initialization
def initialize_objects(raw_data, preset_deliveries: bool | list[str]) -> list[Parcel]:
    deliveries: list[str] = generate_deliveries(preset_deliveries)
    parcels: list[Parcel] = Map.set_up_state(deliveries, raw_data) #todo make this correct
    return parcels

def generate_deliveries(preset_deliveries: bool | list[str]) -> list[str]:
    if not preset_deliveries:
        pass #todo randomly generate deliveries
    else:
        return preset_deliveries
    

# Cluster Assignment
def assign_clusters(parcels: list[Parcel], size: int) -> dict[str: list[Parcel]]:
    cluster_radius: float = get_cluster_radius(size)
    clusters: dict[str: list[Parcel]] = {}
    parcels_to_check = set(parcels)
    for source in parcels_to_check:
        near_parcels: list[Parcel] = get_parcel_neighbourhood(entry[0]) #note: near_parcels should be sorted closest to farthest!
        for parcel in near_parcels:
            if


def get_cluster_radius(distance: float) -> float:
    pass #todo some operation to decide

def get_parcel_neighbourhood(parcel: Parcel) -> list[Parcel]: #note: near_parcels should be sorted closest to farthest!
    pass #todo use quadtrees to give a short list of parcels to check