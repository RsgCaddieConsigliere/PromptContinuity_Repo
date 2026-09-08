PRAGMA foreign_keys = ON;

CREATE TABLE runs (
  run_id TEXT PRIMARY KEY,
  started_at TEXT NOT NULL,
  completed_at TEXT,
  mode TEXT NOT NULL CHECK (mode IN ('READ_ONLY','PLAN_ONLY','EXECUTE_APPROVED')),
  source_set_id TEXT,
  owner TEXT NOT NULL,
  write_scope TEXT,
  root_id TEXT,
  run_seed TEXT,
  status TEXT NOT NULL,
  notes TEXT
);

CREATE TABLE access_scope (
  scope_id TEXT PRIMARY KEY,
  root_drive_id TEXT NOT NULL,
  path_label TEXT NOT NULL,
  matter TEXT,
  read_allowed INTEGER NOT NULL,
  write_allowed INTEGER NOT NULL,
  create_allowed INTEGER NOT NULL,
  rename_allowed INTEGER NOT NULL,
  move_allowed INTEGER NOT NULL,
  delete_allowed INTEGER NOT NULL DEFAULT 0,
  share_allowed INTEGER NOT NULL DEFAULT 0,
  hitl_required INTEGER NOT NULL DEFAULT 1,
  authority_source_type TEXT NOT NULL,
  authority_source_ref TEXT,
  technical_capabilities_json TEXT,
  observed_at TEXT,
  notes TEXT
);

CREATE TABLE file_instances (
  file_instance_id TEXT PRIMARY KEY,
  root_id TEXT NOT NULL,
  original_relative_path TEXT NOT NULL,
  original_filename TEXT NOT NULL,
  first_observed_run_id TEXT NOT NULL REFERENCES runs(run_id),
  current_relative_path TEXT NOT NULL,
  protection_class TEXT NOT NULL DEFAULT 'UNKNOWN' CHECK (protection_class IN ('SOURCE_IMMUTABLE','MUTABLE_WORK_PRODUCT','DERIVATIVE','QUARANTINE','UNKNOWN')),
  sticky_protection_source TEXT,
  source_or_derivative_role TEXT NOT NULL DEFAULT 'UNKNOWN',
  quarantine_flag INTEGER NOT NULL DEFAULT 0,
  status TEXT NOT NULL DEFAULT 'ACTIVE',
  UNIQUE(root_id, original_relative_path, file_instance_id)
);

CREATE TABLE source_objects (
  src_id TEXT PRIMARY KEY,
  run_id TEXT NOT NULL REFERENCES runs(run_id),
  file_instance_id TEXT NOT NULL REFERENCES file_instances(file_instance_id),
  content_id TEXT,
  matter TEXT,
  drive_id TEXT,
  gmail_message_id TEXT,
  current_parent_id TEXT,
  current_relative_path TEXT NOT NULL,
  original_relative_path TEXT NOT NULL,
  original_name TEXT NOT NULL,
  mime_type TEXT NOT NULL,
  size_bytes_pre INTEGER,
  size_bytes_post INTEGER,
  mtime_ns_pre INTEGER,
  mtime_ns_post INTEGER,
  created_time TEXT,
  modified_time TEXT,
  google_native INTEGER NOT NULL DEFAULT 0,
  version TEXT,
  revision_id TEXT,
  drive_sha256 TEXT,
  local_sha256 TEXT,
  export_format TEXT,
  export_sha256 TEXT,
  fixity_basis TEXT NOT NULL,
  fixity_status TEXT NOT NULL,
  hash_error TEXT,
  protection_class TEXT NOT NULL DEFAULT 'UNKNOWN',
  sticky_protection_source TEXT,
  source_or_derivative_role TEXT NOT NULL DEFAULT 'UNKNOWN',
  quarantine_flag INTEGER NOT NULL DEFAULT 0,
  symlink_flag INTEGER NOT NULL DEFAULT 0,
  path_escape_flag INTEGER NOT NULL DEFAULT 0,
  extension_mismatch_flag INTEGER NOT NULL DEFAULT 0,
  hidden_flag INTEGER NOT NULL DEFAULT 0,
  exclusion_status TEXT NOT NULL DEFAULT 'INCLUDED',
  exclusion_reason TEXT,
  relationship_scan_status TEXT,
  collision_status TEXT,
  provenance_status TEXT NOT NULL DEFAULT 'OBSERVED',
  current_disposition TEXT NOT NULL DEFAULT 'KEEP',
  observed_at TEXT,
  UNIQUE(run_id, file_instance_id)
);

CREATE TABLE emails (
  email_id TEXT PRIMARY KEY,
  src_id TEXT NOT NULL REFERENCES source_objects(src_id),
  gmail_message_id TEXT,
  gmail_thread_id TEXT,
  rfc_message_id TEXT,
  internal_date TEXT,
  date_header TEXT,
  from_value TEXT,
  to_value TEXT,
  cc_value TEXT,
  bcc_value TEXT,
  subject TEXT,
  in_reply_to TEXT,
  references_header TEXT,
  raw_mime_sha256 TEXT,
  native_status TEXT NOT NULL CHECK (native_status IN ('GMAIL_NATIVE','EML_NATIVE','EMAIL_DERIVATIVE','SOURCE_MISSING'))
);

CREATE TABLE attachments (
  attachment_id TEXT PRIMARY KEY,
  email_id TEXT NOT NULL REFERENCES emails(email_id),
  parent_src_id TEXT NOT NULL REFERENCES source_objects(src_id),
  child_src_id TEXT REFERENCES source_objects(src_id),
  gmail_attachment_id TEXT,
  ordinal INTEGER,
  original_filename TEXT,
  mime_type TEXT,
  size_bytes INTEGER,
  sha256 TEXT NOT NULL
);

CREATE TABLE relationships (
  relationship_id TEXT PRIMARY KEY,
  from_src_id TEXT NOT NULL REFERENCES source_objects(src_id),
  to_src_id TEXT NOT NULL REFERENCES source_objects(src_id),
  relationship_type TEXT NOT NULL,
  basis TEXT NOT NULL,
  certainty TEXT NOT NULL DEFAULT 'UNKNOWN' CHECK (certainty IN ('CONFIRMED','HIGH_CONFIDENCE','CANDIDATE','UNKNOWN')),
  confidence REAL CHECK (confidence IS NULL OR (confidence >= 0 AND confidence <= 1)),
  family_id TEXT,
  observed_at TEXT,
  notes TEXT,
  UNIQUE(from_src_id, to_src_id, relationship_type)
);

CREATE TABLE duplicate_families (
  family_id TEXT PRIMARY KEY,
  family_type TEXT NOT NULL,
  canonical_src_id TEXT REFERENCES source_objects(src_id),
  sha256 TEXT,
  member_count INTEGER NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('CANDIDATE','HITL_REVIEW','LOCKED','REJECTED')),
  rationale TEXT
);

CREATE TABLE propositions (
  proposition_id TEXT PRIMARY KEY,
  src_id TEXT REFERENCES source_objects(src_id),
  assertion_text TEXT NOT NULL,
  assertion_type TEXT NOT NULL,
  attribution_platform TEXT,
  attribution_thread TEXT,
  attribution_turn TEXT,
  status TEXT NOT NULL,
  controlling_proposition_id TEXT,
  verification_question TEXT,
  notes TEXT
);

CREATE TABLE rename_move_plan (
  proposal_id TEXT PRIMARY KEY,
  src_id TEXT NOT NULL REFERENCES source_objects(src_id),
  file_instance_id TEXT NOT NULL REFERENCES file_instances(file_instance_id),
  content_id TEXT,
  old_parent_id TEXT,
  old_name TEXT NOT NULL,
  proposed_parent_id TEXT,
  proposed_name TEXT NOT NULL,
  naming_rule_version TEXT NOT NULL,
  operation TEXT NOT NULL CHECK (operation IN ('RENAME','MOVE','RENAME_MOVE','COPY')),
  protection_class TEXT NOT NULL,
  eligibility_status TEXT NOT NULL CHECK (eligibility_status IN ('ELIGIBLE','BLOCKED')),
  block_reason TEXT,
  collision_status TEXT NOT NULL DEFAULT 'UNKNOWN',
  expected_pre_sha256 TEXT,
  expected_post_sha256 TEXT,
  reason TEXT NOT NULL,
  family_id TEXT,
  policy_status TEXT NOT NULL,
  hitl_required INTEGER NOT NULL DEFAULT 1,
  parent_approval_status TEXT NOT NULL DEFAULT 'PENDING'
);

CREATE TABLE transactions (
  tx_id TEXT PRIMARY KEY,
  proposal_id TEXT REFERENCES rename_move_plan(proposal_id),
  file_instance_id TEXT NOT NULL REFERENCES file_instances(file_instance_id),
  action TEXT NOT NULL CHECK (action IN ('RENAME','MOVE','RENAME_MOVE','COPY')),
  state TEXT NOT NULL,
  drive_id TEXT NOT NULL,
  expected_parent_id TEXT,
  expected_name TEXT NOT NULL,
  expected_fixity TEXT NOT NULL,
  new_parent_id TEXT,
  new_name TEXT,
  approved_by TEXT,
  approved_at TEXT,
  applied_at TEXT,
  verified_at TEXT,
  rollback_parent_id TEXT,
  rollback_name TEXT,
  error_code TEXT,
  error_message TEXT
);

CREATE TABLE transaction_events (
  event_id TEXT PRIMARY KEY,
  tx_id TEXT NOT NULL REFERENCES transactions(tx_id),
  from_state TEXT,
  to_state TEXT NOT NULL,
  event_time TEXT NOT NULL,
  actor TEXT NOT NULL,
  evidence_json TEXT,
  notes TEXT
);

CREATE TABLE exceptions_hitl (
  exception_id TEXT PRIMARY KEY,
  run_id TEXT REFERENCES runs(run_id),
  src_id TEXT REFERENCES source_objects(src_id),
  file_instance_id TEXT REFERENCES file_instances(file_instance_id),
  tx_id TEXT REFERENCES transactions(tx_id),
  severity TEXT NOT NULL CHECK (severity IN ('INFO','REVIEW','BLOCKER')),
  exception_type TEXT NOT NULL,
  description TEXT NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('OPEN','RESOLVED','PARKED')),
  owner TEXT,
  resolution TEXT
);

CREATE INDEX idx_instance_current_path ON file_instances(root_id, current_relative_path);
CREATE INDEX idx_source_content ON source_objects(content_id);
CREATE INDEX idx_source_sha ON source_objects(drive_sha256, local_sha256);
CREATE INDEX idx_source_drive ON source_objects(drive_id);
CREATE INDEX idx_source_instance ON source_objects(file_instance_id, run_id);
CREATE INDEX idx_email_rfc ON emails(rfc_message_id);
CREATE INDEX idx_attachment_sha ON attachments(sha256);
CREATE INDEX idx_rel_from_to ON relationships(from_src_id, to_src_id);
CREATE INDEX idx_tx_state ON transactions(state);
