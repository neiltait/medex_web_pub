from errors.utils import log_internal_error


def filter_national(locations):
    from locations.models import Location

    def is_national(location):
        if location.get('type') == 'National':
            return True
        else:
            return False

    national_data = list(filter(is_national, locations))
    if len(national_data) != 1:
        log_internal_error('loading national location',
                           'Expected to find 1 national location instead found %s' % len(national_data))
        return Location()
    else:
        return Location().set_values(national_data[0])


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


def filter_sites(locations):
    from locations.models import Location

    def is_site(location):
        if location.get('type') == 'Site':
            return True
        else:
            return False

    site_data = filter(is_site, locations)
    sites = []
    for site in site_data:
        sites.append(Location().set_values(site))
    return sites
