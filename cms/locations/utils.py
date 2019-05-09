def filter_national(location):
    if location.get('type') == 'National':
        return True
    else:
        return False


def filter_regions(locations):
    from locations.models import Location

    def is_region(location):
        if location.get('type') == 'Region':
            return True
        else:
            return False

    regions_data = filter(is_region, locations)
    regions = []
    for region in regions_data:
        regions.append(Location().set_values(region))
    return regions


def filter_trusts(locations):
    from locations.models import Location

    def is_trust(location):
        if location.get('type') == 'Trust':
            return True
        else:
            return False

    trusts_data = filter(is_trust, locations)
    trusts = []
    for trust in trusts_data:
        trusts.append(Location().set_values(trust))
    return trusts


def filter_sites(location):
    if location.get('type') == 'Site':
        return True
    else:
        return False
