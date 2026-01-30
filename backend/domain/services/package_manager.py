from typing import List, Optional
from domain.entities.package_item import PackageItem


class PackageManager:
    def __init__(self, repository):
        self.repository = repository
        self._cache: Optional[List[PackageItem]] = None

    def _ensure_cache(self):
        if self._cache is None:
            try:
                self._cache = self.repository.load_all()
            except Exception as e:
                raise RuntimeError(f"Erro ao carregar pacotes: {e}")

            if self._cache is None:
                self._cache = []

    def reload(self):
        self._cache = None
        self._ensure_cache()

    def get_all_packages(self) -> List[PackageItem]:
        self._ensure_cache()
        return list(self._cache)

    def find_by_name(self, name: str) -> Optional[PackageItem]:
        self._ensure_cache()
        name = name.lower().strip()

        for pkg in self._cache:
            if pkg.name.lower() == name:
                return pkg
        return None

    def find_by_type(self, type_: str) -> List[PackageItem]:
        self._ensure_cache()
        type_ = type_.lower().strip()

        return [p for p in self._cache if p.type.lower() == type_]
