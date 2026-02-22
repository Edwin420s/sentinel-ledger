"""Initial schema — creates all application tables."""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # --- tokens ---
    op.create_table(
        "tokens",
        sa.Column("address", sa.String(), primary_key=True),
        sa.Column("chain", sa.String(), nullable=False),
        sa.Column("deployer", sa.String(), nullable=False),
        sa.Column("deployer_original_chain", sa.String(), nullable=True),
        sa.Column("deployed_block", sa.BigInteger(), nullable=False),
        sa.Column("deployed_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("bytecode_hash", sa.String(), nullable=True),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("symbol", sa.String(), nullable=True),
        sa.Column("decimals", sa.Integer(), nullable=True),
        sa.Column("contract_score", sa.Float(), default=0.0),
        sa.Column("liquidity_score", sa.Float(), default=0.0),
        sa.Column("ownership_score", sa.Float(), default=0.0),
        sa.Column("deployer_score", sa.Float(), default=0.0),
        sa.Column("final_score", sa.Float(), default=0.0),
        sa.Column("risk_level", sa.String(), default="UNKNOWN"),
        sa.Column("flags", postgresql.JSONB(), nullable=True),
        sa.Column("analyzed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_tokens_chain", "tokens", ["chain"])
    op.create_index("ix_tokens_deployer", "tokens", ["deployer"])

    # --- wallets ---
    op.create_table(
        "wallets",
        sa.Column("address", sa.String(), primary_key=True),
        sa.Column("chain", sa.String(), primary_key=True),
        sa.Column("first_seen_block", sa.BigInteger(), nullable=True),
        sa.Column("first_seen_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("last_seen_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("total_contracts", sa.Integer(), default=0),
        sa.Column("erc20_count", sa.Integer(), default=0),
        sa.Column("suspected_rugs", sa.Integer(), default=0),
        sa.Column("avg_liquidity_duration_hours", sa.Float(), default=0.0),
        sa.Column("wallet_age_days", sa.Integer(), default=0),
        sa.Column("deployer_risk_score", sa.Float(), default=0.0),
        sa.Column("is_flagged", sa.Boolean(), default=False),
        sa.Column("flags", postgresql.JSONB(), nullable=True),
        sa.Column("base_activity", postgresql.JSONB(), nullable=True),
        sa.Column("ethereum_activity", postgresql.JSONB(), nullable=True),
    )

    # --- liquidity_pools ---
    op.create_table(
        "liquidity_pools",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("token_address", sa.String(), sa.ForeignKey("tokens.address"), nullable=False),
        sa.Column("chain", sa.String(), nullable=False),
        sa.Column("dex", sa.String(), nullable=False),
        sa.Column("pool_address", sa.String(), nullable=False),
        sa.Column("initial_liquidity_usd", sa.Float(), default=0.0),
        sa.Column("current_liquidity_usd", sa.Float(), default=0.0),
        sa.Column("peak_liquidity_usd", sa.Float(), default=0.0),
        sa.Column("liquidity_locked", sa.Boolean(), default=False),
        sa.Column("lp_holder", sa.String(), nullable=True),
        sa.Column("lp_lock_contract", sa.String(), nullable=True),
        sa.Column("created_at_block", sa.BigInteger(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("first_liquidity_added_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("first_liquidity_removed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("removed_early", sa.Boolean(), default=False),
        sa.Column("removal_percentage", sa.Float(), default=0.0),
    )
    op.create_index("ix_liquidity_pools_token_address", "liquidity_pools", ["token_address"])

    # --- contract_analysis ---
    op.create_table(
        "contract_analysis",
        sa.Column("token_address", sa.String(), sa.ForeignKey("tokens.address"), primary_key=True),
        sa.Column("chain", sa.String(), primary_key=True),
        sa.Column("has_mint", sa.Boolean(), default=False),
        sa.Column("mint_restricted", sa.Boolean(), default=True),
        sa.Column("has_blacklist", sa.Boolean(), default=False),
        sa.Column("has_pause", sa.Boolean(), default=False),
        sa.Column("has_ownership", sa.Boolean(), default=False),
        sa.Column("ownership_renounced", sa.Boolean(), default=False),
        sa.Column("is_proxy", sa.Boolean(), default=False),
        sa.Column("upgradeable", sa.Boolean(), default=False),
        sa.Column("can_change_fees", sa.Boolean(), default=False),
        sa.Column("can_withdraw", sa.Boolean(), default=False),
        sa.Column("suspicious_patterns", postgresql.JSONB(), nullable=True),
        sa.Column("function_selectors", postgresql.JSONB(), nullable=True),
        sa.Column("analyzed_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )

    # --- risk_history ---
    op.create_table(
        "risk_history",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("token_address", sa.String(), sa.ForeignKey("tokens.address"), nullable=False),
        sa.Column("chain", sa.String(), nullable=False),
        sa.Column("score", sa.Float(), nullable=False),
        sa.Column("level", sa.String(), nullable=False),
        sa.Column("flags", postgresql.JSONB(), nullable=True),
        sa.Column("calculated_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )

    # --- processed_blocks ---
    op.create_table(
        "processed_blocks",
        sa.Column("chain", sa.String(), primary_key=True),
        sa.Column("block_number", sa.BigInteger(), nullable=False),
        sa.Column("processed_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("hash", sa.String(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("processed_blocks")
    op.drop_table("risk_history")
    op.drop_table("contract_analysis")
    op.drop_table("liquidity_pools")
    op.drop_table("wallets")
    op.drop_table("tokens")
