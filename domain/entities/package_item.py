class PackageItem:
    def __init__(self, name: str = "", type_: str = "", description: str = "", file_path: str = ""):
        self.name = name
        self.type = type_
        self.description = description
        self.file_path = file_path

    @staticmethod
    def from_dict(data: dict) -> "PackageItem":
        return PackageItem(
            name=data.get("Name", ""),
            type_=data.get("Type", ""),
            description=data.get("Description", ""),
            file_path=data.get("FilePath", "")
        )

    def to_dict(self) -> dict:
        return {
            "Name": self.name,
            "Type": self.type,
            "Description": self.description,
            "FilePath": self.file_path,
        }

    def __repr__(self):
        return f"PackageItem(name='{self.name}', type='{self.type}', file='{self.file_path}')"
