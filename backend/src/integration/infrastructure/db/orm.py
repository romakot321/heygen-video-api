from sqlalchemy.orm import Mapped

from src.db.base import BaseMixin, Base


class AvatarDB(BaseMixin, Base):
    __tablename__ = "avatars"

    user_id: Mapped[str]
    app_bundle: Mapped[str]
    heygen_group_id: Mapped[str]
    heygen_id: Mapped[str | None]
