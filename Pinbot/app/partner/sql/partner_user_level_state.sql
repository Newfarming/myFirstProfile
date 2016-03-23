CREATE OR REPLACE VIEW `partner_user_level_state` AS
SELECT `partner_taskcoinrecord`.`id`, `auth_user`.`username` AS `username`,
        SUM(CASE WHEN `partner_taskcoinrecord`.`record_type` = 'check' THEN 1 ELSE 0 END) AS `check_count`,
        SUM(CASE WHEN `partner_taskcoinrecord`.`record_type` = 'download' THEN 1 ELSE 0 END) AS `download_count`,
        SUM(CASE WHEN `partner_taskcoinrecord`.`record_type` = 'interview' THEN 1 ELSE 0 END) AS `interview_count`,
        SUM(CASE WHEN `partner_taskcoinrecord`.`record_type` = 'taking_work' THEN 1 ELSE 0 END) AS `taking_work_count`
FROM `partner_taskcoinrecord`, `partner_uploadresume`, `auth_user`
WHERE `partner_taskcoinrecord`.`upload_resume_id` = `partner_uploadresume`.`id`
AND `partner_uploadresume`.`user_id` = `auth_user`.`id`
GROUP BY `partner_uploadresume`.`user_id`
