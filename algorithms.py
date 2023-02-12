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

    parcels_to_check: set[Parcel] = set(parcels)
    for origin in parcels_to_check:
        cluster: dict[str: list[Parcel]] = {origin.name: [origin]}
        for source in cluster[origin.name]:
            near_parcels: list[tuple[Parcel, float]] = get_parcel_neighbourhood(source) #note: near_parcels should be sorted closest to farthest!
            for (target, distance) in near_parcels:
                if (distance <= cluster_radius) and (target not in cluster[origin.name]):
                  target.cluster_id = origin.name
                  cluster[origin.name].append(target)
                  parcels_to_check.remove(target)
                else:
                  break
        if len(cluster[origin.name]) > 1:
            clusters.update(cluster)
        parcels_to_check.remove(origin)


def get_cluster_radius(distance: float) -> float:
    pass #todo some operation to decide

def get_parcel_neighbourhood(parcel: Parcel) -> list[tuple(Parcel, float)]: #note: near_parcels should be sorted closest to farthest!
    #todo use quadtrees to give a short list of parcels to check along with associated distance using Map.find_distance() function
    #also sort the list by proximity to source parcel
    pass 