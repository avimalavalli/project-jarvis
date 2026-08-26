# Backup and Recovery Design v1

Status: Proposed; restore drill not yet performed.

## Scope

Back up canonical memory, audit records, approved non-secret configuration and
database migrations. Derived indexes are rebuildable and need not be treated as
canonical. OS-vault secrets use the vault provider's separate recovery method
and are never copied into repository or ordinary backup archives.

## Controls

- Encrypt backups before they leave the JARVIS Core.
- Use a key that is not stored inside the backup.
- Keep at least one offline or logically isolated recovery copy.
- Record backup version, schema version, creation time and integrity hash.
- Test restoration into an isolated clean environment.
- Audit backup and restore operations without logging private payloads.

## Proposed initial targets

- Recovery point objective: 24 hours.
- Recovery time objective: 4 hours for the single-user prototype.

These targets require owner approval and measurement before production use.

## Restore drill

1. Create an encrypted backup with known synthetic records.
2. Provision a clean isolated environment with no access to live storage.
3. Verify archive integrity before decryption.
4. Restore canonical store, audit store and configuration.
5. Run migrations and rebuild derived indexes.
6. Prove record counts, provenance, corrections and deletions match.
7. Prove a deliberately excluded secret is absent.
8. Record duration, failures, operator and evidence; destroy the test restore.

