CREATE OR REPLACE VIEW lead_calendar_view AS
    SELECT
       id as id,
       id as "lead_id",
       status,
       leads_lead.result as "result",
       NULL as "task_id",
       created as date,
       'pending_lead' as type,
       user_id as user_id,
       'lead' as subtype
    FROM  leads_lead WHERE status='new'
    UNION
    SELECT
           leads_task.id*100 as id,
           lead_id as "lead_id",
           l.status as "status",
           l.result as "result",
           leads_task.id as "task_id",
           planified_realization_date as date,
           'pending_task' as type,
           l.user_id as user_id,
           type as subtype
    FROM leads_task inner join leads_lead l on l.id=leads_task.lead_id
        WHERE is_traking_task=0 and realization_date_check=0 and lead_id is NOT NULL
    UNION
    SELECT
           leads_task.id*1000 as id,
           lead_id as "lead",
           l.status as "status",
           l.result as "result",
           leads_task.id as "task_id",
           planified_realization_date as date,
           'pending_traking' as type,
           l.user_id as user_id,
           type as subtype
    FROM leads_task inner join leads_lead l on l.id=leads_task.lead_id
        WHERE is_traking_task=1 and realization_date_check=0  and lead_id is NOT NULL;