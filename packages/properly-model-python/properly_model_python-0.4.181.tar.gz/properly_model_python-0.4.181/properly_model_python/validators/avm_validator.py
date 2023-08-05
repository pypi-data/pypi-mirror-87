BASE_REQUIRED_FEATURES = [
    "address",
    "bedroomsTotal",
    "bathroomsFull",
    "bathroomsTotal",
    "buildingType",
    "enclosedParking",
    "directionFaces",
    "latitude",
    "longitude",
    "parking",
    "style",
    "totalParking",
]

CONDO_ONLY_REQUIRED_FEATURES = [
    "associationFee",
    "bedroomsStandard",
    "buildingPlaceId",
    "unitNumber",
]

RESIDENTIAL_ONLY_REQUIRED_FEATURES = [
    "basement",
    "exterior",
    "heatingType",
]


def check_property_price_avm_ready(model_property: dict) -> bool:
    """
    Determines whether there is enough data to get a reasonable AVM price estimate
    :param model_property: dictionary of property values in ModelProperty spec
    :return: True if the input contains enough data for a reasonable AVM price estimate
    """
    city_code = model_property.get("properlyCityCode")
    municipality_code = model_property.get("properlyMunicipalityCode")

    # Initially we only support the City of Toronto
    if city_code != "toronto-on-ca" or municipality_code != "toronto-on-ca":
        return False

    if "associationFee" in model_property:
        required_features = BASE_REQUIRED_FEATURES + CONDO_ONLY_REQUIRED_FEATURES
    else:
        required_features = BASE_REQUIRED_FEATURES + RESIDENTIAL_ONLY_REQUIRED_FEATURES

    for feature in required_features:
        if feature not in model_property:
            return False

    return True
