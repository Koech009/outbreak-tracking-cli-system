from datetime import datetime

class Region:
    """Represents a geographic region that tracks outbreak cases."""
    
    def __init__(self, id, name, location):
        self.id = id
        self.name = name
        self.location = location
        self.created_at = datetime.now().isoformat()

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,       
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data):
        region = cls(data["id"], data["name"], data["location"])
        region.created_at = data["created_at"]
        return region

    def region_summary(self):
        """Returns a formatted string summary of the region."""
        return f"Region Info: {self.name} | Location: {self.location} | Created: {self.created_at}"

    def __repr__(self):
        return f"Region(id={self.id}, name={self.name}, location={self.location})"
    
