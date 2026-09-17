from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geography


revision: str = "c6be139b95a3"
down_revision: Union[str, Sequence[str], None] = "3bb92d90c72f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    # ---------------------------------------------------------
    # network_nodes
    # ---------------------------------------------------------
    op.create_table(
        "network_nodes",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column(
            "node_code",
            sa.String(50),
            nullable=False,
            unique=True,
        ),
        sa.Column(
            "name",
            sa.String(255),
            nullable=False,
        ),
        sa.Column(
            "node_type",
            sa.String(50),
            nullable=False,
        ),
        sa.Column(
            "location",
            Geography(
                geometry_type="POINT",
                srid=4326,
            ),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.CheckConstraint(
            "node_type <> ''",
            name="ck_network_nodes_node_type_not_empty",
        ),
    )

    # ---------------------------------------------------------
    # network_links
    # ---------------------------------------------------------
    op.create_table(
        "network_links",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column(
            "link_code",
            sa.String(50),
            nullable=False,
            unique=True,
        ),
        sa.Column(
            "source_node_id",
            sa.BigInteger(),
            sa.ForeignKey(
                "network_nodes.id",
                ondelete="RESTRICT",
            ),
            nullable=False,
        ),
        sa.Column(
            "target_node_id",
            sa.BigInteger(),
            sa.ForeignKey(
                "network_nodes.id",
                ondelete="RESTRICT",
            ),
            nullable=False,
        ),
        sa.Column(
            "name",
            sa.String(255),
            nullable=False,
        ),
        sa.Column(
            "link_type",
            sa.String(50),
            nullable=False,
        ),
        sa.Column(
            "geometry",
            Geography(
                geometry_type="LINESTRING",
                srid=4326,
            ),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.CheckConstraint(
            "source_node_id <> target_node_id",
            name="ck_network_links_different_nodes",
        ),
        sa.CheckConstraint(
            "link_type <> ''",
            name="ck_network_links_link_type_not_empty",
        ),
    )

    # ---------------------------------------------------------
    # service_zones
    # ---------------------------------------------------------
    op.create_table(
        "service_zones",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column(
            "zone_code",
            sa.String(50),
            nullable=False,
            unique=True,
        ),
        sa.Column(
            "name",
            sa.String(255),
            nullable=False,
        ),
        sa.Column(
            "zone_type",
            sa.String(50),
            nullable=False,
        ),
        sa.Column(
            "geometry",
            Geography(
                geometry_type="POLYGON",
                srid=4326,
            ),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.CheckConstraint(
            "zone_type <> ''",
            name="ck_service_zones_zone_type_not_empty",
        ),
    )

    # ---------------------------------------------------------
    # Spatial indexes
    # ---------------------------------------------------------
    op.create_index(
        "idx_network_nodes_location_gist",
        "network_nodes",
        ["location"],
        postgresql_using="gist",
    )

    op.create_index(
        "idx_network_links_geometry_gist",
        "network_links",
        ["geometry"],
        postgresql_using="gist",
    )

    op.create_index(
        "idx_service_zones_geometry_gist",
        "service_zones",
        ["geometry"],
        postgresql_using="gist",
    )

    # ---------------------------------------------------------
    # Required relational indexes
    # ---------------------------------------------------------
    op.create_index(
        "idx_network_links_source_node_id",
        "network_links",
        ["source_node_id"],
    )

    op.create_index(
        "idx_network_links_target_node_id",
        "network_links",
        ["target_node_id"],
    )


def downgrade() -> None:

    op.drop_index(
        "idx_network_links_target_node_id",
        table_name="network_links",
    )

    op.drop_index(
        "idx_network_links_source_node_id",
        table_name="network_links",
    )

    op.drop_index(
        "idx_service_zones_geometry_gist",
        table_name="service_zones",
    )

    op.drop_index(
        "idx_network_links_geometry_gist",
        table_name="network_links",
    )

    op.drop_index(
        "idx_network_nodes_location_gist",
        table_name="network_nodes",
    )

    op.drop_table("service_zones")
    op.drop_table("network_links")
    op.drop_table("network_nodes")