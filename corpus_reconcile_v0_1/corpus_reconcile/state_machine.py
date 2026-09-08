from __future__ import annotations
from dataclasses import dataclass
from .constants import TxState, TxAction

ALLOWED = {
    TxState.DRAFT: {TxState.HITL_PENDING, TxState.CANCELLED},
    TxState.HITL_PENDING: {TxState.APPROVED, TxState.CANCELLED},
    TxState.APPROVED: {TxState.PRECONDITION_CHECK, TxState.STALE, TxState.CANCELLED},
    TxState.PRECONDITION_CHECK: {TxState.EXECUTING, TxState.STALE, TxState.CONFLICT, TxState.FAILED},
    TxState.EXECUTING: {TxState.APPLIED, TxState.FAILED},
    TxState.APPLIED: {TxState.READBACK_VERIFIED, TxState.CONFLICT, TxState.ROLLBACK_PENDING},
    TxState.READBACK_VERIFIED: {TxState.CLOSED, TxState.ROLLBACK_PENDING},
    TxState.ROLLBACK_PENDING: {TxState.ROLLED_BACK, TxState.FAILED},
    TxState.STALE: set(),
    TxState.CONFLICT: {TxState.ROLLBACK_PENDING, TxState.CANCELLED},
    TxState.FAILED: {TxState.ROLLBACK_PENDING, TxState.CANCELLED},
    TxState.ROLLED_BACK: set(),
    TxState.CANCELLED: set(),
    TxState.CLOSED: set(),
}

@dataclass(frozen=True)
class Transaction:
    tx_id: str
    action: TxAction
    state: TxState = TxState.DRAFT

    def transition(self, target: TxState) -> "Transaction":
        if target not in ALLOWED[self.state]:
            raise ValueError(f"Illegal transition {self.state} -> {target}")
        return Transaction(self.tx_id, self.action, target)

def validate_action(action: str) -> TxAction:
    try:
        return TxAction(action)
    except ValueError as exc:
        raise ValueError("v0.1 permits only RENAME, MOVE, RENAME_MOVE, COPY; DELETE is intentionally unsupported") from exc
