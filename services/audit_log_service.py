from models.audit_log_model import AuditLog

def create_audit_log(db, user_id, action, entity, entity_id):
    audit = AuditLog( user_id=user_id, action=action, entity=entity, entity_id=entity_id)
    db.add(audit)
    db.commit()
    return audit

def get_audit_logs(db):
    return db.query(AuditLog).all()

def user_audit_logs(db, user_id):
    return (db.query(AuditLog).filter(AuditLog.user_id == user_id).all())