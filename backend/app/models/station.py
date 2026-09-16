from sqlalchemy import Column, Integer, String, Float, Boolean, Text
from app.database import Base

class ChargingStation(Base):
    __tablename__ = "charging_stations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(200), nullable=False, index=True)
    latitude = Column(Float, nullable=False, index=True)
    longitude = Column(Float, nullable=False, index=True)
    address = Column(String(255), nullable=True)
    city = Column(String(100), nullable=True, index=True)
    state = Column(String(50), nullable=True, index=True)
    country = Column(String(50), default="US")
    operator = Column(String(100), nullable=False, index=True) # e.g. Tesla Supercharger, Electrify America, EVgo, ChargePoint, IONITY
    power_kw = Column(Float, nullable=False) # e.g. 50, 150, 250, 350
    total_ports = Column(Integer, default=8)
    available_ports = Column(Integer, default=6)
    connector_types = Column(String(200), default="CCS, NACS") # Comma separated: CCS, NACS, CHAdeMO, Type 2
    price_per_kwh = Column(Float, default=0.36) # USD per kWh
    amenities = Column(String(255), default="Restrooms, Dining, WiFi") # Comma separated
    is_operational = Column(Boolean, default=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "country": self.country,
            "operator": self.operator,
            "power_kw": self.power_kw,
            "total_ports": self.total_ports,
            "available_ports": self.available_ports,
            "connector_types": [c.strip() for c in self.connector_types.split(",") if c.strip()],
            "price_per_kwh": self.price_per_kwh,
            "amenities": [a.strip() for a in self.amenities.split(",") if a.strip()],
            "is_operational": self.is_operational,
        }
