"""
    Create stations on NEM for interconnectors
    which provide stats on region flows.


"""

import logging
from typing import List

from opennem.core.loader import load_data
from opennem.core.networks import network_from_state, state_from_network_region
from opennem.core.parsers.aemo import (
    AEMOParserException,
    AEMOTableSchema,
    parse_aemo_csv,
)
from opennem.db import SessionLocal
from opennem.db.models.opennem import Facility, Location, Station
from opennem.schema.aemo.mms import MarketConfigInterconnector
from opennem.utils.mime import decode_bytes

logger = logging.getLogger(__name__)


def import_nem_interconnects() -> None:
    session = SessionLocal()

    # Load the MMS CSV file that contains interconnector info
    csv_data = load_data(
        "mms/PUBLIC_DVD_INTERCONNECTOR_202006010000.CSV",
        from_project=True,
    )

    # gotta be a string otherwise decode
    if not isinstance(csv_data, str):
        csv_data = decode_bytes(csv_data)

    # parse the AEMO CSV into schemas
    aemo_table_set = None

    try:
        aemo_table_set = parse_aemo_csv(csv_data)
    except AEMOParserException as e:
        logger.error(e)
        return None

    records: List[MarketConfigInterconnector] = aemo_table_set.get_table(
        "MARKET_CONFIG_INTERCONNECTOR"
    ).get_records()

    for interconnector in records:
        if not isinstance(interconnector, MarketConfigInterconnector):
            raise Exception("Not what we're looking for ")

        if interconnector.regionfrom in [
            "SNOWY1"
        ] or interconnector.regionto in ["SNOWY1"]:
            continue

        logger.debug(interconnector)

        interconnector_station = (
            session.query(Station)
            .filter_by(code=interconnector.interconnectorid)
            .filter_by(network_code=interconnector.interconnectorid)
            .one_or_none()
        )

        if not interconnector_station:
            interconnector_station = Station(
                code=interconnector.interconnectorid,
                network_code=interconnector.interconnectorid,
            )

        interconnector_station.approved = True
        interconnector_station.approved_by = __name__
        interconnector_station.created_by = __name__

        if not interconnector_station.location:
            interconnector_station.location = Location(
                state=state_from_network_region(interconnector.regionfrom)
            )

        interconnector_station.name = interconnector.description

    return None


if __name__ == "__main__":
    import_nem_interconnects()
