from typing import Sequence, Union

from alembic import op


revision: str = "da89053c4f4e"
down_revision: Union[str, Sequence[str], None] = "c6be139b95a3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_index(
        "idx_network_nodes_location",
        table_name="network_nodes",
    )

    op.drop_index(
        "idx_network_links_geometry",
        table_name="network_links",
    )

    op.drop_index(
        "idx_service_zones_geometry",
        table_name="service_zones",
    )


def downgrade() -> None:
    op.create_index(
        "idx_network_nodes_location",
        "network_nodes",
        ["location"],
        postgresql_using="gist",
    )

    op.create_index(
        "idx_network_links_geometry",
        "network_links",
        ["geometry"],
        postgresql_using="gist",
    )

    op.create_index(
        "idx_service_zones_geometry",
        "service_zones",
        ["geometry"],
        postgresql_using="gist",
    )